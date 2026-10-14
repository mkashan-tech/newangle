# NewAngle — Product & User Research

Document 02 · Version 1.0 · 28 September 2026

Users · Problems · User Stories · Scenarios · Assumptions · Validation

## Document Status

- **Status:** FOUNDATION / HYPOTHESIS DOCUMENT
- **Owner:** Mohammad Kashan
- **Evidence status:** Most user/persona material in this first version is a product hypothesis derived from the NewAngle concept and design discussions, not validated user research.
- **Important rule:** Hypotheses must not be presented as measured market facts. Interview findings, analytics, or other evidence can upgrade them later.
- **Related document:** Document 01 — Project Charter / Bible

## 1. Purpose

This document defines who NewAngle is intended to help, the research problems it is intended to address, the workflows users may need, and the assumptions that must be validated before major product commitments.

It is intentionally a living research document. It does not claim that the personas, pain points, or feature priorities below have already been proven through a formal user study.

## 2. Product Problem Statement

Market research can require combining numerical market data, company information, corporate events, management signals, external context, historical behavior, and source documents. These pieces may be difficult to connect into one auditable research path.

**Working problem hypothesis:** Researchers need a way to move from an observed market/company event to relevant context and historical evidence without losing provenance, timing, methodology, or uncertainty.

## 3. Target User Groups

NewAngle initially considers three broad user groups. These are working hypotheses, not confirmed personas.

### 3.1 Individual Market Researcher / Investor

- **Job to be done:** Investigate a company or event and understand the evidence and historical context around it.
- **Likely needs:** Company intelligence, event timelines, historical relationships, source evidence, comparisons, and research trails.
- **Potential frustration:** Relevant information may be fragmented and require manual cross-checking.
- **Validation needed:** Interviews or observed workflows should establish which research tasks are genuinely frequent and costly.

### 3.2 Student / Academic / Independent Researcher

- **Job to be done:** Explore market questions and reproduce or understand analyses without relying on unexplained conclusions.
- **Likely needs:** Transparent methodology, datasets or references where permitted, notebooks/research outputs, historical studies, and explanations.
- **Potential frustration:** Financial datasets and analytical conclusions can be difficult to reproduce or interpret.
- **Validation needed:** Determine whether students primarily need education, data access, research tooling, or finished analysis.

### 3.3 Developer / Data Scientist / Open-Source Contributor

- **Job to be done:** Use, inspect, extend, or contribute to NewAngle's data, analytics, and product infrastructure.
- **Likely needs:** Clear architecture, reproducible pipelines, source provenance, contribution guidance, tests, and documented decisions.
- **Potential frustration:** AI-generated or rapidly evolving projects can become difficult to understand without durable documentation.
- **Validation needed:** Observe what information new contributors actually require to make a first meaningful contribution.

## 4. Core User Problems — Working Hypotheses

- **P1 — Fragmented context** — A user may need to move among prices, filings, corporate events, management information, news, and broader context to investigate one question.
  *Potential impact:* Research may become slower and harder to audit. *Validation:* Validate through interviews and task observation.
- **P2 — Historical evidence is difficult to connect** — A user may see an event but not have an easy way to investigate how similar events behaved historically.
  *Potential impact:* Users may rely on anecdotes or manually repeat analysis. *Validation:* Validate by observing how users perform historical event research.
- **P3 — Evidence and conclusions can become disconnected** — A chart or AI-generated explanation may not make its sources, timing, sample, or methodology obvious.
  *Potential impact:* Users may struggle to distinguish observation from interpretation. *Validation:* Validate by testing evidence-oriented prototypes.
- **P4 — Conflicting signals are hard to organize** — Fundamentals, management activity, insider activity, price behavior, and external events can point in different directions.
  *Potential impact:* The user may need to manually build a mental model of the contradiction. *Validation:* Validate whether a structured contradiction view improves research.
