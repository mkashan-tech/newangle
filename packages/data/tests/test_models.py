"""Tests for basic entity creation and database-level constraints.

All data in this file is SYNTHETIC (see tests/fixtures/synthetic_data.py).
"""

from __future__ import annotations

import datetime as dt

import pytest
from fixtures.synthetic_data import (
    synthetic_company,
    synthetic_corporate_event,
    synthetic_listed_security,
    synthetic_promoter_holding_observation,
    synthetic_source,
)
from sqlalchemy.exc import IntegrityError

from newangle_data.models import Exchange


def test_create_company_valid(session):
    company = synthetic_company()
    session.add(company)
    session.flush()

    assert company.id is not None
    assert company.created_at is not None
    assert company.updated_at is not None


def test_company_name_required(session):
    company = synthetic_company(name=None)
    session.add(company)
    with pytest.raises(IntegrityError):
        session.flush()


def test_company_cin_uniqueness(session):
    session.add(synthetic_company(cin="L99999MH2001PLC999999"))
    session.flush()

    session.add(synthetic_company(name="Another Synthetic Co", cin="L99999MH2001PLC999999"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_company_cin_nullable_multiple_unknown(session):
    """Two companies with unknown (NULL) CIN must both be insertable —
    Postgres does not enforce uniqueness across NULLs, which is exactly
    the desired behavior: "CIN not yet confirmed" is not the same claim
    as "CIN confirmed to be identical" for two different companies."""
    session.add(synthetic_company(name="Company A", cin=None))
    session.add(synthetic_company(name="Company B", cin=None))
    session.flush()  # should not raise


def test_listed_security_requires_company(session):
    security = synthetic_listed_security(company=None)
    session.add(security)
    with pytest.raises(IntegrityError):
        session.flush()


def test_listed_security_symbol_period_uniqueness(session):
    company = synthetic_company()
    session.add(company)
    session.flush()

    session.add(
        synthetic_listed_security(company, symbol="SYNTEST", effective_from=dt.date(2020, 1, 1))
    )
    session.flush()

    # Same exchange + symbol + effective_from is a genuine duplicate.
    session.add(
        synthetic_listed_security(company, symbol="SYNTEST", effective_from=dt.date(2020, 1, 1))
    )
    with pytest.raises(IntegrityError):
        session.flush()


def test_listed_security_symbol_change_over_time(session):
    """A company can have two ListedSecurity rows for the same exchange
    representing a real-world symbol change, as long as the effective
    periods are represented with different effective_from dates."""
    company = synthetic_company()
    session.add(company)
    session.flush()

    old = synthetic_listed_security(
        company,
        symbol="OLDSYM",
        effective_from=dt.date(2015, 1, 1),
        effective_to=dt.date(2022, 6, 30),
    )
    new = synthetic_listed_security(
        company,
        symbol="NEWSYM",
        effective_from=dt.date(2022, 7, 1),
        effective_to=None,
    )
    session.add_all([old, new])
    session.flush()  # should not raise

    assert len(company.listed_securities) == 2


def test_same_isin_across_two_exchanges_allowed(session):
    """The same underlying security commonly shares one ISIN across
    NSE and BSE listings under different symbols — isin is deliberately
    not globally unique (see security.py docstring)."""
    company = synthetic_company()
    session.add(company)
    session.flush()

    session.add(
        synthetic_listed_security(
            company, exchange=Exchange.NSE, symbol="SYNNSE", isin="INE000S00000"
        )
    )
    session.add(
        synthetic_listed_security(
            company, exchange=Exchange.BSE, symbol="539999", isin="INE000S00000"
        )
    )
    session.flush()  # should not raise


def test_source_name_uniqueness(session):
    session.add(synthetic_source(name="Duplicate Source"))
    session.flush()

    session.add(synthetic_source(name="Duplicate Source"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_corporate_event_requires_source_and_company(session):
    event = synthetic_corporate_event(company=None, source=None)
    session.add(event)
    with pytest.raises(IntegrityError):
        session.flush()


def test_corporate_event_publication_before_event_date_rejected(session):
    """A disclosure cannot legitimately predate the event it discloses."""
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    event = synthetic_corporate_event(
        company,
        source,
        event_date=dt.date(2024, 6, 10),
        publication_date=dt.date(2024, 6, 9),  # before event_date: invalid
    )
    session.add(event)
    with pytest.raises(IntegrityError):
        session.flush()


def test_corporate_event_duplicate_raw_reference_from_same_source_rejected(session):
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    session.add(synthetic_corporate_event(company, source, raw_reference="dup-ref"))
    session.flush()

    session.add(synthetic_corporate_event(company, source, raw_reference="dup-ref"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_corporate_event_multiple_null_raw_references_allowed(session):
    """Two distinct events from the same source that both lack a
    captured raw_reference must not collide — NULL != NULL."""
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    session.add(
        synthetic_corporate_event(
            company,
            source,
            raw_reference=None,
            event_date=dt.date(2024, 1, 1),
            publication_date=dt.date(2024, 1, 1),
        )
    )
    session.add(
        synthetic_corporate_event(
            company,
            source,
            raw_reference=None,
            event_date=dt.date(2024, 2, 1),
            publication_date=dt.date(2024, 2, 1),
        )
    )
    session.flush()  # should not raise


def test_promoter_holding_pct_out_of_range_rejected(session):
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    obs = synthetic_promoter_holding_observation(
        company, source, pledged_pct_of_promoter_holding=150.0
    )
    session.add(obs)
    with pytest.raises(IntegrityError):
        session.flush()


def test_promoter_holding_negative_share_count_rejected(session):
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    obs = synthetic_promoter_holding_observation(company, source, pledged_shares_count=-1)
    session.add(obs)
    with pytest.raises(IntegrityError):
        session.flush()


def test_promoter_holding_duplicate_filing_rejected(session):
    """Re-ingesting the exact same (source, raw_reference) filing twice
    must be rejected as a duplicate observation."""
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    session.add(synthetic_promoter_holding_observation(company, source, raw_reference="filing-1"))
    session.flush()

    session.add(synthetic_promoter_holding_observation(company, source, raw_reference="filing-1"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_promoter_holding_correction_chain(session):
    """A revised/corrected intimation is modeled as a new row pointing
    back to the observation it corrects, per the real BSE "revised
    intimation" example found during Phase 1 research (see
    docs/decisions/003-promoter-holding-observation-model.md)."""
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    original = synthetic_promoter_holding_observation(
        company, source, raw_reference="filing-original", pledged_pct_of_promoter_holding=10.0
    )
    session.add(original)
    session.flush()

    correction = synthetic_promoter_holding_observation(
        company,
        source,
        raw_reference="filing-correction",
        pledged_pct_of_promoter_holding=12.0,
        corrects=original,
    )
    session.add(correction)
    session.flush()  # should not raise

    assert correction.corrects_observation_id == original.id


def test_promoter_holding_pledged_cannot_exceed_total_shares_is_app_level_not_db_level():
    """The invariant "pledged_shares_count <= total_promoter_shares_count"
    is enforced by the Pydantic input schema (see schemas.py), not by a
    database CHECK constraint, because it requires comparing two nullable
    columns and Postgres CHECK constraints involving two nullable columns
    would silently pass whenever either is NULL, which would be a weaker
    guarantee than the one the application actually needs. This test
    documents that this invariant lives at the validation layer — see
    test_schemas.py for its enforcement."""
    assert True
