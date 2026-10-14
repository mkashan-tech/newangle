"""Tests that run the actual Alembic migration (not just
`Base.metadata.create_all()`) against a disposable scratch database.

This is the test that actually proves "the migration can initialize the
schema from a clean database," rather than only proving the ORM model
definitions are internally consistent (which is what conftest.py's
`engine` fixture / test_models.py exercise). It creates and drops its own
scratch database so it doesn't interfere with the shared test database
used by other test modules, and is skipped (not failed) if no local
Postgres admin connection is available, consistent with never depending
on infrastructure the environment doesn't provide.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import psycopg
import pytest
import sqlalchemy as sa
from alembic.config import Config

from alembic import command

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ADMIN_DATABASE_URL = os.environ.get(
    "TEST_ADMIN_DATABASE_URL",
    "postgresql://newangle:newangle_dev@localhost:5432/postgres",
)


def _make_scratch_database() -> tuple[str, str]:
    """Create a uniquely-named scratch database; return (db_name, sqlalchemy_url)."""
    db_name = f"newangle_migration_test_{uuid.uuid4().hex[:12]}"
    conn = psycopg.connect(ADMIN_DATABASE_URL, autocommit=True)
    try:
        conn.execute(f'CREATE DATABASE "{db_name}"')
    finally:
        conn.close()
    url = ADMIN_DATABASE_URL.rsplit("/", 1)[0] + f"/{db_name}"
    return db_name, url.replace("postgresql://", "postgresql+psycopg://")


def _drop_scratch_database(db_name: str) -> None:
    conn = psycopg.connect(ADMIN_DATABASE_URL, autocommit=True)
    try:
        conn.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
    finally:
        conn.close()


@pytest.fixture()
def scratch_db():
    try:
        db_name, url = _make_scratch_database()
    except Exception as exc:  # pragma: no cover - environment guard
        pytest.skip(f"Could not create a scratch database ({exc!r}); skipping migration test.")
        return
    yield db_name, url
    _drop_scratch_database(db_name)


def _alembic_config(database_url: str) -> Config:
    cfg = Config(str(PACKAGE_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(PACKAGE_ROOT / "alembic"))
    os.environ["DATABASE_URL"] = database_url
    return cfg


def test_migration_upgrades_from_empty_database(scratch_db):
    _db_name, url = scratch_db
    cfg = _alembic_config(url)

    command.upgrade(cfg, "head")

    engine = sa.create_engine(url)
    inspector = sa.inspect(engine)
    tables = set(inspector.get_table_names())
    assert {
        "companies",
        "sources",
        "corporate_events",
        "listed_securities",
        "promoter_holding_observations",
        "alembic_version",
    }.issubset(tables)
    engine.dispose()


def test_migration_downgrade_then_upgrade_round_trip(scratch_db):
    """Reproduces the exact failure mode found and fixed during Phase 1
    development: Postgres ENUM types are not dropped automatically when
    their table is dropped, so a downgrade-then-upgrade cycle would fail
    with "type already exists" unless the migration's downgrade() also
    drops the ENUM types explicitly."""
    _db_name, url = scratch_db
    cfg = _alembic_config(url)

    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")  # must not raise

    engine = sa.create_engine(url)
    inspector = sa.inspect(engine)
    assert "companies" in inspector.get_table_names()
    engine.dispose()
