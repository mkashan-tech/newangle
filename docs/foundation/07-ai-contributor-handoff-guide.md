# NewAngle — AI & Contributor Handoff Guide

Document 07 · Version 1.0 · 28 September 2026

How a new AI system or human contributor should understand, review, modify, and extend NewAngle

## Document Status

- **Status:** FOUNDATION HANDOFF GUIDE
- **Owner:** Mohammad Kashan
- **Purpose:** Provide a repeatable onboarding protocol for future AI systems and human contributors.
- **Authority:** Read this guide together with the current repository and the other NewAngle foundation documents.
- **Critical rule:** Do not assume that a concept described in future-facing documentation is implemented.

## 1. What NewAngle Is

NewAngle is an open-source, India-first market intelligence platform intended to connect numbers, people, companies, events, context, and historical evidence into an auditable research workflow.

**Core thesis:** Numbers tell you what happened. Context tells you why.

**North Star:** `DATA → CONTEXT → RELATIONSHIPS → EVIDENCE → DECISION SUPPORT`

## 2. First Rule for a New Contributor

Before writing code, first determine what is actually true about the current project. The repository, tests, source documentation, and accepted decision records take precedence over assumptions, old chats, prototype screenshots, or AI-generated suggestions.

- Inspect the repository.
- Read README and current contributor instructions.
- Read the relevant methodology and architecture documentation.
- Check current ADRs before changing a settled decision.
- Identify current milestone and scope.
- Run existing validation/tests before modifying behavior.
- Ask only when a decision materially affects methodology, data validity, licensing, security, or major architecture.

## 3. Required Reading Order

1. **01 — Project Charter / Bible** — understand identity, vision, principles, and boundaries.
2. **02 — Product & User Research** — understand users, problems, stories, and hypotheses.
3. **03 — Research Methodology** — understand what counts as valid analytical evidence.
4. **04 — Technical Architecture** — understand current/target system boundaries.
5. **05 — Product Requirements & Roadmap** — understand current milestone and scope.
6. **06 — Decision Log / ADRs** — understand why major choices were made.
7. **07 — This Handoff Guide** — understand how to work on the project.
8. **Data-source documentation** — read before implementing or changing ingestion.

## 4. Source-of-Truth Hierarchy

1. Current repository code and tests — what is actually implemented.
2. Current data-source/provenance records — what data can legitimately be used.
3. Accepted methodology and ADRs — current research/architecture decisions.
4. PRD and roadmap — intended product scope.
5. Project Charter — durable identity and philosophy.
6. Historical AI conversations — context and brainstorming only.
7. Unverified prototype behavior/screenshots — inspiration only.

## 5. Labels Contributors Must Respect

- **CURRENT STATE** — verified in the repository.
- **TARGET STATE** — intended future architecture/product direction.
- **DECISION** — intentionally adopted.
- **HYPOTHESIS** — not yet validated.
- **ILLUSTRATIVE / SYNTHETIC** — example only.
- **DEFERRED** — intentionally not being built now.
- **OPEN QUESTION** — unresolved.
- **OBSERVED** — source-backed fact.
- **HISTORICAL RELATIONSHIP** — empirical association from a defined study.
- **MODEL OUTPUT** — generated analytical result.
- **SCENARIO** — hypothetical pathway.
- **FORECAST** — only when a validated forecasting methodology exists.

## 6. How an AI Coding Agent Should Work

**Default operating mode: milestone-level autonomy.**

- Inspect the current repository before changing anything.
- Understand the complete current milestone.
- Implement the coherent milestone end-to-end where routine choices are clear.
- Do not stop for every file-level implementation decision.
- Stop and request human review when a choice materially changes research methodology, data validity, licensing, security, or major architecture.
- Run appropriate tests and validation.
- Inspect the final diff for accidental scope changes.
- Report assumptions, limitations, validation, and unresolved questions.
- Do not commit or push unless the project owner explicitly asks for it.

## 7. Recommended AI Task Brief

A future milestone prompt should communicate:

- Current milestone and exact scope.
- Relevant source documents.
- Explicit non-goals.
- Expected deliverables.
- Validation requirements.
- Stop conditions for high-impact decisions.
- Required final report.

## 8. Recommended AI Completion Report

- Completed
- Files Created/Modified
- Validation
- Important Decisions
- Assumptions
- Limitations
- Known Risks
- Proposed Commit
- Proposed PR
- Next Step

This keeps implementation progress separate from reasoning that needs later review.

## 9. Human Contributor Workflow

1. Choose an issue/milestone that is within current scope.
2. Read the relevant documentation.
3. Confirm source/data rights before adding external data.
4. Create a small, coherent implementation change.
5. Add/update tests.
6. Update documentation when behavior or decisions change.
7. Review the diff.
8. Open a focused PR with rationale, testing, and limitations.
9. Update or create an ADR if the change materially affects architecture/methodology.

## 10. When to Ask the Project Owner

Ask before proceeding when a decision could:

- Change the research question or event definition.
- Introduce a new source with uncertain rights.
- Change point-in-time semantics.
- Change the statistical methodology.
- Introduce a major dependency or infrastructure component.
- Expose sensitive information.
- Create a new public product claim.
- Expand scope beyond the current milestone.
- Turn a hypothesis into a permanent product assumption.

## 11. When Not to Ask

