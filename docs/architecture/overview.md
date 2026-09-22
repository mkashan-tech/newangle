# Architecture Overview

## Status of This Document

This document describes the **intended** architecture for NewAngle. As of Phase 0 (repository foundation), **none of the layers described below are implemented.** This document exists to guide upcoming implementation decisions and to make boundaries explicit from the start — it is not a description of working software.

This document will be updated as each layer is actually built, and any deviation between what was planned here and what was actually implemented will be recorded (either inline or via a decision record under `docs/decisions/`, once that becomes relevant).

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
- **Entity / Event Layer** — Structured representations of companies, sources, and corporate events, with explicit provenance fields (`event_date`, `publication_date`, `available_at`, `source`, `retrieved_at`).
- **Research Analytics** — Signal detection and statistical methods (e.g., an event-study framework) applied to the entity/event layer, always respecting point-in-time correctness (no use of information not yet available at a given analysis cutoff).
- **Evidence Layer** — Structuring analytics output into an auditable, source-linked, uncertainty-aware form — not a black-box score.
- **API** — Exposes evidence-backed research objects with typed contracts; does not expose fabricated or placeholder values as if they were real.
- **Frontend** — Presents results while clearly distinguishing observed data, historical relationships, model output, hypothesis, scenario, and (only if validated) forecast. These categories are never blurred.

## Boundary Principle: Raw vs. Normalized vs. Derived vs. Presented

A recurring source of misleading research tools is conflating these four things. NewAngle keeps them explicit at every layer:

1. **Raw data** — exactly what a source returned, with a reference back to it.
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
└── docs/
    └── architecture/
        └── overview.md
```

Directories such as `apps/`, `packages/`, `tests/`, and `scripts/` referenced in the long-term structure are intentionally **not** created yet — they will be added in the phase where they first have real content (Phase 1 onward), not pre-emptively.

## Next Steps

Phase 1 (data model) will introduce the entity/event layer described above, starting with `companies`, `sources`, and event/provenance structures — implemented, tested, and documented before any ingestion or analytics logic is added.
