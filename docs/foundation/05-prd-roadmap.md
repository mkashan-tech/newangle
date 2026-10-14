# NewAngle — Product Requirements & Roadmap

Document 05 · Version 1.0 · 28 September 2026 (current-state note added for Phase 1 — see §7 and §13)

Product scope · MVP · Milestones · Acceptance criteria · Deferred direction

## Document Status

- **Status:** FOUNDATION PRD / ROADMAP
- **Owner:** Mohammad Kashan
- **Purpose:** Translate NewAngle's charter, user research hypotheses, methodology, and architecture into an implementation sequence.
- **Authority:** This document defines product intent and sequencing; the repository remains authoritative for implementation.
- **Planning rule:** Roadmap items are targets, not claims that functionality exists.

## 1. Product Objective

Build a narrow, reproducible research workflow that demonstrates NewAngle's core value before expanding into a broad market-intelligence platform.

**First product loop:** Company/event → evidence → historical analysis → interpretation with uncertainty → research next step.

## 2. MVP Definition

The MVP is not the entire NewAngle vision. It is the smallest credible system that can demonstrate the product thesis with real, permitted data.

- A clearly defined initial company universe.
- At least one validated research event/signal selected after source feasibility and methodology review.
- Permitted source ingestion with provenance.
- Point-in-time-aware event and observation model.
- Reproducible historical analysis.
- Evidence-oriented API output.
- A focused web workflow for company/event research.
- Tests covering critical calculations and data transformations.
- Documentation sufficient for another developer/researcher to understand the result.

## 3. MVP Non-Goals

- Full geopolitical intelligence platform.
- Full macroeconomic transmission engine.
- Real-time tick trading infrastructure.
- Generic stock-price prediction.
- Custom LLM training.
- Autonomous multi-agent research system.
- Voice/behavioral scoring of executives.
- Large knowledge graph infrastructure.
- Dozens of signals before the first one is validated.
- Personalized buy/sell recommendation engine.

## 4. Product Modules — Direction

| Module | Purpose | MVP? | Notes |
|---|---|---|---|
| Company Intelligence | Company identity, relevant observations, events, and research entry point. | YES | Keep focused; avoid dashboard overload. |
| Event Timeline | Chronological, source-backed corporate/market events. | YES | Point-in-time metadata is important. |
| Evidence / Research Result | Shows methodology, sample, distribution, uncertainty, and sources. | YES | Core differentiator. |
| Historical Pattern Study | Runs/reports the first validated event study. | YES | Signal chosen only after feasibility review. |
| Universe | Defines and exposes the research universe. | YES | Must handle historical membership appropriately. |
| Contradiction Engine | Surfaces materially diverging signals. | LATER | Needs multiple reliable signals. |
| Research Replay | Reconstructs what was knowable at historical cutoffs. | LATER | Data complexity is significant. |
| Impact / Transmission Map | Connects events across macro, sectors, and companies. | LATER | Requires broader context data. |
| Scenarios | Structured hypothetical pathways. | LATER | Must clearly distinguish scenarios from forecasts. |
| AI Copilot | Evidence-grounded research assistance. | LATER | Depends on trustworthy evidence layer. |
| Alerts | Event/research notifications. | LATER | Useful after core event pipeline is reliable. |

## 5. MVP User Journey

1. User selects or searches for a company.
2. User sees verified company identity and relevant source-backed events.
3. User opens a defined event.
4. System shows event date, availability timing, source, and context.
5. User opens the historical study.
6. System shows universe, event definition, benchmark, window, sample size, distribution, uncertainty, and limitations.
7. User can inspect methodology and provenance.
8. User can formulate the next research question without being given an unexplained recommendation.

## 6. MVP Acceptance Criteria

- Every displayed research result has a traceable methodology version.
- Event definitions are reproducible.
- Historical analysis respects the defined information cutoff.
- Critical calculations have automated tests.
- Data sources and redistribution status are documented.
- Synthetic/demo data is never represented as empirical evidence.
- Results expose sample size and relevant uncertainty/distribution.
- Causal language is avoided unless justified by the research design.
- Known limitations are visible to the user.
- The workflow can be reproduced from documented configuration/code where data rights permit.

## 7. Milestone Sequence

> **Updated for Phase 1.** The status lines for Milestone 0 and Milestone 1 below have been updated from the original document to reflect actual progress; the milestone content/scope itself is unchanged from the original.

### Milestone 0 — Repository Foundation

- README and project documentation foundation
- environment/config templates
- contribution/security guidance
- initial architecture/methodology documentation

