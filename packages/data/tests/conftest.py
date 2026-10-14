"""Shared pytest fixtures for the newangle-data test suite.

Tests run against a real PostgreSQL database (see packages/data/README.md
for setup) rather than SQLite, because this schema relies on
Postgres-specific behavior (native ENUM types, NUMERIC precision,
partial-NULL-aware UNIQUE constraints) that SQLite does not faithfully
emulate. Tests never depend on any live external/internet data source —
only on a local Postgres instance the developer or CI controls.

Each test runs inside a transaction that is rolled back afterward, so
tests do not depend on execution order and leave no residue.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from newangle_data.db import make_engine
from newangle_data.models import Base

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://newangle:newangle_dev@localhost:5432/newangle_test",
)


@pytest.fixture(scope="session")
def engine():
    engine = make_engine(TEST_DATABASE_URL)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - environment guard, not app logic
        pytest.skip(
            f"Could not connect to test database at {TEST_DATABASE_URL!r} ({exc!r}). "
            "Start PostgreSQL and create the test database — see packages/data/README.md."
        )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def session(engine) -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    # join_transaction_mode="create_savepoint": session-level rollback (which
    # happens automatically after a flush raises IntegrityError, as several
    # constraint tests intentionally trigger) uses a SAVEPOINT instead of
    # ending the outer transaction, so the fixture's own rollback() below
    # always has a live transaction to roll back.
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connection.close()
