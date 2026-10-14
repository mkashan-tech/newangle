"""Tests for the Pydantic input-validation schemas in newangle_data.schemas.

These validate invariants that are enforced at the application layer
rather than (or in addition to) the database layer — see
test_promoter_holding_pledged_cannot_exceed_total_shares_is_app_level_not_db_level
in test_models.py for why that particular invariant lives here.
"""

from __future__ import annotations

import datetime as dt

import pytest
from pydantic import ValidationError

from newangle_data.models.enums import PromoterHoldingObservationType
from newangle_data.schemas import CorporateEventInput, PromoterHoldingObservationInput

UTC = dt.UTC


def _valid_event_kwargs(**overrides):
    defaults = dict(
        company_id=1,
        event_type="BOARD_DECISION",
        event_date=dt.date(2024, 1, 29),
        publication_date=dt.date(2024, 1, 29),
        available_at=dt.datetime(2024, 1, 29, 14, 59, tzinfo=UTC),
        retrieved_at=dt.datetime(2024, 1, 30, 9, 0, tzinfo=UTC),
        source_id=1,
        description="SYNTHETIC test event",
    )
    defaults.update(overrides)
    return defaults


def _valid_observation_kwargs(**overrides):
    defaults = dict(
        company_id=1,
        observation_type=PromoterHoldingObservationType.EVENT,
        as_of_date=dt.date(2024, 8, 14),
        publication_date=dt.date(2024, 8, 14),
        available_at=dt.datetime(2024, 8, 14, 18, 0, tzinfo=UTC),
        retrieved_at=dt.datetime(2024, 8, 15, 9, 0, tzinfo=UTC),
        source_id=1,
        pledged_shares_count=1_000,
        total_promoter_shares_count=10_000,
    )
    defaults.update(overrides)
    return defaults


def test_corporate_event_input_valid():
    CorporateEventInput(**_valid_event_kwargs())  # should not raise


def test_corporate_event_input_rejects_publication_before_event():
    with pytest.raises(ValidationError):
        CorporateEventInput(
            **_valid_event_kwargs(
                event_date=dt.date(2024, 6, 10), publication_date=dt.date(2024, 6, 9)
            )
        )


def test_corporate_event_input_rejects_available_before_publication():
    with pytest.raises(ValidationError):
        CorporateEventInput(
            **_valid_event_kwargs(
                publication_date=dt.date(2024, 6, 10),
                available_at=dt.datetime(2024, 6, 9, 9, 0, tzinfo=UTC),
            )
        )


def test_corporate_event_input_rejects_empty_description():
    with pytest.raises(ValidationError):
        CorporateEventInput(**_valid_event_kwargs(description=""))


def test_promoter_holding_input_valid():
    PromoterHoldingObservationInput(**_valid_observation_kwargs())  # should not raise


def test_promoter_holding_input_rejects_pct_out_of_range():
    with pytest.raises(ValidationError):
        PromoterHoldingObservationInput(
            **_valid_observation_kwargs(pledged_pct_of_promoter_holding=101)
        )


def test_promoter_holding_input_rejects_pledged_exceeding_total_shares():
    with pytest.raises(ValidationError):
        PromoterHoldingObservationInput(
            **_valid_observation_kwargs(
                pledged_shares_count=20_000, total_promoter_shares_count=10_000
            )
        )


def test_promoter_holding_input_allows_missing_figures():
    """Not-disclosed figures must be representable as None, never a
    fabricated value — see PromoterHoldingObservation docstring."""
    obs = PromoterHoldingObservationInput(
        **_valid_observation_kwargs(
            pledged_shares_count=None,
            total_promoter_shares_count=None,
            pledged_pct_of_promoter_holding=None,
            pledged_pct_of_total_share_capital=None,
            total_promoter_holding_pct=None,
        )
    )
    assert obs.pledged_shares_count is None
