"""Appointment repository for database operations."""

from __future__ import annotations

from datetime import datetime, timezone, date, timedelta

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.appointment import Appointment
from app.utils.constants import AppointmentStatus


class AppointmentRepository:
    """Repository for appointment database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, appointment: Appointment) -> Appointment:
        """Create a new appointment."""
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        """Get appointment by ID."""
        return (
            self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        )

    def get_booked_slots_for_date(self, target_date: date) -> list[Appointment]:
        """Get all booked appointment slots for a specific date."""
        start_of_day = datetime.combine(target_date, datetime.min.time()).replace(
            tzinfo=timezone.utc
        )
        end_of_day = datetime.combine(target_date, datetime.max.time()).replace(
            tzinfo=timezone.utc
        )

        return (
            self.db.query(Appointment)
            .filter(
                and_(
                    Appointment.scheduled_datetime >= start_of_day,
                    Appointment.scheduled_datetime <= end_of_day,
                    Appointment.status.in_(
                        [AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED]
                    ),
                )
            )
            .all()
        )

    def get_patient_appointments(
        self,
        patient_id: int,
        status: AppointmentStatus | None = None,
        upcoming_only: bool = False,
    ) -> list[Appointment]:
        """Get appointments for a patient with optional filtering."""
        from app.models.doctor import Doctor
        from app.models.user import User

        query = (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor).joinedload(Doctor.user))
            .filter(Appointment.patient_id == patient_id)
        )

        if status:
            query = query.filter(Appointment.status == status)

        if upcoming_only:
            query = query.filter(
                and_(
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status.in_(
                        [AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED]
                    ),
                )
            )

        return query.order_by(Appointment.scheduled_datetime.asc()).all()

    def get_next_appointment(self, patient_id: int) -> Appointment | None:
        """Get the next upcoming appointment for a patient (pending or scheduled)."""
        from app.models.doctor import Doctor

        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor).joinedload(Doctor.user))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status.in_(
                        [AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED]
                    ),
                )
            )
            .order_by(Appointment.scheduled_datetime.asc())
            .first()
        )

    def count_upcoming_appointments(self, patient_id: int) -> int:
        """Count upcoming scheduled/pending appointments for a patient."""
        return (
            self.db.query(func.count(Appointment.id))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    Appointment.scheduled_datetime >= datetime.now(timezone.utc),
                    Appointment.status.in_(
                        [AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED]
                    ),
                )
            )
            .scalar()
        )

    def get_pending_appointments(self) -> list[Appointment]:
        """Get all pending appointments awaiting doctor assignment (for admin)."""
        from app.models.patient import Patient

        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.patient).joinedload(Patient.user))
            .filter(Appointment.status == AppointmentStatus.PENDING)
            .order_by(Appointment.scheduled_datetime.asc())
            .all()
        )

    def assign_doctor(self, appointment_id: int, doctor_id: int) -> Appointment | None:
        """Assign a doctor to a pending appointment and update status to scheduled."""
        appointment = self.get_by_id(appointment_id)
        if appointment:
            appointment.doctor_id = doctor_id
            appointment.status = AppointmentStatus.SCHEDULED
            self.db.commit()
            self.db.refresh(appointment)
        return appointment

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

    def get_patient_past_appointments(
        self,
        patient_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Appointment]:
        """Get past/completed appointments for a patient with pagination."""
        from app.models.doctor import Doctor

        query = (
            self.db.query(Appointment)
            .options(joinedload(Appointment.doctor).joinedload(Doctor.user))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    or_(
                        Appointment.scheduled_datetime < datetime.now(timezone.utc),
                        Appointment.status.in_(
                            [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]
                        ),
                    ),
                )
            )
            .order_by(Appointment.scheduled_datetime.desc())
            .offset(offset)
        )

        if limit:
            query = query.limit(limit)

        return query.all()

    def count_patient_past_appointments(self, patient_id: int) -> int:
        """Count past/completed appointments for a patient."""
        return (
            self.db.query(func.count(Appointment.id))
            .filter(
                and_(
                    Appointment.patient_id == patient_id,
                    or_(
                        Appointment.scheduled_datetime < datetime.now(timezone.utc),
                        Appointment.status.in_(
                            [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]
                        ),
                    ),
                )
            )
            .scalar()
        )
