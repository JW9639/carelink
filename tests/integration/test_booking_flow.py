"""Integration test for booking flow."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

from app.services.appointment_service import AppointmentService
from app.utils.constants import AppointmentStatus


def test_booking_flow_creates_pending_appointment(test_db, test_patient, test_user):
    service = AppointmentService(test_db)
    scheduled = datetime.combine(
        date.today() + timedelta(days=1), time(9, 0), tzinfo=timezone.utc
    )

    appointment = service.create_appointment(
        patient_id=test_patient.id,
        scheduled_datetime=scheduled,
        duration_minutes=30,
        reason="Integration test booking",
        created_by_user_id=test_user.id,
    )

    assert appointment.id is not None
    assert appointment.status == AppointmentStatus.PENDING
