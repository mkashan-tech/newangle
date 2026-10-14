# 002 — Provenance and Point-in-Time Timestamp Design

## Context

Principle 6 of the master brief requires that a historical analysis with
cutoff `T` never use information that became available after `T`
(`available_at <= analysis_cutoff`). Principle 8 requires every externally
sourced observation to carry documented provenance. The brief's original
conceptual schema listed `event_date`, `publication_date`, `available_at`,
`retrieved_at`, `source`, and `raw_reference` as the fields that matter —
but treated that list as a starting hypothesis to verify, not a fixed
design.

## Research Performed

Before finalizing these fields, I researched how Indian listed-company
disclosures actually work, specifically SEBI's Regulation 30 (LODR) and
Regulation 31 (SAST) disclosure timelines:

- Regulation 30 requires disclosure of board-decided material events
  within 30 minutes of the board meeting's closure, events originating
  within the company within 12 hours, and events originating outside the
  company within 24 hours of occurrence — timelines tightened by SEBI's
  2023/2024 amendments.
- Real BSE/NSE corporate announcements are timestamped to the minute
  (e.g. "announcement dated 29-01-2024 at 14:59 hours"), and that
  timestamp is legally significant — it is what the disclosure-timeline
  rules above are measured against.
- A real BSE example found during this research shows a company filing a
  "revised intimation" correcting an earlier announcement's stated
  compliance timeline, days after the original filing — i.e. corrections
  to already-published disclosures are a real, documented occurrence, not
  a hypothetical edge case.

This confirms two things the schema needed to take seriously: (1) the gap
between an event occurring and it becoming knowable is often measured in
hours, not days, so date-only granularity would be too coarse for
`available_at`; and (2) corrections/revisions to prior filings are real
and need a representable relationship, not just an implicit "latest row
wins" convention.

## Decision

Every provenance-bearing table (`CorporateEvent`,
`PromoterHoldingObservation`) carries four distinct temporal fields,
matching the brief's original hypothesis but with a materially different
justification for the precision of one of them:

| Field | Type | Meaning |
|---|---|---|
| `event_date` (events only) / `as_of_date` (holdings) | `DATE` | When the underlying fact occurred, or the date the figures describe. |
| `publication_date` | `DATE` | The date the source disclosed it. |
| `available_at` | `TIMESTAMPTZ` | The precise instant the information became knowable to a market participant. |
| `retrieved_at` | `TIMESTAMPTZ` | When NewAngle's (future) ingestion pipeline retrieved it. |

`available_at` is deliberately timestamp-precision, not date-precision,
because real exchange announcements are timestamped to the minute and
same-day announcements are common — a date-only field would make it
impossible to distinguish "available before market open" from "available
after market close," which matters for any future event-study work
against intraday or next-day price reactions. This is the one place this
schema diverges materially from treating the brief's original field list
as settled: it upgrades `available_at`'s precision based on verified
real-world disclosure behavior rather than assuming date-level
granularity was sufficient.

`retrieved_at` is kept distinct from the row's `created_at` bookkeeping
timestamp (see `models/base.py`) even though the two currently coincide
in practice (there is no ingestion pipeline yet in Phase 1) — see
`CreatedAtMixin`'s docstring for why they are expected to diverge once
backfills exist.

Every provenance-bearing row also carries `source_id` (required FK) and
`raw_reference` (nullable string pointer to the originating filing/
document at the source). A `(source_id, raw_reference)` unique constraint
prevents re-ingesting the identical filing twice, while still allowing
multiple rows from the same source with no captured reference (Postgres
treats `NULL` as distinct from `NULL` in unique constraints, which is the
correct semantics here — verified with a dedicated test,
`test_corporate_event_multiple_null_raw_references_allowed`).

## What Was Deliberately Deferred

- **Raw payload storage.** This schema stores a *reference* to raw
  source documents (`raw_reference`), not the documents themselves. No
  ingestion pipeline exists yet to produce raw payloads, so a
  raw-document-storage table would have nothing real to hold — building
  it now would be schema over-engineering ahead of demonstrated need
  (Section 39 of the master brief). It is deferred to Phase 2.
- **Database-level enforcement of `available_at >= publication_date`.**
  This invariant is enforced at the Pydantic input-validation layer
  (`schemas.py`), not as a Postgres `CHECK` constraint, because
  `available_at` is a `TIMESTAMPTZ` and `publication_date` is a `DATE`;
  a database-level check would require casting the timestamp to a date
  (`available_at::date >= publication_date`), and that cast's result
  depends on the database session's timezone setting — introducing a
  subtle, environment-dependent correctness risk for exactly the kind of
  invariant this project cares most about getting right. Enforcing it in
  the application layer, where the comparison is explicit and
  timezone-unambiguous (see `_check_date_ordering` /
  `_check_availability_ordering` in `schemas.py`), was judged the more
  conservative choice. This is a real trade-off, not an oversight — see
  the main Phase 1 report's "Potential Risks / Future Decisions" section
  for what would need to be true to revisit it.

## Consequences

- Point-in-time research queries filter on `available_at <= cutoff`,
  never on `event_date` or `publication_date` alone. This is directly
  exercised in `tests/test_point_in_time.py`, including a test that
  deliberately demonstrates the look-ahead-bias failure mode a naive
  `event_date`-only filter would produce.
- Any future ingestion connector must populate `available_at` from the
  source's actual disclosure timestamp, not derive it from
  `publication_date` at midnight — doing the latter would silently
  reintroduce the imprecision this design exists to avoid.
