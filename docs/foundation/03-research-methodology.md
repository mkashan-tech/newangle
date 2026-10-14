# NewAngle — Research Methodology

Document 03 · Version 1.0 · 28 September 2026

Research design · Event studies · Point-in-time discipline · Bias controls · Evidence standards

## Document Status

- **Status:** FOUNDATION METHODOLOGY — RESEARCH DESIGN, NOT A CLAIM OF VALIDATED RESULTS
- **Owner:** Mohammad Kashan
- **Purpose:** Define the methodological standards NewAngle should follow before presenting historical analytical results as evidence.
- **Authority:** A concrete analysis must cite the methodology version and the actual data/source configuration used.
- **Important boundary:** This document defines principles and candidate methods. Exact parameters must be selected and justified for each research question.

## 1. Methodological Objective

NewAngle should answer clearly defined research questions using reproducible, point-in-time-aware evidence. The objective is not to manufacture predictive certainty. It is to quantify what happened historically under a defined event or condition, show the distribution of outcomes, and make limitations visible.

**Core principle:** A result is only as meaningful as its event definition, data timing, comparison framework, sample selection, and reproducibility.

## 2. Research Lifecycle

1. Define the research question.
2. Define the event or condition precisely.
3. Identify the eligible universe and point-in-time rules.
4. Identify authoritative data sources and licensing constraints.
5. Construct events without future information leakage.
6. Define benchmark, return measure, estimation period, event window, and exclusions.
7. Run the analysis reproducibly.
8. Perform robustness and bias checks.
9. Report distributions, uncertainty, sample size, and limitations.
10. Publish methodology/version and provenance.
11. Record negative or inconclusive results.

## 3. Research Question Before Feature

NewAngle should begin analytical work with a research question rather than with a desired product output.

**Illustrative question:** What historical market behavior followed defined changes in promoter pledge status for an explicitly defined universe, after accounting for the chosen benchmark and information-availability date?

The exact signal, universe, benchmark, and windows remain open until data feasibility and research design are validated.

## 4. Event Definition

An event must have an operational definition that can be applied consistently across observations:

- What constitutes an event?
- What date represents the economic event?
- What date represents public availability?
- What source establishes the event?
- How are revisions, corrections, duplicates, and conflicting disclosures handled?
- What observations are excluded and why?

Event date and information-availability date must not be casually treated as interchangeable.

## 5. Point-in-Time Discipline

Historical analysis must use only information that would have been available at the analysis cutoff.

- Store publication/availability timestamps where relevant.
- Use an explicit analysis cutoff.
- Enforce `availability_at <= analysis_cutoff` for information used in historical reconstruction.
- Do not silently use later corrections, classifications, survivorship lists, or derived labels unavailable at the time.
- Document revisions and whether the study uses current restated values or historical snapshots.

## 6. Universe Definition

The company universe must be defined independently of the outcome being studied. A current index constituent list must not automatically be treated as a historically valid universe.

- Record universe membership dates where relevant.
- Handle delisted, merged, suspended, renamed, and acquired companies explicitly.
- Avoid survivorship bias caused by selecting only companies that exist today.
- Document exchange, market, sector, capitalization, or other inclusion criteria.
- Version the universe definition used in each study.

## 7. Return and Benchmark Definitions

Market outcomes must be defined before analysis. Depending on the question, NewAngle may use simple returns, log returns, excess returns, or abnormal returns.

- Define price source and corporate-action treatment.
- Define the return interval explicitly.
- Define the benchmark explicitly.
- Consider sector or matched controls when scientifically appropriate.
- Document trading-day calendars and missing observations.

No benchmark is universally correct. The appropriate comparison depends on the event, universe, and research question.

## 8. Event-Study Framework

Event studies are a candidate core analytical framework for NewAngle's initial historical research. They estimate whether returns around defined events differ from an appropriate expected or benchmark return.

### 8.1 Candidate components

- **Estimation window** — a historical period used to estimate expected behavior, where applicable.
- **Event window** — the trading-day interval around the event used for measurement.
- **Abnormal return** — observed return minus the selected expected/benchmark return.
- **Cumulative abnormal return** — aggregation of abnormal returns over a defined event window.

These are methodological building blocks, not a fixed universal configuration. Window lengths and expected-return models must be justified for the specific event.

## 9. Candidate Analytical Models

- Market-adjusted return
- Market model
- Sector-adjusted comparison
- Matched-company or control-group comparison
- Other models where a research question genuinely requires them

NewAngle should prefer the simplest defensible model first. More complex models should be introduced only when they address a demonstrated limitation.

## 10. Statistical Reporting

NewAngle should avoid presenting a single average return or p-value as the complete result:

- Sample size (N)
- Mean and median where useful
- Dispersion such as standard deviation or interquartile range where appropriate
- Relevant quantiles or distribution visualization
- Effect size
- Confidence intervals or other uncertainty intervals when appropriate
- Statistical test and assumptions
- Benchmark/comparison definition
- Event and estimation windows
- Exclusions and missing-data treatment

Statistical significance does not automatically imply economic significance, causality, or future usefulness.

## 11. Multiple Testing and Researcher Degrees of Freedom

- Record major hypotheses and analysis choices.
- Separate exploratory analysis from confirmatory analysis.
- Use appropriate multiple-testing controls where applicable.
- Prefer out-of-sample or holdout validation for claims intended to generalize.
- Avoid selecting only the most favorable window or subgroup after seeing results.

## 12. Bias Controls

