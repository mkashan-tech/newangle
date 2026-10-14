# NewAngle — Decision Log & Architecture Decision Records

Document 06 · Version 1.0 · 28 September 2026 (current-state note added for Phase 1 — see §5)

Why decisions were made · What is settled · What remains open · How future decisions are recorded

## Document Status

- **Status:** FOUNDATION DECISION RECORD
- **Owner:** Mohammad Kashan
- **Purpose:** Preserve the reasoning behind durable NewAngle product, research, architecture, and development decisions.
- **Authority:** A decision record documents an intentional choice; repository state remains authoritative for implementation.
- **Update rule:** Material changes should create a new decision or supersede an existing one rather than silently rewriting history.

> **Note on numbering:** This document's ADRs (ADR-001 and up) are product/process decisions. They use a separate numbering sequence from the engineering/schema decision records in `docs/decisions/001-003-*.md` (which cover the Phase 1 data-model implementation specifically). Both are decision logs; neither supersedes the other. See Document 01 §17 for the documentation-authority breakdown.

## 1. Why a Decision Log Exists

NewAngle is being developed with substantial AI assistance and may involve multiple contributors and tools over time. Chat conversations are not a durable engineering record. This log preserves the decisions that materially shape the project, the alternatives considered, and the conditions under which a decision may need to change.

The goal is not to record every small implementation choice. Record decisions that affect product identity, research validity, architecture, data rights, security, scope, or long-term maintainability.

## 2. Decision Status Vocabulary

- **PROPOSED** — under discussion; not yet adopted.
- **ACCEPTED** — current project decision.
- **DEFERRED** — intentionally postponed.
- **REJECTED** — considered and not selected.
- **SUPERSEDED** — replaced by a later decision.
- **REVISIT** — accepted for now but explicitly scheduled for reconsideration when a condition occurs.

## 3. ADR Template

- ID and title
- Status
- Date
- Owner
- Context / problem
- Decision
- Alternatives considered
- Rationale
- Consequences
- Evidence / references
- Revisit trigger
- Supersedes / superseded by

## 4. Decision Records

### ADR-001 — NewAngle is India-first

- **Status:** ACCEPTED
- **Decision:** The initial product, research universe, data context, and workflows will be designed around Indian listed-company markets.
- **Rationale:** The project is intended to develop differentiated market-intelligence capability in a defined market context rather than attempting global coverage immediately.
- **Consequences:** Initial source research, entity handling, market calendars, corporate events, and UX can be optimized for India. India-first does not mean India-only forever.
- **Revisit trigger:** Expansion beyond India becomes justified by validated user demand, data feasibility, and research quality.

### ADR-002 — Evidence over unexplained scores

- **Status:** ACCEPTED
- **Decision:** NewAngle will prioritize observable evidence, methodology, distributions, uncertainty, and provenance over arbitrary composite scores.
- **Rationale:** A score without a defensible definition can create false precision and obscure the underlying evidence.
- **Consequences:** UI should expose the components and sources behind analytical outputs. Composite scores require explicit validation before introduction.
- **Revisit trigger:** A specific validated scoring problem is identified with a defensible methodology.

### ADR-003 — Event studies as an initial research framework

- **Status:** ACCEPTED AS A METHODOLOGICAL DIRECTION
- **Decision:** Historical event studies will be a major candidate framework for evaluating relationships between defined events and subsequent market behavior.
- **Rationale:** Event studies provide a transparent way to define an event, benchmark outcomes, specify windows, and report distributions.
- **Consequences:** NewAngle must define events, information timing, benchmarks, windows, samples, and limitations explicitly. Event studies do not automatically establish causality.
- **Revisit trigger:** A research question demonstrates that another methodology is more appropriate.

### ADR-004 — Point-in-time discipline

