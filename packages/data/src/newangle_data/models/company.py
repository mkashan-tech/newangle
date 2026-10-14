"""Company (entity) identity.

A Company represents the underlying corporate entity, independent of any
particular stock-exchange listing, ticker symbol, or ISIN. See
docs/decisions/001-company-security-identity.md for why entity identity
and listed-security identity are modeled as separate tables.
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from newangle_data.models.base import Base, CreatedAtMixin, IdMixin

if TYPE_CHECKING:
    from newangle_data.models.security import ListedSecurity


class Company(Base, IdMixin, CreatedAtMixin):
    """A corporate entity researched by NewAngle.

    `cin` (Corporate Identity Number) is India's Ministry of Corporate
    Affairs registration number — a genuinely stable, government-issued
    identifier for the legal entity that does not change when the
    company renames, re-lists, or changes its trading symbol. It is
    modeled as nullable + unique-when-present because, at this stage,
    NewAngle may register a company before its CIN has been confirmed
    from an authoritative source, and fabricating a placeholder CIN is
    explicitly disallowed by the project's research-honesty principles.

    `sector` is an intentionally plain, free-text, nullable field for
    now. A controlled sector taxonomy (e.g. NSE/BSE industry
    classification) is a real future need, but building that taxonomy
    now — before any sector-based research question requires it — would
    be schema over-engineering ahead of demonstrated need.
    """

    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cin: Mapped[str | None] = mapped_column(String(21), unique=True, nullable=True)
    sector: Mapped[str | None] = mapped_column(String(255), nullable=True)

    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    listed_securities: Mapped[list[ListedSecurity]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug convenience only
        return f"Company(id={self.id!r}, name={self.name!r}, cin={self.cin!r})"
