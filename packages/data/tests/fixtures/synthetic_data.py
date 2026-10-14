"""SYNTHETIC test fixtures.

Every value produced here is fabricated for the sole purpose of
exercising schema behavior in tests. None of it is real market data,
real company data, or a real regulatory filing. It must never be reused
outside the test suite, and nothing in this module should be imported by
application/library code — only by tests.
"""

from __future__ import annotations

import datetime as dt

from newangle_data.models import (
    Company,
    CorporateEvent,
    Exchange,
    ListedSecurity,
    PromoterHoldingObservation,
    PromoterHoldingObservationType,
    Source,
    SourceType,
)

UTC = dt.UTC


def synthetic_company(**overrides) -> Company:
    """A fabricated company — SYNTHETIC, not a real listed entity."""
    defaults = dict(
        name="Synthetic Testware Industries Ltd.",
        cin="L99999MH2001PLC999999",
        sector="Synthetic Testing",
    )
    defaults.update(overrides)
    return Company(**defaults)


def synthetic_source(**overrides) -> Source:
    """A fabricated source record — SYNTHETIC."""
    defaults = dict(
        name="Synthetic Test Exchange Filings",
        source_type=SourceType.EXCHANGE_FILING,
        url="https://example.invalid/synthetic-source",
        terms_reference="SYNTHETIC fixture source; not a real data provider.",
    )
    defaults.update(overrides)
    return Source(**defaults)


def synthetic_listed_security(company: Company, **overrides) -> ListedSecurity:
    """A fabricated exchange listing — SYNTHETIC symbol/ISIN."""
    defaults = dict(
        company=company,
        exchange=Exchange.NSE,
        symbol="SYNTEST",
        isin="INE000S00000",
        effective_from=dt.date(2020, 1, 1),
        effective_to=None,
    )
    defaults.update(overrides)
    return ListedSecurity(**defaults)


def synthetic_corporate_event(company: Company, source: Source, **overrides) -> CorporateEvent:
    """A fabricated corporate event — SYNTHETIC, modeled loosely on the
    real SEBI LODR Regulation 30 disclosure timeline researched for this
    schema (event occurs, then is disclosed within a documented window,
    with a specific available_at time)."""
    defaults = dict(
        company=company,
        event_type="KMP_APPOINTMENT",
        event_date=dt.date(2024, 1, 29),
        publication_date=dt.date(2024, 1, 29),
        available_at=dt.datetime(2024, 1, 29, 14, 59, tzinfo=UTC),
        retrieved_at=dt.datetime(2024, 1, 30, 9, 0, tzinfo=UTC),
        source=source,
        description="SYNTHETIC: appointment of a company secretary (test fixture).",
        raw_reference="synthetic-ref/kmp-appointment/0001",
    )
    defaults.update(overrides)
    return CorporateEvent(**defaults)


def synthetic_promoter_holding_observation(
    company: Company, source: Source, **overrides
) -> PromoterHoldingObservation:
    """A fabricated promoter holding/pledge observation — SYNTHETIC.

    Modeled loosely on the two real SEBI (SAST) Regulations, 2011
    Regulation 31 disclosure mechanisms researched for this schema:
    event-based pledge creation and periodic quarterly reporting.
    """
    defaults = dict(
        company=company,
        observation_type=PromoterHoldingObservationType.EVENT,
        as_of_date=dt.date(2024, 8, 14),
        total_promoter_holding_pct=55.0,
        pledged_pct_of_promoter_holding=10.0,
        pledged_pct_of_total_share_capital=5.5,
        pledged_shares_count=1_600_000,
        total_promoter_shares_count=16_000_000,
        publication_date=dt.date(2024, 8, 14),
        available_at=dt.datetime(2024, 8, 14, 18, 0, tzinfo=UTC),
        retrieved_at=dt.datetime(2024, 8, 15, 9, 0, tzinfo=UTC),
        source=source,
        raw_reference="synthetic-ref/pledge-event/0001",
    )
    defaults.update(overrides)
    return PromoterHoldingObservation(**defaults)
