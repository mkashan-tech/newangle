"""Database engine/session construction.

Reads `DATABASE_URL` from the environment (see the repository's
`.env.example`). This module intentionally does no connection pooling
tuning, retry logic, or multi-database routing — none of that is
justified yet for a Phase 1 schema-validation package.
"""

from __future__ import annotations

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    """Return the configured database URL, or raise a clear error."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy the repository's .env.example to .env "
            "and set DATABASE_URL, or export it directly in your shell."
        )
    return url


def make_engine(database_url: str | None = None, *, echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine for the given (or environment) database URL."""
    return create_engine(database_url or get_database_url(), echo=echo, future=True)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a session factory bound to the given engine."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
