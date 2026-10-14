# NewAngle — Data Sources & Provenance

Document 08 · Version 1.0 · 28 September 2026

A source-governance framework for trustworthy, point-in-time market intelligence

## Document Status

- **Status:** FOUNDATION DATA-GOVERNANCE DOCUMENT
- **Owner:** Mohammad Kashan
- **Purpose:** Define how NewAngle discovers, evaluates, records, ingests, validates, cites, and governs external data.
- **Authority:** This document defines the general source/provenance framework. Individual source records contain source-specific facts.
- **Critical limitation:** No source is approved merely because it is publicly accessible. Each source requires its own feasibility, rights, coverage, reliability, and provenance review.

## 1. Why Data Provenance Matters

NewAngle connects market numbers with people, companies, events, context, and historical evidence. That goal is credible only when important observations can be traced to their origin, availability time, transformations, and limitations.

- Evidence without provenance is difficult to audit.
- A current value may not represent what was knowable at an earlier point in time.
- Public accessibility does not automatically grant unrestricted redistribution rights.
- Different providers may define the same field differently.
- Historical research can be invalidated by look-ahead leakage, survivorship bias, revisions, or corporate-action errors.

**Core principle:** Every important analytical input should be traceable from the derived result back to its source and transformation history.

## 2. Source-of-Truth Hierarchy

1. Authoritative primary/regulatory source, when available and appropriate.
2. Official company disclosure or filing.
3. Official exchange/provider publication.
4. Established secondary provider used with documented limitations.
5. Derived/internal dataset created by NewAngle.
6. AI-generated interpretation — never a substitute for underlying evidence.

This is not a universal ranking of data quality. Fitness depends on the specific field, date range, definition, completeness, licensing, and research use case.

## 3. Source Evaluation Before Integration

Before implementing a connector, answer:

- What exact data does the source provide?
- Who publishes or controls it?
- What is the historical coverage and earliest reliable date?
- Is the information point-in-time or retrospectively revised?
- What are publication and information-availability timestamps?
- How stable is the access method?
- Is there an API, downloadable file, filing feed, or documented interface?
- What are usage, licensing, attribution, and redistribution constraints?
- Are automated access, caching, storage, and derivative datasets permitted?
- What rate limits or authentication requirements apply?
- What happens when the source changes format or disappears?
- How will NewAngle validate imported values?

## 4. Source Record Template

Each important source should have a source record under the repository data-source documentation area.

- Source ID
- Source name
- Publisher/owner
- Source type
- Official URL/reference
- Data domains
- Specific fields used
- Geographic/market scope
- Historical coverage
- Update frequency
- Publication timestamp semantics
- Information-availability semantics
- Access method
- Authentication requirements
- Rate limits
- Terms/licensing reference
- Redistribution status
- Storage/caching permission status
- Known limitations
- Validation strategy
- Failure/fallback strategy
- Last reviewed date
- Review owner
- Status

## 5. Recommended Source Statuses

- **DISCOVERED** — identified but not yet evaluated.
- **UNDER REVIEW** — feasibility, rights, and quality are being assessed.
- **APPROVED** — reviewed for a specific documented use case.
- **LIMITED** — usable only with stated restrictions or limitations.
- **DEPRECATED** — no longer recommended for new ingestion.
- **BLOCKED** — unsuitable because of reliability, rights, access, or other material concerns.

## 6. Provenance Model

Conceptual chain:

```text
SOURCE → RAW OBSERVATION → NORMALIZATION → VALIDATION → DERIVED DATA → ANALYSIS → EVIDENCE CARD
```

- **SOURCE** identifies the external origin.
- **RAW OBSERVATION** preserves the obtained source observation, subject to lawful storage constraints.
- **NORMALIZATION** records transformations such as units, identifiers, dates, or field mappings.
- **VALIDATION** records quality checks and anomalies.
- **DERIVED DATA** records reproducible transformations.
- **ANALYSIS** records methodology/version.
- **EVIDENCE CARD** exposes relevant provenance to users.

## 7. Point-in-Time Provenance

Historical research requires more than knowing today's value. NewAngle should distinguish when an event happened from when information about it became available.

| Field | Meaning |
|---|---|
| `event_date` | When the underlying event occurred. |
| `as_of_date` | The date to which a reported value applies. |
| `publication_date` | When the publisher released information. |
| `available_at` | When information could reasonably have been obtained by the research system. |
| `retrieved_at` | When NewAngle retrieved it. |
| `effective_date` | When a change became effective, where relevant. |

For historical analysis, enforce the relevant cutoff rule: information used at cutoff T must satisfy the applicable availability condition, such as `available_at ≤ T`.

## 8. Raw, Normalized, Derived, and Analytical Data

- **Raw:** closest practical representation of the source observation, subject to storage/licensing constraints.
- **Normalized:** standardized identifiers, units, dates, categories, and schemas.
- **Derived:** calculations or transformations produced by NewAngle.
- **Analytical output:** event-study results, distributions, comparisons, or other research outputs.

These layers should not be silently conflated. Users should be able to distinguish source observations from NewAngle-derived values.

## 9. Identifier and Entity Resolution

- Maintain canonical internal entity identifiers.
- Store source-specific identifiers separately.
- Record identifier validity periods when identifiers change.
- Do not resolve ambiguous entities silently.
- Keep an audit trail for material entity-resolution decisions.

## 10. Data Quality Checks

- Schema/type validation.
- Required-field validation.
- Date and timestamp sanity checks.
- Range checks where economically meaningful.
- Duplicate detection.
- Identifier consistency.
- Corporate-action consistency.
- Cross-source reconciliation where independent comparison is possible.
- Missingness and coverage reporting.
- Unexpected structural-change detection.

