# Architecture Overview

## Status of This Document

This document describes the **intended** architecture for NewAngle, updated as of Phase 1 (data model). As of Phase 1:

- **Implemented:** the Entity/Event layer's schema — `Company`, `ListedSecurity`, `Source`, `CorporateEvent`, `PromoterHoldingObservation` — with migrations and tests. See `packages/data/README.md` and `docs/decisions/001` through `003`.
- **Not yet implemented:** Data Sources (no connector selected/built), Ingestion, Normalization logic (the schema exists; nothing populates it from a real source yet), Research Analytics, the Evidence Layer, API, and Frontend.

This document will continue to be updated as each remaining layer is actually built, and any deviation between what was planned here and what was actually implemented is recorded via a decision record under `docs/decisions/`.

## Why an Architecture Document Exists Before Any Code

NewAngle is a research/evidence platform. Its credibility depends on being able to answer, for any conclusion it presents, "where did this come from and how was it derived?" That requires a clear separation between raw data, normalized data, derived analytics, and presentation from the outset, rather than retrofitting it later. This document defines that separation before implementation begins.

## Intended System Layers

```text
Data Sources
    ↓
Ingestion
    ↓
Normalization
    ↓
Entity / Event Layer
    ↓
Research Analytics
    ↓
Evidence Layer
    ↓
API
    ↓
Frontend
```

- **Data Sources** — External, authoritative sources of market data, corporate filings, and corporate/governance events. No source has been selected or integrated yet; source evaluation (authoritativeness, historical coverage, stability, usage terms, redistribution rights) happens before any connector is built, and will be documented under `docs/data-sources/` once it exists.
- **Ingestion** — Retrieval of data from a source, with retry/error handling and no dependency on live sources during tests.
- **Normalization** — Converting raw, source-specific formats into a consistent internal representation, while preserving the original raw reference.
- **Entity / Event Layer** — Structured representations of companies, sources, and corporate events, with explicit provenance fields (`event_date`, `publication_date`, `available_at`, `source`, `retrieved_at`). **Implemented as of Phase 1** — see `packages/data/`. Company identity is kept separate from listed-security identity (symbol/exchange/ISIN) to survive ticker changes and dual listings; see `docs/decisions/001-company-security-identity.md`. Point-in-time fields use timestamp (not date) precision for `available_at`, based on verified Indian exchange disclosure-timeline behavior; see `docs/decisions/002-provenance-and-point-in-time.md`.
- **Research Analytics** — Signal detection and statistical methods (e.g., an event-study framework) applied to the entity/event layer, always respecting point-in-time correctness (no use of information not yet available at a given analysis cutoff).
- **Evidence Layer** — Structuring analytics output into an auditable, source-linked, uncertainty-aware form — not a black-box score.
- **API** — Exposes evidence-backed research objects with typed contracts; does not expose fabricated or placeholder values as if they were real.
- **Frontend** — Presents results while clearly distinguishing observed data, historical relationships, model output, hypothesis, scenario, and (only if validated) forecast. These categories are never blurred.

## Boundary Principle: Raw vs. Normalized vs. Derived vs. Presented

A recurring source of misleading research tools is conflating these four things. NewAngle keeps them explicit at every layer:

1. **Raw data** — exactly what a source returned, with a reference back to it. **Not yet stored in Phase 1** — no ingestion pipeline exists to produce raw payloads yet, so `raw_reference` on each event/observation is currently a pointer to where the raw document would be found at the source, not a stored copy of it. See `docs/decisions/002-provenance-and-point-in-time.md` ("What Was Deliberately Deferred") for why building raw-payload storage now would be premature.
2. **Normalized data** — raw data mapped into NewAngle's internal schema, without adding interpretation.
3. **Derived analytics** — output of an explicit, documented, versioned methodology applied to normalized data (e.g., an abnormal return calculation).
4. **Research conclusions / presentation** — how derived analytics are communicated to a user, always alongside methodology, sample size, uncertainty, and limitations.

No layer is allowed to silently produce something that looks like the layer above it (e.g., a number that looks like derived analytics but is actually a fabricated placeholder must be explicitly labeled as such, never presented as real).

## Planned Technology Stack

Chosen for being boring and sufficient, not for novelty (see README — "simple architecture first"). Nothing below is installed or configured yet; it is documented here so implementation decisions in later phases are consistent with what was originally planned, and any deviation is a deliberate, documented choice rather than an accident.

| Layer | Planned technology |
|---|---|
| Backend | Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic, pytest |
| Database | PostgreSQL |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Data processing | Pandas and/or Polars, NumPy, SciPy (where statistically justified) |

Explicitly deferred unless a concrete requirement emerges: Kubernetes, Kafka, Neo4j / graph databases, vector databases, microservices, custom LLM training, reinforcement learning, real-time tick infrastructure.

## Repository Layout (Current)

```text
newangle/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
│   ├── architecture/
│   │   └── overview.md
│   └── decisions/
│       ├── 001-company-security-identity.md
│       ├── 002-provenance-and-point-in-time.md
│       └── 003-promoter-holding-observation-model.md
└── packages/
    └── data/                  # newangle-data: ORM models, migrations, tests
        ├── README.md
        ├── pyproject.toml
        ├── alembic.ini
        ├── alembic/
        ├── src/newangle_data/
        └── tests/
```

`apps/` (API, frontend) and further `packages/` (`analytics`, `common`) referenced in the long-term structure are intentionally **not** created yet — they will be added in the phase where they first have real content, not pre-emptively. `docs/data-sources/` and `docs/methodology/` are likewise not created yet: no data source has been selected/investigated (that's Phase 2), and no research methodology exists to document (that's later still).

## Next Steps

Phase 2 (data source investigation / ingestion foundation) will identify and evaluate a real data source for the schema implemented in Phase 1, document its provenance and licensing terms under `docs/data-sources/`, and build the ingestion layer that actually populates `CorporateEvent` and `PromoterHoldingObservation` rows from it — still without building analytics or signal detection.