- **Status:** ACCEPTED
- **Decision:** Historical research must distinguish when an underlying value/event occurred from when information became publicly available.
- **Rationale:** Using information that became available only later creates hindsight/look-ahead bias.
- **Consequences:** Where relevant, the data model will preserve event/as-of/publication/availability/retrieval timestamps.
- **Revisit trigger:** Only methodological refinement; the principle itself is durable.

### ADR-005 — Small validated vertical slice before broad platform

- **Status:** ACCEPTED
- **Decision:** NewAngle will first build one complete research workflow rather than many partially implemented modules.
- **Rationale:** A reproducible end-to-end result is stronger evidence of product value than a large but unvalidated feature set.
- **Consequences:** Major features such as geopolitics, scenarios, copilot, and many signals remain deferred until the foundation works.
- **Revisit trigger:** The MVP demonstrates a stable research loop and expansion has a documented rationale.

### ADR-006 — Candidate signals are not permanently fixed

- **Status:** ACCEPTED
- **Decision:** Promoter pledge/holding changes, insider activity, bulk/block deals, auditor events, board/KMP changes, earnings/guidance, regulatory events, and similar signals remain candidate research areas until data and methodology feasibility are validated.
- **Rationale:** Choosing a signal solely because it sounds interesting can lead to poor data quality or weak research validity.
- **Consequences:** The first signal will be selected through a documented feasibility/research decision before implementation.
- **Revisit trigger:** Completion of the first data-source and research-feasibility review.

### ADR-007 — Open-source code does not imply open data rights

- **Status:** ACCEPTED
- **Decision:** NewAngle code can be open source under MIT, while third-party data remains subject to its own access, licensing, and redistribution terms.
- **Rationale:** Software licenses and data/content rights are separate questions.
- **Consequences:** Every production source requires provenance and rights documentation. Restricted data should not be committed merely for convenience.
- **Revisit trigger:** Review source-specific terms when providers or datasets change.

### ADR-008 — Human-owned, AI-assisted development

- **Status:** ACCEPTED
- **Decision:** AI systems may assist with research, critique, documentation, implementation, testing, and review, while product ownership, methodological accountability, and final decisions remain human-led.
- **Rationale:** NewAngle is intended to remain understandable and maintainable independent of any single AI tool.
- **Consequences:** Durable decisions must live in repository documentation rather than only in AI chat history.
- **Revisit trigger:** No scheduled revisit; workflow may evolve as tooling changes.

### ADR-009 — Milestone-level autonomy for coding agents

- **Status:** ACCEPTED
- **Decision:** AI coding agents should work autonomously through coherent milestones, stopping for decisions that materially affect research methodology, data validity, licensing, security, or major architecture.
- **Rationale:** Micro-managing every file reduces development efficiency, while unchecked whole-project generation increases risk.
- **Consequences:** Prompts should define milestone scope and a review gate. Commits should represent meaningful logical work, not artificial activity.
- **Revisit trigger:** If agent behavior repeatedly creates unacceptable scope or quality problems.

### ADR-010 — Current state must be separated from target state

- **Status:** ACCEPTED
- **Decision:** Documentation must clearly distinguish implemented functionality from planned architecture, hypotheses, and future concepts.
- **Rationale:** The old prototype and extensive future vision could otherwise make the repository appear more mature than it is.
- **Consequences:** Architecture, PRD, README, and handoff documents must use explicit current/target language.
- **Revisit trigger:** Durable documentation principle.

### ADR-011 — No generic stock-price prediction as core product

- **Status:** ACCEPTED
- **Decision:** Generic price prediction will not be the central value proposition of NewAngle.
- **Rationale:** The project's differentiation is contextual, evidence-oriented market intelligence rather than another black-box price forecast.
- **Consequences:** Research should focus on events, context, relationships, evidence, and historical behavior. Forecasting, if ever introduced, must be separately validated and labeled.
- **Revisit trigger:** A concrete research question demonstrates a defensible forecasting use case.

### ADR-012 — Defer distributed infrastructure until justified

