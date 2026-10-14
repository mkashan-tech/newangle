# 003 — Promoter Holding Observation Model

## Context

Section 7 of the master brief names promoter pledge/holding change as a
candidate first signal, but explicitly requires verifying — before
implementation — that the event definition is economically and
statistically sensible, and warns against blindly assuming a fixed
threshold like "pledge change > 1% = event."

Phase 1 does not implement event *detection* (that is future-signal work,
out of scope here per the brief). What Phase 1 needed to get right is the
**observation model**: a structure faithful enough to real disclosure
practice that a future event-detection layer can be built on top of it
without the underlying data model getting in the way or silently
misrepresenting what was actually disclosed.

## Research Performed

I researched SEBI (Substantial Acquisition of Shares and Takeovers)
Regulations, 2011 ("SAST Regulations"), Regulation 31, which governs
promoter shareholding/pledge disclosure, and found:

1. **Two distinct, non-interchangeable disclosure mechanisms exist:**
   - **Event-based** (Regulation 31(1)): filed when a pledge is created,
     revoked, or invoked — tied to a specific transaction date, disclosed
     within a matter of days of the transaction.
   - **Periodic** (Regulation 31(4)): filed alongside quarterly results,
     reporting promoter holding/pledge status as of quarter-end,
     regardless of whether anything changed since the prior quarter.

   Treating these as the same kind of row would let a research layer
   misinterpret "promoter re-filed the same unchanged pledge percentage
   this quarter" as "a new pledge event just happened" — exactly the
   kind of unsupported claim the project's research-honesty principles
   (Principle 2, Principle 5) rule out.

2. **Pledge percentage is disclosed on (at least) two different bases**
   in real filings: percentage of the promoter's *own* holding that is
   pledged, and percentage of the company's *total share capital* that is
   pledged. These are genuinely different numbers with different risk
   implications (a promoter with a small stake who has pledged all of it
   has a 100% pledged-of-holding figure but a small pledged-of-total-
   capital figure). A single ambiguous `pledged_pct` field would silently
   conflate them.

3. **Corrections happen.** A real BSE filing found during this research
   (Triveni Weglass Ltd., a "revised intimation" dated 04-05-2024,
   referencing and correcting an earlier 29-01-2024 announcement) shows
   that promoters/companies do file corrected versions of earlier
   disclosures. The schema needed a way to represent "this observation
   corrects an earlier one" without treating the correction as an
   unrelated duplicate or silently overwriting history.

4. **Not every filing discloses every figure.** Event-based filings
   sometimes report only share counts for the specific transaction, not
   a resulting total-holding percentage. This means percentage and count
   fields must be independently nullable — fabricating a missing figure
   to fill a NOT NULL column is disallowed by Principle 7 (no fabricated
   data).

## Decision

`PromoterHoldingObservation` models one disclosed observation, with:

- `observation_type` (`EVENT` | `PERIODIC`) distinguishing the two real
  disclosure mechanisms above, so a future signal-detection layer can
  choose to key off `EVENT` rows specifically (a genuine new pledge
  transaction) without being confused by an unchanged `PERIODIC` refiling.
- Split percentage fields: `pledged_pct_of_promoter_holding` and
  `pledged_pct_of_total_share_capital`, both independently nullable,
  rather than one ambiguous `pledged_pct`.
- `pledged_shares_count` and `total_promoter_shares_count` as separate,
  independently nullable share-count fields, allowing more precise
  figures to be captured when a filing reports counts rather than
  percentages.
- `corrects_observation_id`, a nullable self-referencing foreign key
  (`ON DELETE SET NULL`), modeling a revised intimation as a new row that
  points back to the observation it corrects — preserving both the
  original and the correction as distinct, individually-sourced rows,
  rather than mutating history in place.
- A `(source_id, raw_reference)` uniqueness constraint (not
  `(company_id, as_of_date, observation_type)`) as the duplicate-filing
  guard, because the natural real-world dedup key is "have we already
  ingested this specific filing," and using the filing reference directly
  avoids blocking legitimate same-day corrections or multiple genuinely
  distinct event-based filings that happen to share an `as_of_date`.

## What Was Deliberately Not Done

- **No `signals` or derived-conclusion table in Phase 1.** This
  observation model is the *normalized* layer (Section 7 scope item 8 of
  the Phase 1 task: signal records only if genuinely required at this
  stage). Detecting a "promoter pledge event" from these observations —
  including deciding on a threshold, and validating that the threshold is
  statistically sensible per the brief's Section 7 requirement — is
  explicitly future work (event detection, out of scope for Phase 1).
  Building a signals table now, with no detection logic to populate it,
  would be schema over-engineering ahead of demonstrated need.
- **No enforcement that `pledged_shares_count <= total_promoter_shares_count`
  at the database level.** Both are nullable `BIGINT` columns; a
  Postgres `CHECK` constraint comparing two nullable columns would
  silently pass whenever either is `NULL`, providing a weaker guarantee
  than intended. This invariant is enforced at the Pydantic
  input-validation layer instead (`schemas.py`,
  `_check_share_counts_consistent`) — see
  `test_promoter_holding_pledged_cannot_exceed_total_shares_is_app_level_not_db_level`
  in `test_models.py`, which documents this choice at the point a reader
  might otherwise expect a database constraint.

## Consequences

- A future event-detection component reads `EVENT`-type observations to
  find genuine new pledge transactions, and `PERIODIC` observations
  separately for point-in-time "what was the disclosed pledge status as
  of this quarter" queries — the two are never conflated by construction.
- Any research question involving pledge percentage must explicitly
  choose which basis (`of_promoter_holding` vs. `of_total_share_capital`)
  it means; the schema does not allow that ambiguity to be papered over.