Do not interrupt for routine choices when the existing standards clearly determine the answer, such as:

- Formatting and naming consistent with the repository.
- Straightforward unit tests.
- Routine refactoring that preserves behavior.
- Normal error handling consistent with existing patterns.
- Documentation wording that does not change meaning.
- Small implementation details inside an already-approved design.

## 12. AI Research Rules

- Do not invent empirical market results.
- Do not invent sample sizes, confidence intervals, returns, study dates, or source citations.
- Do not treat another AI's statement as evidence.
- Use web/source research when current external facts are required.
- Keep sourced facts separate from model interpretation.
- Never hide uncertainty to make an answer sound stronger.
- Do not expose private model chain-of-thought.

## 13. Data and Source Rules

- Identify the authoritative source before implementing ingestion.
- Check historical coverage.
- Check access method and rate limits.
- Check terms/licensing and redistribution constraints.
- Record retrieval and availability timestamps where relevant.
- Do not commit secrets.
- Do not commit restricted datasets.
- Do not assume that publicly visible content is automatically redistributable.

## 14. Research Rules

- Start with a research question, not a desired chart.
- Define events operationally.
- Preserve information-availability timing.
- Define the universe and avoid survivorship leakage.
- Report N, distributions, uncertainty, benchmark, windows, and limitations.
- Do not claim causality from an event study alone.
- Record negative/inconclusive findings.
- Use sensitivity/robustness checks where appropriate.
- Version methodology changes.

## 15. Coding Rules

- Keep analytical logic independent from UI code.
- Keep ingestion logic separate from analytical transformations.
- Use typed schemas at application boundaries.
- Write tests for critical calculations.
- Prefer simple architecture until complexity is demonstrated.
- Keep configuration/secrets out of source control.
- Do not add infrastructure merely because it may be needed someday.

## 16. Git & Commit Philosophy

- Commit history should reflect meaningful project progress, not artificial activity.
- One coherent logical change may involve multiple files.
- Do not create commits solely to increase the count.
- Do not rewrite history to make AI-assisted work look manually typed.
- Commit messages should describe the actual change.
- Major methodology/architecture changes should reference the relevant ADR or documentation.

## 17. PR Expectations

- Clear title.
- Problem/context.
- What changed.
- Why it changed.
- Tests/validation performed.
- Data/source implications.
- Methodology implications.
- Known limitations.
- Documentation updated.
- Explicit note if the change affects a decision record.

## 18. Handling the V0 Prototype

The earlier AI-assisted V0 prototype is valuable as product exploration. It should not be treated as the production architecture, validated analytics, or evidence source.

- Preserve useful UX ideas.
- Do not import synthetic claims into production.
- Do not assume prototype modules must all be built.
- Use the PRD and validated user problems to decide what survives.

## 19. Scope-Drift Protection

If an implementation task starts expanding, classify the proposed work:

- Required for current milestone — proceed.
- Necessary dependency — document and proceed if low-risk.
- Research/architecture decision — pause and review.
- Future feature — record/defer.
- Nice-to-have — do not add unless milestone scope changes.

## 20. Handoff to a Completely New AI

A new AI system should be given the repository and this reading sequence rather than a giant conversational dump.

1. Start with README.
2. Read Documents 01–07 as needed.
3. Inspect repository state.
4. Check current milestone in the PRD.
5. Read relevant ADRs.
6. Read data-source records before touching ingestion.
7. Summarize current state and planned task before implementation.

## 21. Handoff Prompt Template

Suggested reusable opening instruction:

> "You are contributing to NewAngle. First inspect the repository and read the relevant project documentation. Treat repository state as authoritative for what exists, ADRs as authoritative for accepted decisions, methodology docs as authoritative for research standards, and source documentation as authoritative for data constraints. Do not assume future-state concepts are implemented. Work autonomously through the assigned milestone, but stop before making decisions that materially affect research methodology, data validity, licensing, security, or major architecture. Do not invent empirical evidence. Before finishing, run validation, inspect the diff, document assumptions and limitations, and report exactly what changed."

## 22. What a New Contributor Should Never Do

- Claim a prototype feature is production-ready without verification.
- Use synthetic data as real evidence.
- Scrape a source without checking its use constraints.
- Change a research definition silently.
- Introduce a major dependency without a reason.
- Add a broad feature because it appears in the long-term vision.
- Delete a negative research result because it looks unattractive.
- Turn an AI suggestion into a permanent decision without review.
- Expose private chain-of-thought as an evidence mechanism.

## 23. Handoff Checklist

- Repository inspected.
- README read.
- Current milestone identified.
- Relevant charter/product/methodology/architecture docs read.
- Relevant ADRs checked.
- Current tests/validation run.
- Data-source constraints checked.
- Current vs target state understood.
- Scope boundaries understood.
- Implementation plan summarized before major changes.

## 24. Open Handoff Improvements

- Add an automated repository health/status command.
- Add a machine-readable project metadata file if useful.
- Create issue/PR templates when contribution volume warrants them.
- Add a concise AI context file only if it reduces duplication without creating a second source of truth.

## 25. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 28 Sep 2026 | Initial AI and contributor handoff guide. Defines reading order, source-of-truth hierarchy, milestone-level autonomy, stop conditions, research/data rules, and reusable handoff protocol. |
