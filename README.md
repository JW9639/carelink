# CareLink

[![pipeline status](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/badges/main/pipeline.svg)](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/-/pipelines)
[![coverage report](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/badges/main/coverage.svg)](https://gitlab-se.eeecs.qub.ac.uk/40365072/carelink_2/-/pipelines)

CareLink is a role-based patient, doctor, and admin portal built with Streamlit and PostgreSQL.

## Quick Start

1. Copy the env template: `cp .env.example .env`
2. Generate a secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. Set `SECRET_KEY` in `.env`
4. Start services: `docker-compose up --build`
5. Seed demo data: `docker-compose exec app python scripts/seed_data.py`
6. Open `http://localhost:8501`

## Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@carelink.nhs.uk | Admin123! |
| Doctor | dr.johnson@carelink.nhs.uk | Doctor123! |
| Patient | patient@carelink.nhs.uk | Patient123! |

## Dev Notes

- Install dev deps: `pip install .[dev]`
- Lint: `black --check app tests` and `flake8 app tests`
- Tests: `pytest`
- Security: `bandit -r app`
