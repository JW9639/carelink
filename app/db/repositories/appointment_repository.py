"""Appointment repository for database operations."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from app.models.appointment import Appointment
from app.utils.constants import AppointmentStatus


class AppointmentRepository:
    """Repository for appointment database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        """Get appointment by ID."""
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_patient_appointments(
        self,
        patient_id: int,
        status: AppointmentStatus | None = None,
        upcoming_only: bool = False,
    ) -> list[Appointment]:
        """Get appointments for a patient with optional filtering."""
        query = (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor))
            .filter(Appointment.patient_id == patient_id)
        )
        
        if status:
            query = query.filter(Appointment.status == status)
        
        if upcoming_only:
            query = query.filter(
                and_(
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status == AppointmentStatus.SCHEDULED,
                )
            )
        
        return query.order_by(Appointment.scheduled_datetime.asc()).all()

    def get_next_appointment(self, patient_id: int) -> Appointment | None:
        """Get the next upcoming appointment for a patient."""
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status == AppointmentStatus.SCHEDULED,
                )
            )
            .order_by(Appointment.scheduled_datetime.asc())
            .first()
        )

    def count_upcoming_appointments(self, patient_id: int) -> int:
        """Count upcoming scheduled appointments for a patient."""
        return (
            self.db.query(func.count(Appointment.id))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status == AppointmentStatus.SCHEDULED,
                )
            )
            .scalar()
        )

    def get_doctor_appointments(
        self,
        doctor_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Appointment]:
        """Get appointments for a doctor within a date range."""
        query = (
            self.db.query(Appointment)
            .options(joinedload(Appointment.patient))
            .filter(Appointment.doctor_id == doctor_id)
        )
        
        if date_from:
            query = query.filter(Appointment.scheduled_datetime >= date_from)
        if date_to:
            query = query.filter(Appointment.scheduled_datetime <= date_to)
        
        return query.order_by(Appointment.scheduled_datetime.asc()).all()
