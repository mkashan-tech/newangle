# NewAngle — Technical Architecture

Document 04 · Version 1.0 · 28 September 2026 (current-state note added for Phase 1 — see §2 and §23)

Current foundation · Target architecture · Data flow · Engineering boundaries

## Document Status

- **Status:** FOUNDATION ARCHITECTURE
- **Owner:** Mohammad Kashan
- **Purpose:** Describe the intended system while clearly separating implemented architecture from future direction.
- **Authority:** Repository/code is authoritative for implementation; this document records architectural intent.
- **Boundary:** Future components remain proposals until an actual requirement justifies them.

## 1. Architecture Objective

NewAngle should support a trustworthy research workflow: ingest permitted data, preserve provenance and point-in-time information, normalize entities/events, perform reproducible analysis, expose evidence through an API, and present it through a research-oriented interface.

**Principle:** Prefer the smallest architecture that can produce a reliable, testable research result.

## 2. Current Repository State

> **Updated for Phase 1.** This section was written at the foundation (Phase 0) stage, when only README and license files existed. It is updated here to reflect the current repository state as of this document set being added; it is not a claim that later phases described elsewhere in this document (ingestion, API, frontend) are implemented.

- README and MIT License form the initial repository foundation (Phase 0).
- A tested, migration-backed PostgreSQL schema (`packages/data/`) now exists for companies, listed securities, sources, corporate events, and promoter holding observations, with point-in-time and provenance fields — see `docs/architecture/overview.md` and `docs/decisions/001-003-*.md` for the implemented data model. This schema contains no production data.
- Production backend (API), frontend, data connectors/ingestion, and an analytics pipeline are **not yet implemented**.
- The earlier AI-assisted V0 prototype is product exploration, not the production architecture.

## 3. Target High-Level Architecture

- **Source/ingestion layer** — permitted market, company, event, and contextual sources.
- **Raw/reference layer** — source references and original observations where storage is permitted.
- **Normalization layer** — canonical companies, people, events, instruments, dates, and identifiers.
- **Research data layer** — point-in-time observations and analytical-ready datasets.
- **Analytics layer** — returns, event studies, statistics, robustness checks, and research artifacts.
- **Evidence/provenance layer** — sources, timestamps, methodology versions, transformations, and limitations.
- **API/application layer** — typed research endpoints and application services.
- **Web application layer** — company intelligence, events, evidence, and future research workflows.

## 4. Logical Data Flow

```text
SOURCE → INGEST → VALIDATE → NORMALIZE → STORE → ANALYZE → EVIDENCE → API → UI
```

Transformations should preserve enough metadata to explain where an analytical value came from and what processing was applied.

## 5. Proposed Technology Direction

| Layer | Candidate | Status | Reason |
|---|---|---|---|
| Backend API | FastAPI + Pydantic | TARGET | Typed Python API suitable for research/data services. |
| Persistence | SQLAlchemy + Alembic | **IN USE (packages/data)** | Explicit models and controlled migrations; adopted and implemented in Phase 1. |
| Database | PostgreSQL | **IN USE (schema implemented, no production data)** | Relational integrity, querying, timestamps, and metadata. |
| Frontend | Next.js + TypeScript + Tailwind | TARGET | Typed web application and research-oriented UI. |
| Analytics | Python + Pandas/Polars + NumPy/SciPy | TARGET | Practical data and statistical computing; choose based on workload. |
| Testing | pytest + appropriate frontend tooling | **IN USE for packages/data (pytest)**; frontend tooling still TARGET | Automated validation of calculations, APIs, and UI. |
| Charts | Research-appropriate charting library | OPEN | Choose from actual analytical UX requirements. |

This is the proposed stack, not a claim that every component is required immediately. The "IN USE" annotations above reflect only the `packages/data` schema/migration work; the rest of the stack remains at the TARGET/OPEN stage this document originally described.

## 6. Repository Structure

- `README.md` — public project overview.
- `LICENSE` — MIT license.
- `.env.example` — configuration names without secrets.
- `CONTRIBUTING.md` — contribution workflow.
- `SECURITY.md` — security reporting guidance.
- `apps/api/` — backend application.
- `apps/web/` — frontend application.
- `packages/data/` — data ingestion/normalization utilities when justified. *(Phase 1 note: this package now contains the implemented SQLAlchemy models, Alembic migrations, and Pydantic schemas for the core domain — see `packages/data/README.md`.)*
- `packages/analytics/` — reusable analytical/research code.
- `packages/common/` — shared schemas/utilities only when genuinely needed.
- `docs/architecture/` — architecture documentation.
- `docs/methodology/` — research methodology.
- `docs/product/` — product and roadmap documentation.
- `docs/decisions/` — ADRs and decision records.
- `docs/data-sources/` — source-specific provenance and rights.
- `docs/onboarding/` — contributor/AI onboarding.
- `tests/` — cross-component/research tests where appropriate.
- `scripts/` — reproducible operational/research scripts.
- `notebooks/` — exploratory research, not production application logic.

