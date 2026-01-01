"""Patient service for business logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.repositories.appointment_repository import AppointmentRepository
from app.db.repositories.patient_repository import PatientRepository
from app.models.appointment import Appointment
from app.models.patient import Patient


@dataclass
class DashboardStats:
    """Data class for patient dashboard statistics."""

    upcoming_appointments: int
    active_prescriptions: int
    pending_results: int
    unread_notifications: int


@dataclass
class NextAppointmentInfo:
    """Data class for next appointment display."""

    doctor_name: str
    specialty: str
    scheduled_datetime: datetime
    reason: str | None


class PatientService:
    """Service for patient-related business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.patient_repo = PatientRepository(db)
        self.appointment_repo = AppointmentRepository(db)

    def get_patient_by_user_id(self, user_id: int) -> Patient | None:
        """Get patient profile by user ID."""
        return self.patient_repo.get_by_user_id(user_id)

    def get_dashboard_stats(self, patient_id: int) -> DashboardStats:
        """Get all dashboard statistics for a patient."""
        return DashboardStats(
            upcoming_appointments=self.appointment_repo.count_upcoming_appointments(
                patient_id
            ),
            active_prescriptions=self.patient_repo.get_active_prescriptions_count(
                patient_id
            ),
            pending_results=self.patient_repo.get_pending_results_count(patient_id),
            unread_notifications=self.patient_repo.get_unread_notifications_count(
                patient_id
            ),
        )

    def get_next_appointment_info(
        self, patient_id: int
    ) -> NextAppointmentInfo | None:
        """Get formatted info for next upcoming appointment."""
        appointment = self.appointment_repo.get_next_appointment(patient_id)
        
        if not appointment or not appointment.doctor:
            return None
        
        doctor = appointment.doctor
        return NextAppointmentInfo(
            doctor_name=f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
            specialty=doctor.specialty,
            scheduled_datetime=appointment.scheduled_datetime,
            reason=appointment.reason,
        )

    def get_upcoming_appointments(self, patient_id: int) -> list[Appointment]:
        """Get all upcoming appointments for a patient."""
        return self.appointment_repo.get_patient_appointments(
            patient_id, upcoming_only=True
        )
