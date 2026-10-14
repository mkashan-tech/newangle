# NewAngle — Project Charter / Bible

Document 01 · Version 1.0 · 28 September 2026

India-first market intelligence platform connecting numbers, people, events, and historical evidence to explain what matters.

## Document Status

- **Status:** Foundation document
- **Owner:** Mohammad Kashan
- **Authority:** Repository/code is authoritative for implementation; this charter records durable project intent and philosophy.
- **Evidence boundary:** Project claims, hypotheses, decisions, and current state are distinguished from externally verified research evidence.
- **Maintenance:** Update when identity, thesis, principles, scope boundaries, or major direction materially changes.

## 1. Executive Definition

NewAngle is an open-source, India-first market intelligence platform designed to connect market numbers with people, companies, events, and the wider context in which businesses operate. Its purpose is not simply to display more data, but to help users understand relationships between observed events, historical market behavior, evidence, uncertainty, and questions worth investigating.

> "Numbers tell you what happened. Context tells you why."

## 2. Why NewAngle Exists

The idea emerged from a desire to build a market-analysis system that does more than present price and fundamental numbers. Relevant information about management, corporate events, people, news, macro conditions, and historical behavior is often fragmented across different surfaces. NewAngle aims to connect those pieces into a research workflow where observations can be traced to evidence and tested against history:

- Observed event or change
- Entity and company identification
- Relevant context and relationships
- Historical evidence
- Statistical or event-study analysis
- Supporting and contradictory signals
- Uncertainty and limitations
- A research question or scenario worth investigating further

## 3. Origin and Evolution

NewAngle evolved from a personal concept for a share-market analyzer into a broader market-intelligence vision. Early exploration focused on combining quantitative market information with qualitative signals such as management changes, executive activity, corporate events, and wider macro or geopolitical context.

An AI-assisted Grok Build Agent prototype was created to explore product workflows and UI ideas. It remains a V0 product exploration, not a source of validated production data or empirical evidence.

Multiple AI systems were later used for brainstorming, critique, architecture discussion, and documentation. Those conversations are development inputs; they are not evidence by themselves. Durable decisions require human review and are recorded in project documentation.

## 4. Product Identity

NewAngle **is**:

- India-first market intelligence and research infrastructure.
- Evidence-oriented rather than narrative-first.
- Historical and context-aware rather than price-only.
- Designed to expose methodology, provenance, uncertainty, and limitations.
- Open source at the code level under the MIT License.
- Designed to grow from a narrow validated vertical into a broader intelligence platform.

NewAngle **is not**:

- A generic stock-price prediction project.
- A conventional news aggregator with a different interface.
- A black-box score generator that hides how conclusions were produced.
- A replacement for the user's own judgment or professional financial advice.
- A claim that historical relationships guarantee future outcomes.
- A license to redistribute third-party data merely because it is publicly accessible.
- A claim that future concepts already exist in the repository.

## 5. Long-Term Vision

The long-term vision is a research platform in which real-world events can be connected to companies, people, markets, industries, and broader systems, with important relationships supported by evidence.

**Conceptual flow:**

```text
REAL WORLD
  → PEOPLE / EVENTS / SYSTEMS
  → ENTITY RESOLUTION
  → CONTEXT / RELATIONSHIPS
  → NUMBERS + NARRATIVES + HISTORY
  → EVIDENCE
  → HISTORICAL EVENT STUDIES
  → CONTRADICTION ANALYSIS
  → IMPACT ANALYSIS
  → SCENARIOS
  → RESEARCH DESK
  → AI COPILOT
```

## 6. Core Principles