Do not create empty directories merely to make the repository look complete.

## 7. Core Domain Concepts

- **Company** — canonical listed-company entity.
- **Instrument** — tradeable security representation with exchange/ticker context.
- **Person** — management/promoter/insider entity where appropriate.
- **Source** — documented information origin.
- **Event** — corporate/market occurrence with defined timing.
- **Observation** — source-backed value/fact available at a defined time.
- **Signal** — explicitly defined derived analytical condition.
- **Study** — reproducible research analysis with configuration and methodology version.
- **Study result** — structured analytical output.
- **Evidence** — traceable support for an observation or analytical result.
- **Methodology version** — versioned definition of how an analysis was produced.

## 8. Conceptual Data Model

```text
companies
instruments
people
sources
events
observations
signals
studies
study_results
methodology_versions
```

This is a domain model, not a frozen database migration. The final schema must follow validated use cases and source research. *(Note: the Phase 1 implementation in `packages/data` covers `companies`, `listed_securities`, `sources`, `corporate_events`, and `promoter_holding_observations` — a subset of this conceptual model scoped to what Phase 1 needed; see `docs/decisions/001-003-*.md` for the reasoning.)*

## 9. Point-in-Time Data Model

Historical reconstruction may require several distinct timestamps:

- `as_of_date` — date the underlying value describes.
- `event_date` — date the event occurred or is defined to occur.
- `publication_date` — source publication/disclosure date where available.
- `available_at` — when the information can be treated as publicly available for historical research.
- `retrieved_at` — when NewAngle obtained the source/data.

These timestamps should not be collapsed into one field when doing so would create hindsight leakage.

## 10. Source and Provenance Architecture

- Source identity and type.
- Canonical URL/reference or document identifier.
- Access/retrieval timestamp.
- Coverage period.
- Terms/licensing reference.
- Redistribution status.
- Transformation history where relevant.
- Known limitations.

Public accessibility does not automatically mean that a source may be scraped, stored, or redistributed.

## 11. Data Ingestion Principles

- Prefer authoritative sources where available.
- Validate coverage before designing around a source.
- Separate ingestion from normalization.
- Make ingestion repeatable and observable.
- Handle rate limits and failures explicitly.
- Do not silently overwrite historical observations.
- Record provenance for derived data.
- Keep credentials outside source control.

## 12. Analytics Architecture

Analytics code should be separated from UI code and source-specific ingestion logic. A study should run from explicit configuration and produce a structured result artifact.

- Input dataset/reference
- Event definition
- Universe definition
- Analysis cutoff
- Benchmark
- Window configuration
- Methodology version
- Result statistics
- Robustness outputs
- Limitations/provenance

## 13. API Design Principles

- Use typed request/response schemas.
- Separate domain/application logic from route handlers.
- Return provenance metadata when analytical claims depend on it.
- Avoid endpoint names that imply unsupported certainty.
- Version breaking API contracts.
- Validate authorization before protected operations.
- Never expose secrets or restricted raw data.

## 14. Frontend Architecture Principles

- Distinguish observations, historical relationships, model outputs, hypotheses, scenarios, and forecasts.
- Analytical cards should provide paths to methodology and evidence.
- Company/event pages should be composable from reusable research components.
- Charts should provide enough context to reduce misleading interpretation.
- Loading, missing, stale, and unavailable states must be explicit.
- Synthetic/demo data must be identifiable during development.

## 15. Authentication and Authorization

Authentication and role-based authorization should be introduced when accounts or protected operations require them.

- Separate authentication from authorization.
- Use secure credential/token handling.
- Never commit secrets.
- Use environment/secret configuration.
- Audit sensitive administrative operations.
- Default to least privilege.

## 16. Caching and Performance

Performance architecture should be evidence-driven. Add caching when repeated expensive work or data access is demonstrated.

- Define freshness requirements.
- Make stale-data behavior explicit.
- Do not cache sensitive information without a security model.
- Measure bottlenecks before introducing distributed infrastructure.