## 11. Handling Revisions

- Record revision/update timestamps where available.
- Do not overwrite historical observations without preserving relevant provenance.
- Document whether a dataset is current-state or point-in-time capable.
- Do not claim point-in-time validity when the source cannot support it.

## 12. Corporate Actions and Historical Prices

Price and return research can be distorted by splits, bonuses, dividends, mergers, demergers, rights issues, symbol changes, delistings, and other corporate actions.

- Document whether prices are raw or adjusted.
- Document the adjustment methodology/provider.
- Ensure event-study returns use internally consistent price series.
- Treat benchmark and security calendars consistently.
- Test major corporate-action cases before relying on the dataset.

## 13. Source Licensing & Redistribution

Open-source NewAngle code does not automatically make third-party data open source. Data rights must be evaluated separately.

- Do not assume public visibility means unrestricted reuse.
- Keep source terms/reference links in source documentation.
- Avoid committing restricted raw datasets to the public repository.
- Keep credentials and access tokens outside source control.
- If redistribution is unclear, do not publish the dataset until the use case is reviewed.
- Prefer sources whose permitted use is compatible with NewAngle's needs.

## 14. Ingestion Architecture Expectations

```text
SOURCE → INGEST → VALIDATE → NORMALIZE → STORE → ANALYZE → EVIDENCE → API → UI
```

- Connectors should be replaceable where practical.
- Source-specific parsing should remain isolated from domain logic.
- Ingestion failures should be observable.
- Retries should respect source limits.
- Source references should be preserved where permitted.
- Transformations should be deterministic where possible.

## 15. Provenance Exposed to Users

Important research outputs should expose enough information to understand the evidence without exposing private model reasoning.

- Observation/event
- Company/entity
- Event date
- Information-available timestamp
- Source
- Source reference
- Underlying dataset or data version
- Methodology/version
- Sample size
- Benchmark
- Study window
- Observed result
- Uncertainty/distribution where relevant
- Limitations

## 16. Source Quality Is Use-Case Specific

There is no single universal best source. A filing may be authoritative for a corporate disclosure while another provider may be practical for historical prices. Fitness must be assessed for the analytical purpose.

- Authority
- Completeness
- Timeliness
- Historical depth
- Point-in-time capability
- Consistency
- Machine accessibility
- Legal usability
- Validation feasibility

## 17. What NewAngle Must Not Do

- Invent a source when a source has not been verified.
- Invent historical coverage.
- Present a secondary source as an official source.
- Claim point-in-time correctness without evidence.
- Hide missing data.
- Silently substitute a different provider.
- Publish restricted data merely because it is useful.
- Treat AI-generated summaries as primary evidence.
- Use an unstable core dependency without documenting the risk.

## 18. First Data-Source Research Workflow

1. Define the exact research question and required fields.
2. List candidate authoritative sources.
3. Evaluate coverage and historical availability.
4. Evaluate access method.
5. Evaluate licensing/terms.
6. Evaluate point-in-time semantics.
7. Define validation and reconciliation checks.
8. Create the source record.
9. Mark source status.
10. Only then implement ingestion.

## 19. Candidate Source Categories

These are categories to investigate, not an approval list and not a claim that any specific provider has already been integrated.

- Indian regulatory and statutory disclosures.
- Stock-exchange disclosures and corporate filings.
- Company investor-relations disclosures.
- Official corporate-action information.
- Historical market-price/reference datasets.
- Fundamental/financial statement datasets.
- Insider/promoter/ownership disclosures.
- Credit-rating and regulatory event publications.
- Macroeconomic and government statistics.
- News/event sources, subject to licensing and reproducibility requirements.

## 20. Data-Source Directory Structure

- `docs/data-sources/README.md` — directory policy and index.
- `docs/data-sources/<source-id>.md` — one record per important source.
- `docs/data-sources/templates/source-record.md` — reusable template.
- `docs/data-sources/reviews/` — dated source reviews when needed.

Do not create one giant source document. Source-specific facts change at different rates and should be maintained independently.

## 21. Review Cadence

- Review a source before first production use.
- Re-review when terms, API behavior, coverage, or access conditions materially change.
- Re-review critical sources periodically.
- Record review date and reviewer.
- Deprecate sources rather than silently letting stale assumptions persist.

## 22. Relationship to Research Methodology

Methodology defines how evidence is analyzed; provenance defines what evidence was available, where it came from, and how it became an analytical input.

**Research validity chain:** `VALID SOURCE → CORRECT POINT-IN-TIME STATE → VALID TRANSFORMATION → VALID METHOD → TRANSPARENT RESULT`

## 23. Relationship to Technical Architecture

The technical architecture should support provenance as a first-class concern. Data models, ingestion jobs, storage, analytical outputs, and APIs should retain enough identifiers and metadata to trace important results.

## 24. Open Questions

- Which initial Indian sources provide the required first signal with acceptable historical depth?
- Which sources support genuine point-in-time reconstruction?
- What minimum provenance metadata must be stored for every dataset?
- Which data should be stored locally versus referenced externally?
- What automated reconciliation checks should be mandatory?
- How should source versions be represented?
- What source failures should block downstream research?

## 25. Initial Data-Governance Acceptance Criteria

- Every production data source has a documented source record.
- Source status and review date are explicit.
- Terms/licensing considerations are recorded.
- Historical coverage is documented.
- Point-in-time capability is documented.
- Important derived data can be traced to its source.
- Critical ingestion transformations are tested.
- Missingness and limitations are visible.
- No secrets or restricted datasets are committed.

## 26. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial data-source and provenance governance framework. |
