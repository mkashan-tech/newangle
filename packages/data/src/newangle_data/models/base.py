"""Declarative base and shared mixins for all NewAngle ORM models.

Design note (implementation-level, not a research decision): primary keys
are simple auto-incrementing integers (`BigInteger`) rather than UUIDs.
This project has no distributed-write or multi-database-merge requirement
yet (Principle 9 — simple architecture first), so integer PKs are the
boring, sufficient choice. Real-world stable identifiers (ISIN, CIN) are
modeled as separate unique business keys where they exist, precisely so
that "database identity" and "real-world identity" are never conflated.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Shared declarative base for all NewAngle data-model tables."""


class IdMixin:
    """Simple auto-incrementing integer primary key."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class CreatedAtMixin:
    """Row-creation bookkeeping timestamp.

    This records when the database row was created (an audit/bookkeeping
    fact about this database), which is conceptually distinct from
    `retrieved_at` on provenance-bearing tables (a domain fact about when
    NewAngle's data pipeline observed/retrieved the underlying information
    from its source). The two happen to coincide today because there is
    no automated ingestion pipeline yet (Phase 1) — rows are created
    directly by whatever process is populating the database, so
    `retrieved_at` is currently supplied by that process rather than
    derived from `created_at`. They are kept as separate columns because
    once real ingestion exists, a single retrieval run may insert rows at
    a different wall-clock time than the domain "retrieved" timestamp
    implied by the source (e.g. a backfill run in 2026 retrieving data
    that describes itself as retrieved on the day of a historical scrape).
    """

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
