"""Appointment service for business logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, time

from sqlalchemy.orm import Session

from app.db.repositories.appointment_repository import AppointmentRepository
from app.models.appointment import Appointment
from app.utils.constants import AppointmentStatus, BookingSource


@dataclass
class TimeSlot:
    """Represents an available time slot."""

    time: time
    display: str
    is_available: bool


class AppointmentService:
    """Service for appointment business logic."""

    # Clinic hours: 9 AM to 5 PM
    CLINIC_START_HOUR = 9
    CLINIC_END_HOUR = 17

    def __init__(self, db: Session) -> None:
        self.db = db
        self.appointment_repo = AppointmentRepository(db)

    def get_available_slots(
        self, target_date: date, duration_minutes: int = 30
    ) -> tuple[list[TimeSlot], list[TimeSlot]]:
        """
        Get available time slots for a date, split into AM and PM.

        Returns:
            Tuple of (am_slots, pm_slots)
        """
        # Get already booked slots for the date
        booked_appointments = self.appointment_repo.get_booked_slots_for_date(
            target_date
        )
        booked_times = set()

        for appt in booked_appointments:
            # Mark the appointment time as booked
            booked_times.add(appt.scheduled_datetime.time())

        am_slots = []
        pm_slots = []

        # Generate slots from clinic start to end
        current_hour = self.CLINIC_START_HOUR
        current_minute = 0

        while current_hour < self.CLINIC_END_HOUR or (
            current_hour == self.CLINIC_END_HOUR and current_minute == 0
        ):
            slot_time = time(hour=current_hour, minute=current_minute)

            # Check if this slot is in the past for today
            is_past = False
            if target_date == date.today():
                now = datetime.now()
                slot_datetime = datetime.combine(target_date, slot_time)
                is_past = slot_datetime <= now

            # Check if slot is booked
            is_booked = slot_time in booked_times
            is_available = not is_booked and not is_past

            # Format display time
            display_hour = current_hour if current_hour <= 12 else current_hour - 12
            if display_hour == 0:
                display_hour = 12
            am_pm = "AM" if current_hour < 12 else "PM"
            display = f"{display_hour}:{current_minute:02d} {am_pm}"

            slot = TimeSlot(time=slot_time, display=display, is_available=is_available)

            if current_hour < 12:
                am_slots.append(slot)
            else:
                pm_slots.append(slot)

            # Move to next slot
            current_minute += duration_minutes
            if current_minute >= 60:
                current_hour += 1
                current_minute = 0

        return am_slots, pm_slots

    def create_appointment(
        self,
        patient_id: int,
        scheduled_datetime: datetime,
        duration_minutes: int,
        reason: str,
        created_by_user_id: int,
    ) -> Appointment:
        """Create a new pending appointment."""
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=None,  # Will be assigned by admin
            scheduled_datetime=scheduled_datetime,
            duration_minutes=duration_minutes,
            status=AppointmentStatus.PENDING,
            booking_source=BookingSource.ONLINE,
            reason=reason,
            created_by=created_by_user_id,
        )
        return self.appointment_repo.create(appointment)

    def get_patient_upcoming_appointments(self, patient_id: int) -> list[Appointment]:
        """Get upcoming appointments for a patient."""
        return self.appointment_repo.get_patient_appointments(
            patient_id=patient_id, upcoming_only=True
        )

    def get_next_appointment(self, patient_id: int) -> Appointment | None:
        """Get the next upcoming appointment for a patient."""
        return self.appointment_repo.get_next_appointment(patient_id)

    def get_pending_appointments(self) -> list[Appointment]:
        """Get all pending appointments (for admin view)."""
        return self.appointment_repo.get_pending_appointments()

    def assign_doctor_to_appointment(
        self, appointment_id: int, doctor_id: int
    ) -> Appointment | None:
        """Assign a doctor to a pending appointment."""
        return self.appointment_repo.assign_doctor(appointment_id, doctor_id)

    def get_patient_past_appointments(
        self,
        patient_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Appointment]:
        """Get past/completed appointments for a patient with pagination."""
        return self.appointment_repo.get_patient_past_appointments(
            patient_id=patient_id,
            limit=limit,
            offset=offset,
        )

    def count_patient_past_appointments(self, patient_id: int) -> int:
        """Count past/completed appointments for a patient."""
        return self.appointment_repo.count_patient_past_appointments(patient_id)
