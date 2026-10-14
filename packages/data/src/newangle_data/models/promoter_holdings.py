"""Promoter holding / pledge observations — the first signal-ready model.

See docs/decisions/003-promoter-holding-observation-model.md for the
research basis (SEBI SAST Regulations, 2011, Regulation 31) and the
reasoning behind every non-obvious field below.
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from newangle_data.models.base import Base, CreatedAtMixin, IdMixin
from newangle_data.models.enums import PromoterHoldingObservationType

if TYPE_CHECKING:
    from newangle_data.models.company import Company
    from newangle_data.models.source import Source


class PromoterHoldingObservation(Base, IdMixin, CreatedAtMixin):
    """One disclosed promoter shareholding/pledge observation.

    Percentage fields are deliberately split by basis rather than a single
    ambiguous `pledged_pct`:

    - `pledged_pct_of_promoter_holding` — pledged shares as a percentage
      of the promoter(s)' own total holding.
    - `pledged_pct_of_total_share_capital` — pledged shares as a
      percentage of the company's total share capital.

    These are two different, both commonly disclosed, numbers, and
    conflating them would silently misrepresent risk (a promoter with a
    small stake who has pledged all of it has 100% pledged-of-holding
    but a small pledged-of-total-capital figure). All percentage/share
    fields are nullable because source disclosures do not always report
    every figure (e.g. an event-based pledge-creation filing may report
    only share counts, not a resulting percentage) — fabricating a
    missing figure is disallowed by the project's research-honesty
    principles, so the schema must allow "not disclosed" to be
    represented honestly as NULL rather than 0 or a guess.

    `corrects_observation_id` models the real-world existence of revised/
    corrected intimations (see decision record for a real BSE example
    found during research) without violating the uniqueness constraint
    that prevents re-ingesting the same filing twice.
    """

    __tablename__ = "promoter_holding_observations"
    __table_args__ = (
        CheckConstraint(
            "pledged_pct_of_promoter_holding IS NULL OR "
            "(pledged_pct_of_promoter_holding >= 0 AND pledged_pct_of_promoter_holding <= 100)",
            name="ck_pledge_pct_of_holding_range",
        ),
        CheckConstraint(
            "pledged_pct_of_total_share_capital IS NULL OR "
            "(pledged_pct_of_total_share_capital >= 0 "
            "AND pledged_pct_of_total_share_capital <= 100)",
            name="ck_pledge_pct_of_capital_range",
        ),
        CheckConstraint(
            "total_promoter_holding_pct IS NULL OR "
            "(total_promoter_holding_pct >= 0 AND total_promoter_holding_pct <= 100)",
            name="ck_total_holding_pct_range",
        ),
        CheckConstraint(
            "pledged_shares_count IS NULL OR pledged_shares_count >= 0",
            name="ck_pledged_shares_nonnegative",
        ),
        CheckConstraint(
            "total_promoter_shares_count IS NULL OR total_promoter_shares_count >= 0",
            name="ck_total_promoter_shares_nonnegative",
        ),
        Index(
            "ix_promoter_holdings_company_as_of_date",
            "company_id",
            "as_of_date",
        ),
        Index("ix_promoter_holdings_available_at", "available_at"),
        UniqueConstraint(
            "source_id", "raw_reference", name="uq_promoter_holdings_source_raw_reference"
        ),
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    observation_type: Mapped[PromoterHoldingObservationType] = mapped_column(
        SAEnum(PromoterHoldingObservationType, name="promoter_holding_observation_type"),
        nullable=False,
    )
    as_of_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    total_promoter_holding_pct: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    pledged_pct_of_promoter_holding: Mapped[float | None] = mapped_column(
        Numeric(6, 3), nullable=True
    )
    pledged_pct_of_total_share_capital: Mapped[float | None] = mapped_column(
        Numeric(6, 3), nullable=True
    )
    pledged_shares_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    total_promoter_shares_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # --- Point-in-time fields (see docs/decisions/002-provenance-and-point-in-time.md) ---
    publication_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    available_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    retrieved_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="RESTRICT"), nullable=False
    )
    raw_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)

    corrects_observation_id: Mapped[int | None] = mapped_column(
        ForeignKey("promoter_holding_observations.id", ondelete="SET NULL"), nullable=True
    )

    company: Mapped[Company] = relationship("Company")
    source: Mapped[Source] = relationship("Source")
    corrects: Mapped[PromoterHoldingObservation | None] = relationship(
        "PromoterHoldingObservation", remote_side="PromoterHoldingObservation.id"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug convenience only
        return (
            f"PromoterHoldingObservation(id={self.id!r}, company_id={self.company_id!r}, "
            f"observation_type={self.observation_type!r}, as_of_date={self.as_of_date!r})"
        )
