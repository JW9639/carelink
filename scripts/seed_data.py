"""Seed database with test data for development."""

from __future__ import annotations

import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from faker import Faker

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models import (
    Appointment,
    Bloodwork,
    Doctor,
    Notification,
    Patient,
    Prescription,
    User,
)
from app.security.auth import hash_password
from app.utils.constants import (
    AppointmentStatus,
    BookingSource,
    NotificationType,
    UserRole,
)

fake = Faker("en_GB")


def generate_valid_nhs_number() -> str:
    """Generate a valid NHS number with checksum."""
    while True:
        digits = [random.randint(0, 9) for _ in range(9)]
        weights = list(range(10, 1, -1))
        total = sum(d * w for d, w in zip(digits, weights))
        remainder = total % 11
        check_digit = (11 - remainder) % 11
        if check_digit == 10:
            continue
        return "".join(str(d) for d in digits) + str(check_digit)


def seed_users(db) -> dict[str, User]:
    """Create test users."""
    print("Creating users...")
    admin = User(
        email="admin@carelink.nhs.uk",
        hashed_password=hash_password("Admin123!"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    doctor_user = User(
        email="dr.johnson@carelink.nhs.uk",
        hashed_password=hash_password("Doctor123!"),
        role=UserRole.DOCTOR,
        is_active=True,
    )
    patient_user = User(
        email="patient@carelink.nhs.uk",
        hashed_password=hash_password("Patient123!"),
        role=UserRole.PATIENT,
        is_active=True,
    )
    db.add_all([admin, doctor_user, patient_user])
    db.commit()
    db.refresh(admin)
    db.refresh(doctor_user)
    db.refresh(patient_user)
    print("Users created successfully!")
    return {"admin": admin, "doctor": doctor_user, "patient": patient_user}


def seed_doctor(db, doctor_user: User) -> Doctor:
    """Create a doctor profile."""
    doctor = Doctor(
        user_id=doctor_user.id,
        gmc_number=str(random.randint(1000000, 9999999)),
        title="Dr",
        first_name="Jordan",
        last_name="Johnson",
        specialty="Cardiology",
        phone_number="07123456789",
        email=doctor_user.email,
        is_approved=True,
        approved_by=doctor_user.id,
        approved_at=datetime.now(timezone.utc),
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def seed_patient(db, patient_user: User, doctor: Doctor) -> Patient:
    """Create a patient profile."""
    patient = Patient(
        user_id=patient_user.id,
        nhs_number=generate_valid_nhs_number(),
        title="Ms",
        first_name="Emily",
        last_name="Carter",
        date_of_birth=date(1990, 4, 12),
        phone_number="07111111111",
        address_line_1="12 Elm Street",
        address_line_2=None,
        city="Belfast",
        postcode="BT12AB",
        emergency_contact_name="Sam Carter",
        emergency_contact_relationship="Sibling",
        emergency_contact_phone="07222222222",
        doctor_id=doctor.id,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def seed_appointments(db, patient: Patient, doctor: Doctor, admin: User) -> None:
    """Create sample appointments."""
    print("Creating appointments...")
    appointments = [
        Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            scheduled_datetime=datetime.now(timezone.utc) + timedelta(days=3),
            duration_minutes=30,
            status=AppointmentStatus.SCHEDULED,
            booking_source=BookingSource.ONLINE,
            reason="Annual checkup",
            created_by=admin.id,
        ),
        Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            scheduled_datetime=datetime.now(timezone.utc) - timedelta(days=10),
            duration_minutes=30,
            status=AppointmentStatus.COMPLETED,
            booking_source=BookingSource.PHONE,
            reason="Follow-up consultation",
            notes="Reviewed treatment plan",
            created_by=admin.id,
        ),
        Appointment(
            patient_id=patient.id,
            doctor_id=None,
            scheduled_datetime=datetime.now(timezone.utc) + timedelta(days=7),
            duration_minutes=60,
            status=AppointmentStatus.PENDING,
            booking_source=BookingSource.ONLINE,
            reason="New symptoms discussion",
            created_by=admin.id,
        ),
    ]
    db.add_all(appointments)
    db.commit()


def seed_bloodwork(db, patient: Patient, doctor: Doctor) -> None:
    """Create sample lab results."""
    print("Creating bloodwork results...")
    results_primary = {
        "test_name": "Full Blood Count & Metabolic Panel",
        "categories": [
            {
                "name": "Complete Blood Count (CBC)",
                "markers": [
                    {
                        "name": "White Blood Cell Count",
                        "abbreviation": "WBC",
                        "value": 7.2,
                        "unit": "x10^9/L",
                        "reference_range": {
                            "low": 4.0,
                            "optimal_low": 4.5,
                            "optimal_high": 11.0,
                            "high": 11.5,
                        },
                    },
                    {
                        "name": "Hemoglobin",
                        "abbreviation": "Hgb",
                        "value": 118,
                        "unit": "g/L",
                        "reference_range": {
                            "low": 130,
                            "optimal_low": 135,
                            "optimal_high": 170,
                            "high": 175,
                        },
                    },
                    {
                        "name": "Platelet Count",
                        "abbreviation": "PLT",
                        "value": 410,
                        "unit": "x10^9/L",
                        "reference_range": {
                            "low": 150,
                            "optimal_low": 170,
                            "optimal_high": 350,
                            "high": 400,
                        },
                    },
                ],
            },
            {
                "name": "Lipid Panel",
                "markers": [
                    {
                        "name": "Total Cholesterol",
                        "abbreviation": "TC",
                        "value": 5.8,
                        "unit": "mmol/L",
                        "reference_range": {
                            "low": 0.0,
                            "optimal_low": 0.0,
                            "optimal_high": 5.0,
                            "high": 6.2,
                        },
                    },
                    {
                        "name": "LDL Cholesterol",
                        "abbreviation": "LDL-C",
                        "value": 3.5,
                        "unit": "mmol/L",
                        "reference_range": {
                            "low": 0.0,
                            "optimal_low": 0.0,
                            "optimal_high": 3.0,
                            "high": 4.0,
                        },
                    },
                    {
                        "name": "HDL Cholesterol",
                        "abbreviation": "HDL-C",
                        "value": 0.9,
                        "unit": "mmol/L",
                        "reference_range": {
                            "low": 0.8,
                            "optimal_low": 1.0,
                            "optimal_high": 2.0,
                            "high": 2.4,
                        },
                    },
                ],
            },
        ],
    }

    results_secondary = {
        "test_name": "Kidney & Liver Function",
        "categories": [
            {
                "name": "Liver Function",
                "markers": [
                    {
                        "name": "Alanine Aminotransferase",
                        "abbreviation": "ALT",
                        "value": 48,
                        "unit": "U/L",
                        "reference_range": {
                            "low": 7,
                            "optimal_low": 10,
                            "optimal_high": 40,
                            "high": 56,
                        },
                    },
                    {
                        "name": "Alkaline Phosphatase",
                        "abbreviation": "ALP",
                        "value": 90,
                        "unit": "U/L",
                        "reference_range": {
                            "low": 30,
                            "optimal_low": 40,
                            "optimal_high": 120,
                            "high": 130,
                        },
                    },
                ],
            },
            {
                "name": "Kidney Function",
                "markers": [
                    {
                        "name": "Creatinine",
                        "abbreviation": "Cr",
                        "value": 108,
                        "unit": "umol/L",
                        "reference_range": {
                            "low": 59,
                            "optimal_low": 65,
                            "optimal_high": 100,
                            "high": 104,
                        },
                    }
                ],
            },
        ],
    }

    bloodwork_entries = [
        Bloodwork(
            patient_id=patient.id,
            test_type="Full Blood Count & Metabolic Panel",
            test_date=date.today() - timedelta(days=2),
            results=results_primary,
            reference_ranges={},
            notes="Discussed during follow-up.",
            is_published=True,
            published_at=datetime.now(timezone.utc) - timedelta(days=1),
            approved_by=doctor.id,
            approved_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        Bloodwork(
            patient_id=patient.id,
            test_type="Kidney & Liver Function",
            test_date=date.today() - timedelta(days=14),
            results=results_secondary,
            reference_ranges={},
            notes="Monitor ALT and creatinine trends.",
            is_published=True,
            published_at=datetime.now(timezone.utc) - timedelta(days=13),
            approved_by=doctor.id,
            approved_at=datetime.now(timezone.utc) - timedelta(days=13),
        ),
    ]
    db.add_all(bloodwork_entries)
    db.commit()


def seed_prescriptions(db, patient: Patient, doctor: Doctor) -> None:
    """Create sample prescriptions."""
    print("Creating prescriptions...")
    prescriptions = [
        Prescription(
            patient_id=patient.id,
            medication_name="Atorvastatin",
            dosage="10mg",
            frequency="Once daily",
            start_date=date.today() - timedelta(days=30),
            end_date=None,
            notes="Monitor cholesterol levels.",
            is_active=True,
            prescribed_by=doctor.id,
        ),
        Prescription(
            patient_id=patient.id,
            medication_name="Metformin",
            dosage="500mg",
            frequency="Twice daily",
            start_date=date.today() - timedelta(days=180),
            end_date=date.today() - timedelta(days=60),
            notes="Course completed.",
            is_active=False,
            prescribed_by=doctor.id,
            discontinued_by=doctor.id,
            discontinued_at=datetime.now(timezone.utc) - timedelta(days=60),
            discontinuation_reason="Course completed",
        ),
    ]
    db.add_all(prescriptions)
    db.commit()


def seed_notifications(db, patient: Patient, admin: User) -> None:
    """Create sample notifications."""
    print("Creating notifications...")
    notifications = [
        Notification(
            patient_id=patient.id,
            type=NotificationType.APPOINTMENT_REMINDER,
            title="Appointment Reminder",
            message="You have an appointment scheduled in 3 days.",
            is_read=False,
            triggered_by=admin.id,
        ),
        Notification(
            patient_id=patient.id,
            type=NotificationType.RESULTS_READY,
            title="Lab Results Ready",
            message="Your recent bloodwork results are ready to view.",
            is_read=False,
            triggered_by=admin.id,
        ),
        Notification(
            patient_id=patient.id,
            type=NotificationType.PRESCRIPTION_UPDATE,
            title="Prescription Updated",
            message="Your prescription has been updated by your clinician.",
            is_read=True,
            read_at=datetime.now(timezone.utc) - timedelta(days=2),
            triggered_by=admin.id,
        ),
    ]
    db.add_all(notifications)
    db.commit()


def main() -> None:
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping seed.")
            return

        users = seed_users(db)
        doctor = seed_doctor(db, users["doctor"])
        patient = seed_patient(db, users["patient"], doctor)
        seed_appointments(db, patient, doctor, users["admin"])
        seed_bloodwork(db, patient, doctor)
        seed_prescriptions(db, patient, doctor)
        seed_notifications(db, patient, users["admin"])

        print("\nDatabase seeded successfully!")
        print("\nTest Credentials:")
        print("  Admin:    admin@carelink.nhs.uk / Admin123!")
        print("  Doctor:   dr.johnson@carelink.nhs.uk / Doctor123!")
        print("  Patient:  patient@carelink.nhs.uk / Patient123!")
    except Exception as exc:
        print(f"Error seeding database: {exc}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