- **Evidence over storytelling** — Claims should be traceable to underlying observations and sources.
- **Show the work, not hidden reasoning** — Expose evidence, methodology, inputs, outputs, and limitations; never expose private model chain-of-thought.
- **Correlation is not causation** — Historical event studies should be described as associations unless stronger causal identification exists.
- **History is evidence, not destiny** — Historical patterns inform research; they do not guarantee future behavior.
- **No unexplained scores** — A score needs a justified definition and validation; visual certainty is not evidence.
- **Point-in-time discipline** — Historical research must respect what information was actually available at the analysis cutoff.
- **Negative results are valid** — Null or inconclusive findings should be preserved rather than hidden.
- **Provenance is part of the product** — Source, timing, method, and limitations are first-class information.
- **Research before scale** — A small reproducible pipeline is more valuable than a large architecture built on unvalidated assumptions.
- **Human judgment remains central** — NewAngle should improve research quality without pretending to make decisions for the user.

## 7. Research Philosophy

NewAngle should prefer transparent empirical methods over impressive-looking outputs. For event-driven questions, event studies are a starting framework for measuring historical relationships between defined events and subsequent market behavior.

Research outputs should make clear:

- Universe and selection rules
- Event definition and event date
- Information-availability timestamp where relevant
- Benchmark and return definition
- Estimation and event windows
- Sample size and exclusions
- Observed distribution, not only a single average
- Uncertainty and effect size where appropriate
- Treatment of missing data and corporate actions
- Potential look-ahead, survivorship, selection, and multiple-testing biases
- Regime differences and other relevant limitations
- Methodology version and reproducibility information

Specific windows, statistical tests, thresholds, or minimum sample sizes are methodological decisions to be validated and documented. They are not universal truths merely because they appeared in an early example.

## 8. Evidence and Provenance Standard

Important NewAngle claims should be auditable. A reviewer should be able to understand what was observed, where it came from, when it became available, how it was analyzed, and what limitations apply:

- Source identity and reference
- Retrieval/access date
- Publication or availability timestamp where applicable
- Underlying observation or dataset reference
- Methodology/version
- Sample size
- Benchmark/comparison basis
- Uncertainty and limitations
- Data licensing and redistribution status where relevant

Analytical surfaces should distinguish **OBSERVED**, **HISTORICAL RELATIONSHIP**, **MODEL OUTPUT**, **HYPOTHESIS**, **SCENARIO**, and **FORECAST**. These labels prevent evidence from being presented as certainty.

## 9. Initial Product Direction

The initial product direction is deliberately narrow: Indian listed companies and a small, well-defined research universe. Candidate research signals include promoter holding/pledge changes, insider transactions, bulk/block deals, auditor events, board/KMP changes, earnings or guidance changes, regulatory events, credit-rating actions, and related-party events.

These are candidate research areas, not a declaration that all are implemented or that any one signal has already been validated as predictive.

## 10. Deliberately Deferred

- Broad geopolitical and macro scenario engine as an initial production feature.
- Real-time tick-level market infrastructure.
- Custom large-language-model training.
- Advanced autonomous agents or reinforcement learning.
- Voice-based CEO/person confidence scoring.
- Knowledge-graph infrastructure before a demonstrated use case requires it.
- Microservices/Kubernetes/distributed infrastructure without demonstrated need.
- Generic stock-price prediction as the core value proposition.
- Direct buy/sell recommendation workflows.
- A large plugin marketplace.
- A large number of signals before the first research pipeline is validated.

## 11. UX Philosophy

- Serious research environment: dense but readable, restrained, transparent, and investigation-oriented.
- Dark-first is acceptable, but visual style must not imply false certainty.
- Avoid crypto-style neon aesthetics, excessive animation, decorative gradients, and gamified conviction meters.
- Make evidence and methodology discoverable from analytical surfaces.
- A company page should connect company facts, market context, events, historical evidence, and research paths.

## 12. Evidence Card — Target Pattern

A future evidence card may contain:

- Company and observed event
- Event date and information-availability timestamp
- Source(s)
- Historical sample size
- Benchmark and study window
- Mean/median abnormal return and distribution
- Uncertainty
- Careful interpretation
- Limitations and exclusions
- Methodology/version reference
- Data provenance

Any values used only as UI examples must be explicitly labeled **ILLUSTRATIVE** or **SYNTHETIC** and must never resemble real empirical results without that label.

