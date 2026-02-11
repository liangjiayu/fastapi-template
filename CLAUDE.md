# CLAUDE.md

## Project Overview

FastAPI project template with async SQLAlchemy, supporting PostgreSQL and SQLite.

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (async)
- **Database:** PostgreSQL (asyncpg) / SQLite (aiosqlite)
- **Migrations:** Alembic
- **Validation:** Pydantic v2 + pydantic-settings
- **Logging:** Loguru
- **Package Manager:** uv

## Project Structure

```
app/
├── main.py              # App entry point (creates app instance)
├── api/                 # Route handlers (thin layer, delegates to services)
├── core/
│   ├── app.py           # App factory (init_app) + lifespan
│   ├── config.py        # Settings via pydantic-settings (single source of truth)
│   └── database.py      # Async engine, session factory, Base, get_db()
├── models/              # SQLAlchemy ORM models
├── repositories/        # Data access layer (static methods, receive db session)
├── schemas/             # Pydantic request/response schemas
└── services/            # Business logic layer (calls repositories)
```

## Architecture

- **Layered architecture:** API → Service → Repository → Database
- Routes only handle request/response; business logic lives in services
- Repositories handle all database operations
- All database operations are async

## Commands

- **Run dev server:** `fastapi dev app/main.py`
- **Install deps:** `uv sync`
- **Initialize database:** `uv run alembic upgrade head`
- **Create migration:** `uv run alembic revision --autogenerate -m "description"`
- **Apply migrations:** `uv run alembic upgrade head`
- **Rollback migration:** `uv run alembic downgrade -1`

## Configuration

All config is in `app/core/config.py` via `pydantic-settings`, reading from `.env`:
- `DB_ENGINE`: "sqlite" or "postgres"
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` for PostgreSQL

Database schema is managed by Alembic migrations. Run `uv run alembic upgrade head` to initialize or update the database.

## Conventions

- Use tabs for indentation
- Imports use absolute paths from project root (e.g., `from app.core.config import settings`)
- Repository methods are `@staticmethod` and receive `db: AsyncSession` as first argument
- Service functions raise `HTTPException` for business rule violations