- **Status:** ACCEPTED
- **Decision:** Kafka, Kubernetes, microservices, and similar infrastructure will not be introduced merely for architectural prestige or hypothetical scale.
- **Rationale:** Complex infrastructure creates operational cost and can distract from research validity.
- **Consequences:** Start with simple services/jobs and introduce distributed components when measured workload or reliability requirements justify them.
- **Revisit trigger:** Concrete performance, throughput, reliability, or team-boundary requirements.

### ADR-013 — Evidence graph over hidden AI reasoning

- **Status:** ACCEPTED AS PRODUCT DIRECTION
- **Decision:** NewAngle should expose source-backed evidence chains and analytical provenance rather than attempting to expose or reproduce an AI model's private chain-of-thought.
- **Rationale:** Users need auditable evidence, not hidden model reasoning.
- **Consequences:** AI features should link to evidence, methodology, and source material where possible.
- **Revisit trigger:** Refine implementation when AI workflows are designed.

### ADR-014 — Synthetic/demo data must be explicit

- **Status:** ACCEPTED
- **Decision:** Synthetic, illustrative, fixture, or placeholder data must be clearly labeled and separated from empirical production data.
- **Rationale:** The project has an existing V0 prototype and AI-generated examples; mixing these with research evidence would undermine trust.
- **Consequences:** UI, tests, documentation, and demos must prevent accidental misrepresentation.
- **Revisit trigger:** Durable principle.

### ADR-015 — Documentation is a durable project memory

- **Status:** ACCEPTED
- **Decision:** Major project context, decisions, methodology, architecture, and handoff knowledge should be preserved in versioned project documentation rather than relying on any single AI conversation.
- **Rationale:** AI access, tools, contributors, and personal memory can change over time.
- **Consequences:** Documentation is part of the product engineering system, not optional project notes.
- **Revisit trigger:** Documentation structure may evolve as the project grows.

## 5. Decisions Intentionally Still Open

> **Updated for Phase 1.** "Exact relational schema" has been removed from this list and annotated below, since it is now resolved for the domain covered by Phase 1. The remaining items are unchanged from the original document.

- First production signal.
- First authoritative data providers and exact access methods.
- Final company universe for the first study.
- Exact event-study model/window/benchmark for each event class.
- ~~Exact relational schema.~~ **Resolved for Phase 1 scope:** the schema covering companies, listed securities, sources, corporate events, and promoter holding observations is implemented and migration-backed in `packages/data`. See `docs/decisions/001-company-security-identity.md`, `002-provenance-and-point-in-time.md`, and `003-promoter-holding-observation-model.md` for the specific decisions and rationale. The schema may still extend to cover additional domain concepts (instruments beyond listed securities, people, signals, studies — see Document 04 §8) as later milestones require them; those extensions remain open.
- Whether Redis is necessary.
- Whether Kafka is necessary.
- Whether a knowledge graph is necessary.
- Cloud/deployment topology.
- Exact charting library.

## 6. Decision-Making Rules

- Prefer evidence over intuition when a decision affects research validity.
- Prefer the simplest solution that satisfies the requirement.
- Document material alternatives, not every trivial option.
- Do not treat AI consensus as empirical evidence.
- Do not freeze a future architecture merely because it sounds sophisticated.
- Record the decision before implementation when the decision materially changes architecture or methodology.
- Supersede decisions rather than silently rewriting history.

## 7. AI Collaboration History — How to Interpret It

NewAngle has used multiple AI systems for brainstorming and critique. Their outputs may contain useful ideas, but they should be treated as proposals. A future AI or contributor should rely on the accepted decisions and source-backed research in the repository rather than assuming that a previous AI recommendation is authoritative.

## 8. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial decision log consolidating durable product, methodology, open-source, AI-development, architecture, and scope decisions. |
| 1.0 (annotated) | — | §5 updated during conversion to Markdown to mark the relational-schema item resolved for Phase 1 scope, with cross-references to `docs/decisions/001-003-*.md`. A numbering cross-reference note was added after the Document Status block. No other content changed. |