- **P5 — Reproducibility is difficult** — A research result can depend on data versions, event definitions, timestamps, and analysis choices that are not recorded.
  *Potential impact:* A later user may be unable to reproduce the result. *Validation:* Validate which provenance metadata users actually need.

## 5. User Stories

The stories below describe desired capabilities, not already-built functionality.

- **US-01 — Company investigation.** As a researcher, I want to inspect a company's important events alongside market and company information so that I can form a contextual research question. *Acceptance direction:* Company identity, timeline, sources, and relevant observations are clearly separated from interpretation.
- **US-02 — Event investigation.** As a researcher, I want to open a specific corporate event and see when it occurred and when information became available so that I can avoid accidental look-ahead. *Acceptance direction:* Event date, publication/availability timestamp, source, and provenance are visible.
- **US-03 — Historical comparison.** As a researcher, I want to examine historical instances of a defined event so that I can understand the distribution of subsequent market behavior. *Acceptance direction:* Event definition, selection rules, sample, benchmark, window, and results are disclosed.
- **US-04 — Evidence inspection.** As a researcher, I want to trace an analytical claim back to its source and underlying observation so that I can judge its reliability. *Acceptance direction:* Claim has source/reference and relevant methodology/provenance.
- **US-05 — Contradiction investigation.** As a researcher, I want to see when major signals disagree so that I know where further investigation may be warranted. *Acceptance direction:* Conflicting observations are shown without converting disagreement into an arbitrary score.
- **US-06 — Point-in-time research.** As a researcher, I want historical analysis to use only information available at the selected cutoff so that the result is not contaminated by future information. *Acceptance direction:* Availability cutoff is explicit and enforced where relevant.
- **US-07 — Methodology review.** As a researcher, I want to inspect how a result was calculated so that I can reproduce or challenge it. *Acceptance direction:* Method/version and key parameters are accessible.
- **US-08 — Research replay.** As a researcher, I want to reconstruct what was knowable at an earlier point in time so that I can evaluate historical reasoning without hindsight. *Acceptance direction:* Historical information state and cutoff are preserved.
- **US-09 — Contributor onboarding.** As a developer, I want clear project documentation and tests so that I can understand where a change belongs and contribute safely. *Acceptance direction:* Current architecture, contribution rules, tests, and decision records are available.
- **US-10 — AI-assisted research.** As a researcher, I want AI assistance to summarize and connect evidence while clearly separating sourced observations from generated interpretation. *Acceptance direction:* AI output cites evidence and exposes uncertainty instead of presenting unsupported certainty.

## 6. User Scenarios

### 6.1 Investigating an Unusual Corporate Event

A researcher notices a material corporate event. Instead of immediately interpreting it, they open the company, verify the event date and information-availability timestamp, inspect the source, review comparable historical events, and examine the observed market distribution around those events. NewAngle surfaces limitations and contradictory evidence before the researcher forms a conclusion.

### 6.2 Researching a Conflicting Signal

A researcher finds positive operational information while another signal appears negative. NewAngle presents the observations separately, shows their sources and dates, and provides historical research paths. The product does not collapse the conflict into a single unexplained conviction score.

### 6.3 Reproducing a Historical Study

A student or developer wants to understand a published NewAngle analysis. They inspect the event definition, universe, cutoff, benchmark, windows, exclusions, data references, methodology version, and tests. They can re-run or challenge the analysis where the data and licensing permit.

## 7. Product Jobs-to-be-Done

- Understand what changed.
- Understand when the information became knowable.
- Understand what context surrounds the change.
- Find comparable historical events.
- Measure what happened historically after those events.
- Inspect contradictory evidence.
- Understand how an analytical result was produced.
- Decide what deserves deeper research next.

## 8. Assumptions to Validate

