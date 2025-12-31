"""Pytest fixtures for CareLink."""

from __future__ import annotations

import os
import uuid
from datetime import date

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401  # ensure models are registered
from app.db.base import Base
from app.models import Doctor, Patient, User
from app.security.auth import hash_password
from app.utils.constants import UserRole


@pytest.fixture(scope="session")
def test_engine():
    """Create an in-memory SQLite engine for tests."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_db(test_engine) -> Session:
    """Provide a database session for a test."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()


@pytest.fixture
def test_user(test_db: Session) -> User:
    """Create a sample patient user."""
    user = User(
        email=f"{uuid.uuid4()}@example.com",
        hashed_password=hash_password("Patient123!"),
        role=UserRole.PATIENT,
        is_active=True,
    )
    test_db.add(user)
    test_db.flush()
    return user


@pytest.fixture
def test_doctor(test_db: Session) -> Doctor:
    """Create a sample doctor."""
    user = User(
        email=f"{uuid.uuid4()}@example.com",
        hashed_password=hash_password("Doctor123!"),
        role=UserRole.DOCTOR,
        is_active=True,
    )
    test_db.add(user)
    test_db.flush()
    doctor = Doctor(
        user_id=user.id,
        gmc_number=str(uuid.uuid4().int)[:7],
        title="Dr",
        first_name="Test",
        last_name="Doctor",
        specialty="Cardiology",
        phone_number="07123456789",
        email=user.email,
    )
    test_db.add(doctor)
    test_db.flush()
    return doctor


@pytest.fixture
def test_patient(test_db: Session, test_user: User, test_doctor: Doctor) -> Patient:
    """Create a sample patient linked to user and doctor."""
    patient = Patient(
        user_id=test_user.id,
        nhs_number=str(uuid.uuid4().int)[:10],
        title="Mr",
        first_name="Test",
        last_name="Patient",
        date_of_birth=date(1990, 1, 1),
        phone_number="07111111111",
        address_line_1="1 Health Street",
        address_line_2=None,
        city="Belfast",
        postcode="BT12AB",
        emergency_contact_name="Jane Doe",
        emergency_contact_relationship="Spouse",
        emergency_contact_phone="07222222222",
        doctor_id=test_doctor.id,
    )
    test_db.add(patient)
    test_db.flush()
    return patient
