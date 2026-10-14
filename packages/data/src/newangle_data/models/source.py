"""Information sources.

Every observation and event in the data model must be traceable to a
Source — see docs/decisions/002-provenance-and-point-in-time.md. This
table intentionally does not attempt to model per-source access
credentials, rate limits, or licensing terms in structured columns yet
(Section 16 of the master brief requires that investigation to happen
*before* a connector is built, and no connector exists in Phase 1). It
provides just enough structure to record what NewAngle currently knows
about a source's identity and terms.
"""

from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from newangle_data.models.base import Base, CreatedAtMixin, IdMixin
from newangle_data.models.enums import SourceType


class Source(Base, IdMixin, CreatedAtMixin):
    """An information source that NewAngle records observations/events from.

    `terms_reference` is a free-text/URL field for a human-readable note
    on usage/redistribution terms (per Section 8 — data provenance
    matters). It is not a substitute for the fuller data-source
    documentation required under `docs/data-sources/` once a real
    connector is built; it exists so that even a manually-entered source
    used for early schema validation carries *some* provenance note
    rather than none.
    """

    __tablename__ = "sources"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(SourceType, name="source_type"), nullable=False
    )
    url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    terms_reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - debug convenience only
        return f"Source(id={self.id!r}, name={self.name!r}, source_type={self.source_type!r})"
