# NewAngle

**NewAngle is an open-source, India-first market intelligence platform for Indian listed companies, currently in early foundational development.**

Traditional market tools tend to answer *"what happened to this stock?"* NewAngle's long-term goal is to investigate a broader question: *"what happened around this company and the wider world, what relationships may matter, what evidence supports them, what happened in comparable historical situations, and what should a researcher look into next?"*

## Current Status

**This project is in Phase 1 (data model). There is no working application yet.**

As of now, the repository contains:
- Project documentation and contribution guidelines
- Architecture documentation describing the system design, current and intended
- A tested, migration-backed PostgreSQL schema (`packages/data/`) for companies, listed securities, sources, corporate events, and promoter holding observations — with point-in-time and provenance fields, but no data in it

The repository does **not** yet contain:
- Any data ingestion or connectors to real data sources — the schema above is empty; nothing populates it yet
- Any signal-detection, event-study, or analytics logic
- An API
- A frontend/UI
- Any validated research results

**No functionality described elsewhere in this README (or in the long-term vision below) is currently implemented, tested, or backed by real data**, beyond the schema itself described above. Anything not explicitly listed under "Current Status" should be treated as a future goal, not a present capability.

## Core Idea

> Numbers tell you what happened. Context tells you why.

NewAngle's intended niche is connecting market numbers, company fundamentals, corporate/governance events, and historical evidence, and presenting the resulting research with an explicit, auditable evidence trail — sources, dates, methodology, sample sizes, and stated limitations — rather than unexplained scores or unsupported causal claims.

NewAngle is **not** intended to become:
- a buy/sell recommendation engine
- an unexplained stock-prediction model
- a generic news aggregator or chatbot
- a source of AI-generated claims without traceable evidence

## Long-Term Vision (Not Yet Built)

The eventual, much larger vision is to connect world events → people/organizations → companies → markets/macro → historical evidence → impact analysis → scenarios, so that a user researching a company can see not just price movement but the context and historical precedent around it.

This vision exists to guide architecture decisions over time. It is **not** the current scope, and most of it may never be built if evidence doesn't support that it's useful. Development proceeds as small, validated, vertical slices — starting with one real signal, one real data pipeline, one validated research method, and one usable page — rather than building broad, unvalidated functionality up front.

## Guiding Principles

These principles govern all development on this project:

- **Evidence over storytelling.** Claims must be traceable to source, date, data, and methodology.
- **No unexplained scores.** No arbitrary composite numbers ("Confidence: 84/100") without a documented, validated methodology.
- **Association is not causation.** Historical relationships are described as historical relationships, not guarantees or causal claims.
- **Point-in-time correctness.** Research must only use information that was actually available at the time being analyzed.
- **No fabricated data.** Anything synthetic, placeholder, or unverified is labeled as such and never presented as empirical evidence.
- **Simple architecture first.** No infrastructure (Kubernetes, Kafka, vector databases, custom LLM training, etc.) is introduced without a demonstrated, concrete need.

See `CONTRIBUTING.md` for how these principles apply to contributions, and `docs/architecture/overview.md` for the intended system design.

## Status of AI Involvement

Parts of this project's early development are assisted by an AI coding agent working from a detailed project brief. All research logic, data claims, and methodology decisions are subject to the same evidence and provenance standards described above regardless of whether they originate from a human contributor or an AI assistant. Nothing labeled elsewhere in this repository as "current status" reflects unreviewed AI-generated content.

## License

Code in this repository is licensed under the [MIT License](LICENSE). Note that the MIT license applies to the code only — it does not grant rights to redistribute any third-party data that may later be used by this project. Data provenance and licensing will be documented separately under `docs/data-sources/` once real data connectors exist.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md) for how to report vulnerabilities.
