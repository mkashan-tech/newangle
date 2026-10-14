"""Listed-security identity.

A ListedSecurity represents one company's listing of one security class
on one exchange, under one trading symbol, for a given period of time.
See docs/decisions/001-company-security-identity.md for the reasoning.
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from newangle_data.models.base import Base, CreatedAtMixin, IdMixin
from newangle_data.models.enums import Exchange

if TYPE_CHECKING:
    from newangle_data.models.company import Company


class ListedSecurity(Base, IdMixin, CreatedAtMixin):
    """One company's listing on one exchange under one symbol, over time.

    Symbols change (renames, demergers, re-listings). A Company can have
    more than one ListedSecurity row over its history on the same
    exchange, and more than one simultaneously across exchanges (e.g. the
    same company listed on both NSE and BSE, typically under different
    symbols but the same ISIN).

    `effective_from` / `effective_to` bound the period during which this
    (exchange, symbol) pairing was the company's active identity there.
    `effective_to IS NULL` means "currently active." Application code
    (and the test suite) is responsible for keeping at most one active
    row per (company_id, exchange) — see
    docs/decisions/001-company-security-identity.md for why this is
    enforced procedurally rather than with a Postgres partial unique
    index in Phase 1.

    `isin` (International Securities Identification Number) is modeled as
    required (not nullable): for a security genuinely listed and
    tradeable in India, an ISIN is assigned by definition, so there is no
    honest "unknown ISIN" state the way there can be an unknown CIN. It
    is intentionally *not* globally unique at the database level: the
    same equity class commonly carries the same ISIN across multiple
    exchange listings (e.g. a company listed on both NSE and BSE under
    different symbols shares one ISIN), so a global uniqueness
    constraint on `isin` alone would be factually wrong. It is indexed
    for lookups instead.
    """

    __tablename__ = "listed_securities"
    __table_args__ = (
        UniqueConstraint(
            "exchange", "symbol", "effective_from", name="uq_listed_security_symbol_period"
        ),
        Index("ix_listed_securities_company_id", "company_id"),
        Index("ix_listed_securities_isin", "isin"),
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    exchange: Mapped[Exchange] = mapped_column(SAEnum(Exchange, name="exchange"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    isin: Mapped[str] = mapped_column(String(12), nullable=False)
    effective_from: Mapped[dt.date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[dt.date | None] = mapped_column(Date, nullable=True)

    company: Mapped[Company] = relationship(back_populates="listed_securities")

    def __repr__(self) -> str:  # pragma: no cover - debug convenience only
        return (
            f"ListedSecurity(id={self.id!r}, company_id={self.company_id!r}, "
            f"exchange={self.exchange!r}, symbol={self.symbol!r}, isin={self.isin!r})"
        )
