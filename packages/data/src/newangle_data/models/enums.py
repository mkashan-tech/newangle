"""Shared enumerations for the NewAngle data model.

Each enum here is deliberately small and bounded. Where a concept is open-
ended or likely to grow in ways we can't predict yet (e.g. `event_type` on
CorporateEvent), it is modeled as a plain, documented string column instead
of an enum, per the master brief's instruction not to hard-code event
taxonomies prematurely (Section 7 / Section 38).
"""

from __future__ import annotations

import enum


class Exchange(enum.StrEnum):
    """Primary Indian stock exchanges.

    Modeled as an enum rather than a lookup table: the set of exchanges
    relevant to an initial India-listed-equity research universe is small,
    well-known, and not expected to change often. If a project requirement
    later demonstrates a need for a richer exchange model (e.g. exchange
    metadata, additional exchanges, or foreign listings), this can be
    migrated to a proper `exchanges` table — see
    docs/decisions/001-company-security-identity.md.
    """

    NSE = "NSE"
    BSE = "BSE"


class SourceType(enum.StrEnum):
    """Broad category of an information source.

    Kept intentionally coarse. Fine-grained distinctions (e.g. "NSE
    corporate announcement" vs "NSE circular") belong on `Source.name` /
    `Source.url`, not in this enum, since the enum exists only to support
    coarse filtering and validation, not to model exchange-specific
    taxonomy.
    """

    EXCHANGE_FILING = "EXCHANGE_FILING"
    REGULATORY_FILING = "REGULATORY_FILING"
    COMPANY_DISCLOSURE = "COMPANY_DISCLOSURE"
    NEWS = "NEWS"
    OTHER = "OTHER"


class PromoterHoldingObservationType(enum.StrEnum):
    """Distinguishes the two real, distinct disclosure mechanisms for
    promoter shareholding/pledge data under SEBI (SAST) Regulations, 2011.

    - EVENT: a transaction-triggered disclosure under Regulation 31(1),
      filed when a pledge is created, revoked, or invoked. Tied to a
      specific transaction date.
    - PERIODIC: a periodic disclosure under Regulation 31(4), filed
      alongside quarterly results, reporting promoter holding/pledge
      status as of a quarter-end date regardless of whether anything
      changed.

    These are not interchangeable: an EVENT row reflects a specific
    pledge transaction; a PERIODIC row is a point-in-time snapshot that
    may repeat an unchanged pledge percentage quarter after quarter.
    Conflating them would misrepresent "no new disclosure this quarter"
    as "a new pledge event," which is exactly the kind of unsupported
    claim the project's research-honesty principles rule out. See
    docs/decisions/003-promoter-holding-observation-model.md.
    """

    EVENT = "EVENT"
    PERIODIC = "PERIODIC"
