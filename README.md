# CareLink

CareLink is a role-based patient and doctor dashboard for integrated patient
management and hybrid appointment booking built with Streamlit, PostgreSQL,
SQLAlchemy 2.0, and Pydantic.

## Features

- Role-based access for patients, doctors, and admins
- Authentication with bcrypt hashing and session management
- Auditable actions and RBAC enforcement
- PostgreSQL persistence with Alembic migrations
- Streamlit UI with NHS-inspired theming

## Tech Stack

- Python 3.11+
- Streamlit + streamlit-authenticator
- SQLAlchemy 2.0, Alembic
- PostgreSQL
- Pydantic v2, pydantic-settings
- Docker & Docker Compose

## Prerequisites

- Python 3.11+
- Docker and Docker Compose

## Quick Start

1. Copy environment template: `cp .env.example .env`
2. Build and start services: `docker-compose up --build`
3. Visit `http://localhost:8501` for the Streamlit app.

## Development Setup

1. Create a virtual environment and install deps: `pip install .[dev]`
2. Run formatting and linting:
   - `black --check app tests`
   - `flake8 app tests`
3. Apply migrations (after configuring DB): `alembic upgrade head`

## Running Tests

- Unit tests with coverage: `pytest`

## Project Structure

See the `app/` package for application code, `migrations/` for Alembic scripts,
`tests/` for automated tests, and `docs/` for project documentation.

## Contributing

Contributions welcome. Please open an issue or merge request before major
changes.

## License

License to be determined.