**Status: COMPLETE.** Phase 0 was committed to the public repository (README, `.gitignore`, `.env.example`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/architecture/overview.md`).

### Milestone 1 — Data & Research Domain

- Select first research question/signal after feasibility review
- Define company/event/source domain model
- Design point-in-time fields
- Select and document initial permitted source(s)
- Create initial database schema and migrations
- Build source-backed fixtures/tests

**Exit condition:** The project can represent the chosen research question and its source data without methodological ambiguity.

**Status: SUBSTANTIALLY IN PROGRESS.** The domain model, point-in-time fields, database schema, and migrations have been implemented and tested in `packages/data` (companies, listed securities, sources, corporate events, and promoter holding observations — see `docs/decisions/001-003-*.md`). This covers the schema/migration portion of this milestone. Selecting and documenting the permitted initial data source(s), and the final feasibility-reviewed choice of first research signal, remain open — see Document 08 (Data Sources & Provenance) and §14 below.

### Milestone 2 — Ingestion & Normalization

- Implement permitted ingestion
- Normalize company/instrument/event identities
- Store provenance
- Validate completeness/duplicates/timestamps
- Create reproducible ingestion scripts

**Exit condition:** A clean, traceable analytical dataset can be produced from documented source inputs.

**Status: Not started.**

### Milestone 3 — First Historical Study

- Implement event definition
- Implement return/benchmark calculation
- Implement event-study analysis
- Add robustness/sensitivity checks
- Generate structured study results
- Test critical calculations

**Exit condition:** One complete historical study is reproducible and its limitations are documented.

**Status: Not started.**

### Milestone 4 — Evidence API

- Expose company/event/study endpoints
- Return provenance and methodology metadata
- Add validation/error states
- Document API contract
- Add API tests

**Exit condition:** The analytical result can be consumed reliably by a client without bypassing the evidence layer.

**Status: Not started.**

### Milestone 5 — MVP Web Experience

- Company research page
- Event timeline
- Evidence/result card
- Methodology/provenance view
- Clear loading/missing/stale states
- Basic responsive experience

**Exit condition:** A user can complete the core research journey end-to-end.

**Status: Not started.**

### Milestone 6 — Validation & Hardening

- Reproduce published study from clean environment
- Review bias controls
- Review source/licensing documentation
- Performance/security review appropriate to scope
- User/task testing
- Fix findings and document limitations

**Exit condition:** The MVP is defensible as a research prototype rather than merely a polished demo.

**Status: Not started.**

## 8. Post-MVP Direction

- Additional validated corporate/governance signals.
- Contradiction analysis across independent signal families.
- Research Replay / point-in-time reconstruction.
- Broader context and transmission relationships.
- Sector and macro impact analysis.
- Structured scenario analysis.
- Research Desk workflow.
- Evidence-grounded AI Copilot.
- Alerts and monitoring.

Expansion should occur only when each new layer has a clear user problem, data source, methodology, and validation path.

## 9. Feature Prioritization Rules

- Does the feature solve a documented user problem?
- Can its data be obtained and used legitimately?
- Can its output be evidenced?
- Can it be tested?
- Can it respect point-in-time constraints where relevant?
- Does it strengthen the core research loop?
- Does it introduce disproportionate architectural complexity?
- Can it wait until after the first validated vertical slice?

## 10. Definition of Done

A NewAngle feature is not complete merely because its UI works.

- Requirement/user problem is documented.
- Data source and rights are understood.
- Domain definition is explicit.
- Methodology is documented if analytical.
- Implementation is tested.
- Important edge cases are handled.
- Evidence/provenance is preserved.
- UI distinguishes data state from interpretation.
- Documentation is updated.
- Git diff and tests have been reviewed.

## 11. Product Quality Gates

- **Data validity gate** — Is the underlying data sufficiently reliable for the stated use?
- **Methodology gate** — Is the analytical definition defensible and reproducible?
- **Evidence gate** — Can important claims be traced to sources and inputs?
- **Bias gate** — Are major hindsight/selection/survivorship risks addressed?
- **Product gate** — Does the workflow solve the intended user problem?
- **Engineering gate** — Is the implementation tested and maintainable?
- **Scope gate** — Is this feature actually needed now?

## 12. Roadmap Boundaries

The roadmap must not be interpreted as a commitment to implement every future idea.

- Major features require an explicit product/research rationale.
- New infrastructure requires a demonstrated technical need.
- New signals require source and methodological feasibility.
- AI features require an evidence layer underneath them.
- Geopolitical/macro expansion requires dedicated source, entity, and transmission methodology.

## 13. Current Priority

> **Updated for Phase 1.** The original text ("complete the documentation foundation, then begin Milestone 1") is superseded by the status below, since both of those steps are now underway/complete.

Immediate priority: finish Milestone 1 by selecting and documenting the initial permitted data source(s) (Document 08 gives the governance framework; no specific provider has been evaluated or approved yet) and completing the feasibility review for the first research signal. Do not begin Milestone 2 (ingestion) before a source has passed that review, and do not begin broad feature development before the first research question, signal, source, and data model are reviewed together.

## 14. Open Product Questions

- Which user group should be the primary MVP user?
- Which first research signal best balances user value, data availability, historical depth, licensing, and analytical validity?
- What exact company universe should the first study use?
- What is the smallest company/event UI that demonstrates the thesis?
- Which metrics best validate whether the MVP is genuinely useful?

## 15. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial PRD and roadmap. Defines MVP, milestones, acceptance criteria, quality gates, and deferred product direction. |
| 1.0 (annotated) | — | §7 and §13 updated during conversion to Markdown to reflect that Milestone 0 is complete and Milestone 1's schema/migration work is substantially done. No other content changed. |
