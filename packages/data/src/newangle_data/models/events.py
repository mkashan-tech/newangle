"""Corporate / governance events — the normalized event layer.

See docs/decisions/002-provenance-and-point-in-time.md for the reasoning
behind the four separate timestamps (`event_date`, `publication_date`,
`available_at`, `retrieved_at`) and the raw/normalized boundary.
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from newangle_data.models.base import Base, CreatedAtMixin, IdMixin

if TYPE_CHECKING:
    from newangle_data.models.company import Company
    from newangle_data.models.source import Source


class CorporateEvent(Base, IdMixin, CreatedAtMixin):
    """A single disclosed corporate/governance event for a company.

    This is a deliberately general-purpose event table (board/KMP
    changes, auditor resignation, litigation, regulatory action, etc.)
    rather than one table per event type. `event_type` is a plain,
    documented string rather than an enum: the master brief explicitly
    warns against hard-coding a fixed taxonomy prematurely (Section 7),
    and future signals (Section 8 of the brief) span a wide, evolving
    range of event categories. Validation of which `event_type` values
    are currently "known" belongs in application/Pydantic code, not as a
    rigid database enum that would require a migration for every new
    signal category.

    `event_metadata` is an intentionally opaque JSON column for
    event-type-specific structured detail (e.g. litigation claim amount,
    KMP designation, rating agency and new/old rating) that doesn't
    justify its own column yet. If a specific field inside it becomes
    something NewAngle regularly queries or joins on, it should graduate
    to a real column in a future migration — it should not silently stay
    buried in JSON once that happens.

    Promoter pledge/holding observations are intentionally NOT modeled
    as rows in this table — see PromoterHoldingObservation and
    docs/decisions/003-promoter-holding-observation-model.md for why
    that signal has a dedicated, more structured model instead.
    """

    __tablename__ = "corporate_events"
    __table_args__ = (
        CheckConstraint("publication_date >= event_date", name="ck_event_publication_after_event"),
        Index("ix_corporate_events_company_event_date", "company_id", "event_date"),
        Index("ix_corporate_events_available_at", "available_at"),
        # Postgres unique constraints treat NULLs as distinct, so this only
        # rejects a genuine duplicate re-ingestion of the same filing
        # (same source + same non-null raw_reference); it never blocks two
        # events from the same source that both lack a raw_reference.
        UniqueConstraint(
            "source_id", "raw_reference", name="uq_corporate_events_source_raw_reference"
        ),
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)

    # --- Point-in-time fields (see docs/decisions/002-provenance-and-point-in-time.md) ---
    event_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    publication_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    available_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    retrieved_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="RESTRICT"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    raw_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    event_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    company: Mapped[Company] = relationship("Company")
    source: Mapped[Source] = relationship("Source")

    def __repr__(self) -> str:  # pragma: no cover - debug convenience only
        return (
            f"CorporateEvent(id={self.id!r}, company_id={self.company_id!r}, "
            f"event_type={self.event_type!r}, event_date={self.event_date!r})"
        )