| Bias | Risk | Control direction |
|---|---|---|
| Look-ahead bias | Using information unavailable at the historical decision time. | Enforce information-availability cutoffs. |
| Survivorship bias | Studying only companies that survived to the present. | Use point-in-time universe membership and explicit treatment of exits. |
| Selection bias | Choosing events or companies because outcomes are already known. | Predefine selection rules where possible. |
| Data-snooping / multiple testing | Searching many configurations until one looks strong. | Record experiments and validate on held-out data. |
| Corporate-action bias | Ignoring splits, dividends, mergers, or adjustments. | Document price/return adjustment methodology. |
| Revision bias | Using later-restated information in historical reconstruction. | Track revisions and point-in-time availability. |
| Regime bias | Assuming relationships are stable across market regimes. | Report periods/regimes and test robustness where appropriate. |
| Missing-data bias | Ignoring systematic gaps in observations. | Report missingness and assess impact. |

## 13. Causal Language

Event studies can identify historical associations. They do not automatically establish that the event caused the observed market movement.

**Preferred language:**
- "Historically associated with…"
- "The event-study sample shows…"
- "Observed outcomes following the event were…"
- "The evidence is consistent with…"

**Avoid causal wording unless the research design genuinely supports it:**
- "The event caused the stock to fall…"
- "This signal guarantees…"
- "This proves the market will react…"

## 14. Robustness and Sensitivity Analysis

- Alternative reasonable event windows.
- Alternative benchmarks where justified.
- Subperiod or regime analysis.
- Alternative event definitions.
- Outlier sensitivity.
- Alternative inclusion/exclusion rules.
- Placebo or falsification tests where appropriate.

Sensitivity analysis should show whether a conclusion depends heavily on one arbitrary methodological choice.

## 15. Negative and Inconclusive Results

NewAngle should preserve results where the historical relationship is weak, inconsistent, statistically uncertain, or absent.

- Null results should remain discoverable.
- Inconclusive samples should not be converted into confident narratives.
- Unexpected findings should trigger investigation, not automatic rejection.
- Methodological failures should be documented when they teach something important.

## 16. Evidence Card — Required Research Fields

- Research question
- Event definition
- Universe
- Event date / availability date
- Data sources
- Analysis cutoff
- Benchmark
- Return definition
- Estimation window
- Event window
- Sample size
- Statistical method
- Observed result/distribution
- Uncertainty
- Robustness checks
- Known limitations
- Methodology version
- Data/provenance references

## 17. Reproducibility Standard

A published analytical result should be reproducible to the extent permitted by data licensing and source availability:

- Version-controlled code.
- Versioned methodology.
- Explicit configuration/parameters.
- Source and dataset references.
- Data retrieval/access timestamps.
- Deterministic or controlled random seeds where applicable.
- Tests for critical calculations.
- Documented environment/dependency versions where material.

If original data cannot legally or technically be redistributed, document the source, retrieval method, terms, transformation process, and reproducible procedure rather than committing restricted data.

## 18. Synthetic / Illustrative Data Policy

Synthetic data may be used for UI development, tests, and demonstrations. It must never be presented as observed market evidence.

- Label synthetic examples clearly.
- Do not invent empirical sample sizes, returns, confidence intervals, or study dates and present them as real.
- Keep demo data separate from production research datasets.
- Tests may use fixtures, but fixture values must not be mistaken for empirical findings.

## 19. Research Result Lifecycle

1. **HYPOTHESIS** — proposed question or relationship.
2. **EXPLORATORY** — initial investigation; not yet validated.
3. **REVIEWED** — methodology and data have been inspected.
4. **VALIDATED** — predefined validation criteria have been met for the stated scope.
5. **PUBLISHED** — reproducible result with evidence and limitations.
6. **SUPERSEDED** — replaced by a newer methodology/result.

A result's status must not be upgraded merely because an AI system, developer, or user believes it looks convincing.

## 20. Candidate First Research Study

The first production study should be selected only after data-source feasibility, historical coverage, event-definition quality, legal/redistribution considerations, and analytical design have been evaluated.

Candidate examples include promoter holding/pledge changes, insider transactions, bulk/block deals, auditor events, board/KMP changes, earnings/guidance events, regulatory events, and credit-rating actions. The project does not yet declare one as the permanent first signal. (Note: the Phase 1 data model's first fully-specified observation structure covers promoter holding/pledge disclosures — see `docs/decisions/003-promoter-holding-observation-model.md` — as a schema-readiness step, not as a declaration that this signal has been selected as the production signal.)

## 21. Research Review Checklist

- Is the research question explicit?
- Is the event definition deterministic enough to reproduce?
- Was information availability handled correctly?
- Is the universe defined without survivorship leakage?
- Are returns and benchmark definitions explicit?
- Are windows justified?
- Is N visible?
- Are distributions and uncertainty visible?
- Were important alternative specifications tested?
- Could multiple testing or data snooping explain the result?
- Are causal claims avoided?
- Are negative/inconclusive outcomes preserved?
- Can another researcher reproduce the analysis?
- Are source and licensing constraints documented?

## 22. Open Methodological Questions

- Which event-study specification should be the default for each event class?
- How should NewAngle handle overlapping events?
- How should clustered events for the same company be treated?
- What is the appropriate control/benchmark for each signal?
- How should delisted securities and corporate actions be represented?
- Which validation protocol is appropriate for exploratory versus confirmatory research?
- How should methodology changes affect comparability between old and new results?

## 23. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial methodology foundation covering research lifecycle, event studies, point-in-time discipline, statistical reporting, bias controls, reproducibility, and evidence standards. |
