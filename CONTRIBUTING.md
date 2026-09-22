# Contributing to NewAngle

Thanks for your interest in NewAngle. This is an early-stage, solo-maintained, public open-source project. It is currently in **Phase 0 (repository foundation)** — see the README for current status.

This document describes how the project is developed. It applies equally to human contributors and to AI coding assistants working on the project.

## Project Principles

Before contributing, please read the guiding principles in the [README](README.md). The two most important, non-negotiable ones:

- **No fabricated data.** Never invent market data, events, sample sizes, sources, or results. If real data isn't available, label the gap explicitly (`DEMO`, `SYNTHETIC`, `PLACEHOLDER`, `UNVERIFIED`) rather than presenting something as real.
- **No unexplained claims.** Every research claim must be traceable to a source, date, and documented methodology. Association is not causation — historical relationships are described as historical relationships, not predictions or causal statements.

Contributions that violate these principles (e.g., adding an arbitrary "confidence score" with no defined methodology, or hard-coding plausible-looking sample data as if it were real) will not be merged.

## Scope Discipline

This project deliberately builds in small, validated, vertical slices rather than broad speculative functionality. Before proposing a new feature, dependency, dashboard, or infrastructure component, ask: *is this required for the current milestone?* If not, it belongs in an issue or `docs/roadmap.md` for later consideration, not in the current change.

Avoid introducing new infrastructure (databases, message queues, ML/NLP models, external services, etc.) unless a concrete, demonstrated requirement justifies it. Prefer boring, well-understood technology.

## Git Workflow

### Branching

```
main
feature/<short-description>
fix/<short-description>
docs/<short-description>
research/<short-description>
```

Examples: `feature/promoter-event-model`, `research/event-study-baseline`, `fix/event-date-validation`.

### Commits

One meaningful logical change = one meaningful commit. Do not manufacture commits to inflate history. Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(scope): short description
fix(scope): short description
docs(scope): short description
test(scope): short description
refactor(scope): short description
chore(scope): short description
research(scope): short description
```

Commits should be understandable to someone reading the repository six months from now.

### Pull Requests

Use PRs for substantial logical units of work (a schema, a connector, an API surface, a UI page, etc.). Small typo/config fixes can be committed directly where appropriate. For research-related changes, clearly document the methodology, validation performed, and relevant limitations in the PR description.

### Issues

Create issues for meaningful units of work, not for every minor task. Keep the issue tracker readable and purposeful.

## Testing

Every analytically important function needs tests, especially around: date handling, event detection, percentage/return calculations, missing data, event windows, benchmark alignment, corporate-action handling, point-in-time filtering, duplicate events, and invalid inputs. Research code should include small, deterministic fixtures — tests must not depend on live external data sources.

## Data & Research Standards

If your contribution touches data sourcing or research methodology:

- Document the source, access method, retrieval date, coverage, and any usage/redistribution restrictions.
- Respect point-in-time correctness — never use information that would not have been available at the analysis cutoff being studied.
- Document methodology decisions (event definitions, thresholds, statistical methods, benchmarks) and their rationale, including in a lightweight decision record under `docs/decisions/` for significant choices.
- Report inconclusive or negative results as-is. Do not adjust methodology until a desired result appears.

## Security

Do not commit secrets, credentials, or restricted third-party datasets. See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

By contributing, you agree your contributions will be licensed under the project's [MIT License](LICENSE). Note this applies to code only, not to any third-party data.
