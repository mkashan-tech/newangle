"""Point-in-time filtering tests.

These tests prove the data model can answer "what was actually known at
cutoff T?" using `available_at`, and that naive filtering on
`event_date` / `as_of_date` alone would leak future information
(look-ahead bias) — the exact failure mode Section 14 of the master
brief requires bias controls against.

All data is SYNTHETIC (see tests/fixtures/synthetic_data.py).
"""

from __future__ import annotations

import datetime as dt

from fixtures.synthetic_data import (
    synthetic_company,
    synthetic_corporate_event,
    synthetic_promoter_holding_observation,
    synthetic_source,
)
from sqlalchemy import select

from newangle_data.models import CorporateEvent, PromoterHoldingObservation

UTC = dt.UTC


def _point_in_time_events(session, cutoff: dt.datetime):
    """The point-in-time query pattern a future research layer would use:
    filter on `available_at`, not on `event_date` or `publication_date`."""
    stmt = select(CorporateEvent).where(CorporateEvent.available_at <= cutoff)
    return session.execute(stmt).scalars().all()


def test_available_at_excludes_future_information(session):
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    # An event whose underlying transaction happened on 2024-01-01, but
    # which (per real SEBI LODR timelines researched for this schema)
    # was only disclosed — and thus only knowable — on 2024-01-03.
    late_disclosed_event = synthetic_corporate_event(
        company,
        source,
        event_type="BOARD_DECISION",
        event_date=dt.date(2024, 1, 1),
        publication_date=dt.date(2024, 1, 3),
        available_at=dt.datetime(2024, 1, 3, 9, 0, tzinfo=UTC),
        raw_reference="pit-test/late-disclosed",
    )
    session.add(late_disclosed_event)
    session.flush()

    # A cutoff set to the event_date itself (2024-01-01) must NOT see
    # this event, even though event_date <= cutoff — because it was not
    # actually knowable until 2024-01-03.
    cutoff = dt.datetime(2024, 1, 1, 23, 59, tzinfo=UTC)
    visible = _point_in_time_events(session, cutoff)
    assert late_disclosed_event not in visible

    # A naive filter on event_date alone would have wrongly included it —
    # demonstrating exactly the look-ahead bias risk available_at exists
    # to prevent.
    naive_stmt = select(CorporateEvent).where(CorporateEvent.event_date <= cutoff.date())
    naively_visible = session.execute(naive_stmt).scalars().all()
    assert late_disclosed_event in naively_visible, (
        "test setup error: this event should demonstrate the naive-filter failure mode"
    )

    # Once the cutoff reaches the actual availability time, it becomes visible.
    later_cutoff = dt.datetime(2024, 1, 3, 9, 0, tzinfo=UTC)
    assert late_disclosed_event in _point_in_time_events(session, later_cutoff)


def test_promoter_holding_point_in_time_filtering(session):
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    obs = synthetic_promoter_holding_observation(
        company,
        source,
        as_of_date=dt.date(2024, 6, 30),  # quarter-end the figures describe
        publication_date=dt.date(2024, 7, 12),  # actually filed ~2 weeks later
        available_at=dt.datetime(2024, 7, 12, 17, 0, tzinfo=UTC),
        raw_reference="pit-test/periodic-q1",
    )
    session.add(obs)
    session.flush()

    stmt = select(PromoterHoldingObservation).where(
        PromoterHoldingObservation.available_at <= dt.datetime(2024, 7, 1, tzinfo=UTC)
    )
    assert session.execute(stmt).scalars().all() == []

    stmt_after = select(PromoterHoldingObservation).where(
        PromoterHoldingObservation.available_at <= dt.datetime(2024, 7, 12, 17, 0, tzinfo=UTC)
    )
    assert obs in session.execute(stmt_after).scalars().all()


def test_available_at_same_day_as_publication_is_valid(session):
    """available_at may equal publication_date (a same-day, timestamped
    disclosure) — this is the common case for Regulation 30 same-day
    filings — and must not be rejected."""
    company = synthetic_company()
    source = synthetic_source()
    session.add_all([company, source])
    session.flush()

    event = synthetic_corporate_event(
        company,
        source,
        event_date=dt.date(2024, 1, 29),
        publication_date=dt.date(2024, 1, 29),
        available_at=dt.datetime(2024, 1, 29, 14, 59, tzinfo=UTC),
        raw_reference="pit-test/same-day",
    )
    session.add(event)
    session.flush()  # should not raise