## 17. Event Processing and Future Extensions

Kafka or similar streaming infrastructure may become useful for high-volume ingestion or real-time propagation, but it is not an initial requirement.

- Start with simple jobs/scheduled pipelines where sufficient.
- Introduce queues/streaming only when workload or reliability requires them.
- Avoid microservices before domain boundaries and operational needs are proven.

## 18. AI Architecture Boundary

AI should sit on top of trustworthy evidence and research infrastructure rather than compensate for missing foundations.

- Retrieval should point to source-backed evidence.
- Generated summaries should distinguish observed facts from interpretation.
- AI outputs should carry provenance where possible.
- Private model chain-of-thought is not a product artifact.
- Custom model training is deferred until a concrete validated use case exists.
- AI must not manufacture empirical results or fill missing data with invented values.

## 19. Security and Reliability

- Secrets managed through environment/secret-management systems.
- Dependency and vulnerability management.
- Input validation.
- Database migration discipline.
- Automated tests for critical analytical calculations.
- Backups/recovery planning once persistent production data exists.
- Structured logging without leaking sensitive information.
- Explicit failure states rather than silent corruption.

## 20. Testing Strategy

- Unit tests for calculations and domain logic.
- Data validation tests for ingestion/normalization.
- Regression tests for methodology-critical outputs.
- API contract tests.
- Integration tests for database workflows.
- Frontend tests for important research workflows.
- Reproducibility checks for published studies.

Analytical code deserves strong regression testing because a small implementation change can alter historical results.

## 21. Observability and Auditability

- Record pipeline runs and failures.
- Record methodology/data versions for research jobs.
- Track source retrieval where useful.
- Make stale or incomplete data visible.
- Preserve enough metadata to diagnose unexpected analytical changes.

## 22. Architecture Decisions Not Yet Frozen

- Exact first data providers.
- Exact first signal.
- Exact event-study configuration.
- Whether/when Kafka is needed.
- Whether/when Redis is needed.
- Whether a knowledge graph is warranted.
- Exact charting library.
- Cloud provider and deployment topology.

These should be resolved through ADRs when they become implementation decisions. *(The exact database schema item from the original list has moved out of this "not yet frozen" set — see §23 and `docs/decisions/001-003-*.md`.)*

## 23. Current vs Target Architecture

> **Updated for Phase 1.** The Database row below has been updated from the original "Not implemented" to reflect the schema/migration work completed in `packages/data`. Other rows are unchanged from the original document.

| Area | Current state | Target direction |
|---|---|---|
| Repository | Foundation files, documentation, and an implemented data-model package (`packages/data`). | Application organized around data, analytics, API, and web layers. |
| Data | No production ingestion pipeline; no production data. | Permitted, provenance-aware, point-in-time data pipelines. |
| Database | Schema and versioned migrations implemented (`packages/data`, PostgreSQL via SQLAlchemy/Alembic), covering companies, listed securities, sources, corporate events, and promoter holding observations. No production data loaded. | PostgreSQL with versioned migrations. *(Target substantially reached for the domain covered so far; broader domain coverage remains target work.)* |
| Backend | Not implemented. | FastAPI service with typed boundaries. |
| Frontend | Not implemented. | Next.js/TypeScript research interface. |
| Analytics | Methodology documented; production pipeline absent. | Reproducible studies and evidence artifacts. |
| Infrastructure | Minimal. | Scale only when measured requirements justify it. |

## 24. Architecture Review Checklist

- Does the design solve a current requirement?
- Can major data values be traced to a source?
- Can historical information timing be preserved?
- Are research calculations separated from presentation code?
- Can critical calculations be tested?
- Does the design avoid unnecessary distributed complexity?
- Are licensing/redistribution constraints represented?
- Are secrets excluded from source control?
- Is current state clearly separated from future state?
- Is a material architectural decision recorded in an ADR?

## 25. Open Architecture Questions

- What exact source/data model is required for the first research signal?
- Which data should be relational versus file/object-based?
- What job orchestration is sufficient for the first production pipeline?
- When does caching become necessary?
- What deployment environment best supports reproducible research and a public project?
- Which domain boundaries should become services only after actual complexity appears?

## 26. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial technical architecture foundation; separates current state from target direction and avoids prematurely freezing unsettled choices. |
| 1.0 (annotated) | — | §2, §5, §6, §8, §22, and §23 annotated during conversion to Markdown to reflect the Phase 1 `packages/data` schema/migration work completed after this document was first drafted. No other content changed. |
