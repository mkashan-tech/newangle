# newangle-data

The NewAngle data-model foundation: SQLAlchemy ORM models, Alembic
migrations, and Pydantic validation schemas for companies, listed
securities, sources, corporate events, and promoter holding observations.

**What this package is:** a tested, reproducible database schema and the
Python types to work with it.

**What this package is not (yet):** there is no data ingestion, no event
detection, no analytics/event-study engine, and no API here. See the
repository root `README.md` for current project status, and
`docs/architecture/overview.md` for how this fits into the longer-term
design.

## Requirements

- Python 3.11+
- A local PostgreSQL server (16 was used during development; no
  version-specific features beyond standard `ENUM`, `NUMERIC`, and
  partial/plain `UNIQUE` constraints are used, so other reasonably
  current versions should work)

This project intentionally does not use SQLite for tests or development —
the schema relies on Postgres-specific behavior (native `ENUM` types,
`NUMERIC` precision, and `NULL`-aware `UNIQUE` constraints) that SQLite
does not faithfully emulate, and validating against the actual database
the project ships against was judged more valuable than a faster but
less faithful SQLite test run.

## Setup

1. **Install PostgreSQL** and ensure it's running locally (e.g. `sudo apt
   install postgresql` on Debian/Ubuntu, or your platform's equivalent).
   This project does not use Docker for this — running Postgres directly
   was simpler and didn't need Docker's benefits (see Principle 9, simple
   architecture first, in the repository root README).

2. **Create a role and databases.** Two are needed: one for local
   development, one for running the test suite (kept separate so running
   tests never touches data you're manually inspecting).

   ```bash
   sudo -u postgres psql -c "CREATE ROLE newangle WITH LOGIN PASSWORD 'newangle_dev' CREATEDB;"
   sudo -u postgres psql -c "CREATE DATABASE newangle_dev OWNER newangle;"
   sudo -u postgres psql -c "CREATE DATABASE newangle_test OWNER newangle;"
   ```

   The `CREATEDB` privilege is used by `tests/test_migrations.py`, which
   creates and drops its own disposable scratch database per test run to
   verify the Alembic migration works against a genuinely empty database
   (not just a database that already has the ORM's tables created some
   other way).

3. **Install the package:**

   ```bash
   cd packages/data
   pip install -e ".[dev]"
   ```

   The repository root's `.env.example` documents the environment
   variables below with working local-dev values matching step 2. No
   `.env` loader is wired up automatically in Phase 1 (adding one wasn't
   yet justified) — copy it to `.env` for your own reference if useful,
   but you still need to `export` the variables (step 4) for them to
   take effect.

4. **Set environment variables** (or rely on a `.env` loader of your
   choice — none is wired up automatically in Phase 1, to avoid adding a
   dependency not yet justified):

   ```bash
   export DATABASE_URL="postgresql+psycopg://newangle:newangle_dev@localhost:5432/newangle_dev"
   export TEST_DATABASE_URL="postgresql+psycopg://newangle:newangle_dev@localhost:5432/newangle_test"
   export TEST_ADMIN_DATABASE_URL="postgresql://newangle:newangle_dev@localhost:5432/postgres"
   ```

   `TEST_ADMIN_DATABASE_URL` points at Postgres's default `postgres`
   maintenance database and is only used to create/drop the scratch
   database in `test_migrations.py`.

## Running Migrations

```bash
cd packages/data
alembic upgrade head      # apply all migrations
alembic downgrade base    # revert to empty (useful for testing)
alembic current            # show the currently applied revision
alembic check               # confirm models and the latest migration agree (no drift)
```

`alembic/env.py` reads `DATABASE_URL` from the environment at runtime, so
the same migration environment works against the dev database, the test
database, or a CI database without editing `alembic.ini`.

To generate a new migration after changing a model:

```bash
alembic revision --autogenerate -m "short description"
```

**Always inspect the generated migration file before applying it.**
Autogenerate does not reliably handle everything — for example, Postgres
`ENUM` types are not dropped automatically when their table is dropped,
which had to be fixed by hand in the initial migration's `downgrade()`
(see the comment there, and
`docs/decisions/002-provenance-and-point-in-time.md`).

## Running Tests

```bash
cd packages/data
pytest
```

All 31 Phase 1 tests should pass against a correctly configured local
Postgres. Tests are skipped (not failed) with a clear message if no
database connection is available, rather than failing in a way that's
easy to misread as a code problem.

Test data is clearly labeled `SYNTHETIC` throughout (see
`tests/fixtures/synthetic_data.py`) and is fabricated purely to exercise
schema behavior — none of it is real company, market, or filing data.

## Linting and Type Checking

```bash
cd packages/data
ruff check .
ruff format --check .
mypy src/newangle_data
```

## Package Layout

```text
packages/data/
├── pyproject.toml
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/          # migration history
├── src/newangle_data/
│   ├── db.py               # engine/session construction
│   ├── schemas.py          # Pydantic input validation (not an API)
│   └── models/              # SQLAlchemy ORM models
│       ├── base.py
│       ├── enums.py
│       ├── company.py
│       ├── security.py
│       ├── source.py
│       ├── events.py
│       └── promoter_holdings.py
└── tests/
    ├── conftest.py
    ├── fixtures/synthetic_data.py
    ├── test_models.py
    ├── test_point_in_time.py
    ├── test_migrations.py
    └── test_schemas.py
```

## Why These Entities, Specifically

See `docs/decisions/` at the repository root for the full reasoning
behind each non-obvious schema choice:

- `001-company-security-identity.md` — why `Company` and `ListedSecurity`
  are separate tables, and how symbol changes and dual listings are
  represented.
- `002-provenance-and-point-in-time.md` — why four separate timestamp
  fields exist on every observation/event, and what real Indian
  disclosure-timeline research justified their precision.
- `003-promoter-holding-observation-model.md` — why promoter holding
  observations split event-based from periodic disclosures, and why
  pledge percentage is modeled on two separate bases.
