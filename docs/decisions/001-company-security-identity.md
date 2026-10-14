# 001 — Company vs. Listed-Security Identity

## Context

The master brief warns against assuming a ticker/symbol is a permanent
company identity, and asks for explicit reasoning about company/entity
identity vs. listed-security identity, exchange identity, and symbol
changes.

Indian listed companies can, and do, rename, demerge, and change their
trading symbol on NSE and/or BSE while remaining the same legal entity.
A schema that used `(exchange, symbol)` as the primary identity for a
company would silently break the moment a symbol changed, since any
prior events/observations tied to the old symbol would no longer be
associated with anything.

## Options Considered

1. **Single `companies` table keyed by symbol.** Simplest, but conflates
   entity identity with a mutable trading label. Rejected — breaks on
   any symbol change, demerger, or dual listing.
2. **Company + ListedSecurity, security identity anchored on symbol
   alone.** Better, but still doesn't distinguish a security's stable
   identifier (ISIN) from its current label (symbol).
3. **Company + ListedSecurity with effective-dated symbol and required
   ISIN, `Exchange` modeled as a small enum.** Chosen.

## Decision

- `Company` is the entity-identity table. It carries `cin` (India's MCA
  Corporate Identity Number) as a nullable-but-unique field — nullable
  because NewAngle may register a company before its CIN is confirmed
  from an authoritative source (fabricating one is disallowed), unique
  because, when known, it is a genuinely stable government identifier.
- `ListedSecurity` represents one company's listing on one exchange
  under one symbol, for one effective period (`effective_from` /
  `effective_to`, with `NULL` `effective_to` meaning "currently
  active"). A symbol change is represented as closing the old row and
  opening a new one, not as an update-in-place, so historical events
  tied to the old symbol's effective period remain resolvable.
- `isin` is required on `ListedSecurity` (a real, tradeable Indian
  security has one by definition) but is **not** globally unique at the
  database level, because the same equity class commonly carries the
  same ISIN across multiple exchange listings (e.g. NSE and BSE under
  different symbols). A global uniqueness constraint here would be
  factually wrong, not just overly strict — an earlier draft of this
  schema had this bug; it was caught during Phase 1 review before the
  migration was applied.
- `Exchange` (NSE, BSE) is modeled as a small enum, not a lookup table.
  The set is small, well-known, and not expected to change often for an
  initial India-equities research universe. If a future requirement
  needs richer exchange metadata or more exchanges, this can be migrated
  to a proper table — that migration is deferred, not avoided, per
  Principle 9 (simple architecture first).
- At most one `ListedSecurity` row per `(company_id, exchange)` should
  have `effective_to IS NULL` at a time. This is enforced procedurally
  (application code + `test_listed_security_symbol_change_over_time` /
  related tests) rather than with a Postgres partial unique index in
  Phase 1, since enforcing it correctly at the database level also
  requires deciding what happens during the moment a symbol-change
  transaction is being written (old row closed, new row opened,
  atomically) — a genuine design question better addressed once an
  ingestion pipeline actually performs that write, rather than guessed
  at now.

## Consequences

- Events and observations reference `company_id` directly (the stable
  entity), not a `(exchange, symbol)` pair, so they remain valid across
  symbol changes.
- Building "what was this company's symbol on NSE on date X" requires a
  point-in-time query against `ListedSecurity.effective_from` /
  `effective_to`, not a simple lookup — this is intentional and consistent
  with the project's broader point-in-time discipline (see
  002-provenance-and-point-in-time.md).
- The partial-unique-index enforcement gap (previous bullet) is a known,
  documented limitation, not an oversight — see the main Phase 1 report's
  "Potential Risks / Future Decisions" section.