## 13. Open-Source Philosophy

NewAngle's code is intended to be open source under the MIT License. Open source does not automatically grant rights to third-party datasets, websites, market feeds, filings, or other content. Data-source rights, terms, access methods, and redistribution conditions must be evaluated separately.

The project should never commit credentials, proprietary datasets, or restricted third-party data merely to make a demonstration convenient.

## 14. Development Philosophy

- Build milestone-by-milestone rather than attempting the entire vision at once.
- Use AI coding agents as implementation collaborators while keeping product and research ownership human-led.
- Prefer meaningful commits and coherent milestones over artificial commit-count targets.
- Review at research, architecture, data-validity, licensing, security, and other meaningful boundaries.
- Do not confuse a polished prototype with validated product capability.
- Document important decisions so future contributors do not need to reconstruct them from chat history.

## 15. AI Collaboration Philosophy

NewAngle is intentionally not dependent on one AI system. Different AI systems may be used for brainstorming, critique, research assistance, coding, documentation, or review. No AI system is automatically the authority.

The durable source of truth is the combination of project documentation, repository state, source-backed research, validated methodology, and explicit human decisions.

A new AI contributor should read the relevant project documentation before changing major architecture, methodology, data assumptions, or product scope.

## 16. Current State vs Target State

See the Change Log table in §20, and `docs/architecture/overview.md` in the repository, for the current engineering state. This charter records durable intent rather than tracking implementation status day to day.

## 17. Documentation Authority

- **README** — current public-facing project explanation.
- **Architecture docs** (`docs/architecture/`) — current and target technical design.
- **Methodology docs** (this foundation set, Document 03) — research definitions and validation procedures.
- **PRD/Roadmap** (this foundation set, Document 05) — product scope and sequencing.
- **ADRs/Decision Log** (`docs/decisions/` for engineering/schema decisions; this foundation set, Document 06, for product/process decisions) — important decisions and rationale.
- **Data-source docs** (`docs/data-sources/`, once populated) — source-specific provenance, coverage, rights, and limitations.
- **Repository/code/tests** — authority for what is actually implemented.
- **This charter** — durable project identity, intent, philosophy, and boundaries.

## 18. Durable North Star

```text
DATA → CONTEXT → RELATIONSHIPS → EVIDENCE → DECISION SUPPORT
```

NewAngle should become valuable not because it produces the loudest prediction, biggest score, or most features, but because it helps a researcher move from an observation to a defensible understanding of what happened, why it may matter, what historical evidence says, what contradicts that evidence, and what remains uncertain.

## 19. Open Questions

- Which initial research signal has the best combination of data availability, historical coverage, legal usability, and analytical validity?
- Which company universe should be used for the first production study, and how will survivorship bias be handled?
- Which event-study specification is appropriate for each signal and market regime?
- Which data providers/sources can be used under terms compatible with the open-source project?
- Which product workflow demonstrates real user value before broader platform expansion?

## 20. Change Log

### State Snapshot (as of this document's version)

| Area | Current / Verified | Target / Direction |
|---|---|---|
| Repository | Public GitHub repository; MIT license; foundation stage. | Professional application repository with tested product and research infrastructure. |
| Prototype | Prior AI-assisted V0 exists as product exploration; not production evidence. | Validated product experience backed by real, permitted data. |
| Backend | Not implemented in the foundation state. | FastAPI + SQLAlchemy + PostgreSQL, subject to documented implementation decisions. |
| Frontend | Not implemented in the foundation state. | Next.js + TypeScript + Tailwind, with research-oriented UX. |
| Analytics | Research design exists conceptually; no validated production event-study pipeline yet. | Reproducible historical event-study and evidence pipelines. |
| Data | Sources and rights require validation before production ingestion. | Point-in-time, provenance-aware, permitted data pipelines. |

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial consolidated Project Charter / Bible. Establishes identity, origin, principles, evidence boundaries, scope, current-vs-target distinction, and documentation authority. |