- **A1** — Users value connected context more than another conventional screener. *Validation route:* Interview/task evidence.
- **A2** — Historical event studies can provide useful research value when carefully defined. *Validation route:* Reproducible studies + user testing.
- **A3** — Evidence/provenance increases trust and research quality. *Validation route:* Prototype usability/research comparison.
- **A4** — Users want contradictions surfaced rather than hidden inside a single score. *Validation route:* Workflow interviews + prototype testing.
- **A5** — Point-in-time reconstruction is valuable enough to justify its data complexity. *Validation route:* Research interviews + feasibility assessment.
- **A6** — A small set of high-quality signals is more useful initially than a large collection of weak signals. *Validation route:* Usage and research outcomes.
- **A7** — Open-source transparency can attract technically capable contributors. *Validation route:* Repository/contributor observation.

## 9. Feature Prioritization Logic

Features should not be prioritized merely because they are visually impressive or technically interesting. A feature should earn priority by connecting to a validated user problem and a defensible research capability.

- **High priority candidate:** company/event → evidence → historical study workflow.
- **High priority candidate:** provenance and point-in-time metadata.
- **High priority candidate:** methodology/evidence presentation.
- **Potential later priority:** contradiction engine after signal definitions exist.
- **Potential later priority:** research replay after historical data infrastructure is mature.
- **Deferred:** broad AI copilot before reliable evidence and data foundations exist.

## 10. Validation Plan

- Conduct semi-structured interviews with potential users rather than asking only whether they "like" the concept.
- Observe users completing real research tasks where possible.
- Record exact workflows, repeated manual steps, sources used, and points of uncertainty.
- Separate stated preferences from observed behavior.
- Prototype one narrow evidence-to-historical-study workflow and test it.
- Measure task completion, time/effort, comprehension, reproducibility, and user-reported usefulness.
- Record negative findings and rejected assumptions.

## 11. Research Interview Guide — Initial

- Tell me about the last time you investigated a company or market event in depth.
- What triggered the investigation?
- Which sources or tools did you use?
- What information was hardest to connect?
- How did you determine whether a claim or signal was trustworthy?
- Did you look for historical examples? If yes, how?
- How did you handle conflicting information?
- What part of the process was most repetitive?
- What would you want an ideal research tool to show you?
- What would make you distrust an analytical result?
- Which information must always show its source or timestamp?
- Would you want to reproduce or inspect the underlying methodology? Why?

## 12. What Counts as Evidence

This document currently contains product hypotheses. The following evidence can upgrade a hypothesis into a stronger product finding:

- Direct user interview statements, with date and participant context.
- Observed user behavior during a real task.
- Repeated patterns across independent users.
- Usage analytics from a functioning prototype, with appropriate interpretation.
- Research or literature relevant to the specific workflow.
- Validated technical or empirical experiments.

A single positive conversation, AI opinion, or imagined persona is **not** sufficient evidence of product-market need.

## 13. Personas: Evidence Status

The three user groups in this document are provisional archetypes. They are intentionally broad and do not contain invented demographic details, portfolio sizes, income, or behavior presented as facts. If interviews establish specific personas later, those details should be added with evidence and dates.

## 14. Product Boundaries Derived from User Research

- Do not optimize for prediction accuracy before defining a valid research question.
- Do not hide source quality or methodology behind an AI-generated summary.
- Do not create a "conviction" number simply because users find scores attractive.
- Do not turn a hypothetical scenario into a factual market claim.
- Do not expand into many signals before the first workflow proves useful and reproducible.

## 15. Open Questions

- Who is the first user NewAngle should optimize for?
- Which research task is painful enough that users will return for it?
- Which candidate event/signal has the best data and user value?
- How much historical context do users actually need on a company page?
- Do users prefer a guided research workflow, a flexible research desk, or both?
- Which provenance details materially improve trust without overwhelming the interface?
- What would make an open-source researcher contribute rather than simply use the product?

## 16. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial Product & User Research document. Converts earlier persona, pain-point, user-story and scenario ideas into an evidence-aware hypothesis framework. |
