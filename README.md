# CareLink

[![pipeline status](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/badges/main/pipeline.svg)](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/-/pipelines)
[![coverage report](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/badges/main/coverage.svg)](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/-/pipelines)

CareLink is a role-based patient, doctor, and admin portal built with Streamlit and PostgreSQL.

## Tech Stack

- Python 3.11+
- Streamlit
- SQLAlchemy 2.0, Alembic
- PostgreSQL
- Pydantic v2, pydantic-settings
- Docker & Docker Compose
- bcrypt

## Prerequisites

- Python 3.11+
- Docker and Docker Compose

## Quick Start

1. Copy the env template: `cp .env.example .env`
2. Generate a secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. Set `SECRET_KEY` in `.env`
4. Start services: `docker-compose up --build`
5. Seed demo data: `docker-compose exec app python scripts/seed_data.py`
6. Open `http://localhost:8501`

## Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@carelink.nhs.uk | Admin123! |
| Doctor | dr.johnson@carelink.nhs.uk | Doctor123! |
| Patient | patient@carelink.nhs.uk | Patient123! |

## Development Setup

1. Create a virtual environment and install deps: `pip install .[dev]`
2. Run formatting and linting:
   - `black --check app tests`
   - `flake8 app tests`
3. Run security checks: `bandit -r app`
4. Apply migrations (after configuring DB): `alembic upgrade head`

## Running Tests

- Unit tests with coverage: `pytest`
- Coverage XML (CI-compatible): `pytest --cov-report=xml:coverage.xml`
