# Foundation Documentation

This directory holds NewAngle's foundation document set: eight documents the project owner wrote to capture durable project identity, research philosophy, product direction, architecture intent, decisions, and governance — material meant to outlive any single chat conversation or contributor and let someone pick the project back up (or hand it to a new contributor, human or AI) without reconstructing context from scratch.

They were originally authored as `.docx` files and converted to Markdown here so they live and version alongside the code, rather than as a separate copy on Google Drive that could drift out of sync with the repository.

## Reading order

For a first read, or when onboarding a new contributor (human or AI), read in this order:

1. [`01-project-charter-bible.md`](01-project-charter-bible.md) — identity, origin, principles, vision, and scope boundaries.
2. [`02-product-user-research.md`](02-product-user-research.md) — target users, problem hypotheses, user stories, and what counts as evidence for product decisions.
3. [`03-research-methodology.md`](03-research-methodology.md) — how historical/analytical research should be designed, validated, and reported.
4. [`04-technical-architecture.md`](04-technical-architecture.md) — current vs. target system architecture.
5. [`05-prd-roadmap.md`](05-prd-roadmap.md) — MVP scope, milestones, and acceptance criteria.
6. [`06-decision-log-adrs.md`](06-decision-log-adrs.md) — product/process decisions and why they were made.
7. [`07-ai-contributor-handoff-guide.md`](07-ai-contributor-handoff-guide.md) — how an AI system or new contributor should approach working on the project.
8. [`08-data-sources-provenance.md`](08-data-sources-provenance.md) — how data sources should be evaluated, recorded, and governed.

## How this relates to the rest of `docs/`

This foundation set is deliberately broad and durable — it is about project intent, philosophy, and planning. It is not a substitute for the documentation that tracks actual implementation state:

- **`docs/architecture/overview.md`** is the authoritative, continuously-updated record of what is actually implemented, versus Document 04's broader architectural intent and reasoning. When the two disagree on current state, `docs/architecture/overview.md` wins.
- **`docs/decisions/001-*.md` and up** are engineering/schema-level ADRs (e.g. the Phase 1 data-model decisions). **Document 06 in this set** is a separate, product/process-level decision log using its own `ADR-001` and up numbering. Both are kept — see Document 01 §17 and Document 06's numbering note for how they relate. Neither numbering sequence should be merged into the other.
- **`docs/data-sources/`** (not yet populated) will hold the concrete, source-specific records that Document 08's governance framework calls for. Document 08 defines *how* to evaluate and record a source; the actual source records belong there, not in this foundation set.
- **Repository code and tests remain authoritative** for what is actually built, per Document 07 §4 (source-of-truth hierarchy).

## A note on currency

Documents 01, 02, 03, 07, and 08 needed no factual updates during this conversion — they are philosophy, research design, process guidance, and governance framework, none of which depended on implementation status. Documents 04, 05, and 06 originally described the project at the Phase 0 (foundation-only) stage; each was annotated during this conversion to reflect that the Phase 1 data model (`packages/data/`) is now implemented, with the original text preserved and the updates clearly marked inline rather than silently rewritten, consistent with this project's own principle that current state must be separated from target state (Document 06, ADR-010) and that documentation changes should be visible, not retroactive.
