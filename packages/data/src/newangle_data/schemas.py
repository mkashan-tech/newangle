"""Pydantic validation schemas.

These are *not* an API layer (none is built in Phase 1 — see the master
brief). They exist so that anything constructing a CorporateEvent or
PromoterHoldingObservation — right now, test fixtures; later, an
ingestion pipeline — validates basic invariants (date ordering,
percentage ranges) before touching the database, rather than relying on
database constraints as the only line of defense. Field-level docstrings
intentionally mirror the ORM model docstrings; see
newangle_data.models.events and newangle_data.models.promoter_holdings
for the full reasoning.
"""

from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field, model_validator

from newangle_data.models.enums import PromoterHoldingObservationType


class CorporateEventInput(BaseModel):
    """Validated input for creating a CorporateEvent row."""

    model_config = ConfigDict(str_strip_whitespace=True)

    company_id: int
    event_type: str = Field(min_length=1, max_length=64)
    event_date: dt.date
    publication_date: dt.date
    available_at: dt.datetime
    retrieved_at: dt.datetime
    source_id: int
    description: str = Field(min_length=1)
    raw_reference: str | None = None
    event_metadata: dict | None = None

    @model_validator(mode="after")
    def _check_date_ordering(self) -> CorporateEventInput:
        if self.publication_date < self.event_date:
            raise ValueError("publication_date cannot be before event_date")
        if self.available_at.date() < self.publication_date:
            # available_at may legitimately equal publication_date (same-day
            # disclosure with a specific time), but never precede it — you
            # cannot become aware of a disclosure before it was published.
            raise ValueError("available_at cannot be before publication_date")
        return self


class PromoterHoldingObservationInput(BaseModel):
    """Validated input for creating a PromoterHoldingObservation row."""

    model_config = ConfigDict(str_strip_whitespace=True)

    company_id: int
    observation_type: PromoterHoldingObservationType
    as_of_date: dt.date
    total_promoter_holding_pct: float | None = Field(default=None, ge=0, le=100)
    pledged_pct_of_promoter_holding: float | None = Field(default=None, ge=0, le=100)
    pledged_pct_of_total_share_capital: float | None = Field(default=None, ge=0, le=100)
    pledged_shares_count: int | None = Field(default=None, ge=0)
    total_promoter_shares_count: int | None = Field(default=None, ge=0)
    publication_date: dt.date
    available_at: dt.datetime
    retrieved_at: dt.datetime
    source_id: int
    raw_reference: str | None = None
    corrects_observation_id: int | None = None

    @model_validator(mode="after")
    def _check_availability_ordering(self) -> PromoterHoldingObservationInput:
        if self.available_at.date() < self.publication_date:
            raise ValueError("available_at cannot be before publication_date")
        return self

    @model_validator(mode="after")
    def _check_share_counts_consistent(self) -> PromoterHoldingObservationInput:
        if (
            self.pledged_shares_count is not None
            and self.total_promoter_shares_count is not None
            and self.pledged_shares_count > self.total_promoter_shares_count
        ):
            raise ValueError("pledged_shares_count cannot exceed total_promoter_shares_count")
        return self
