"""Tests for appointment service."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

import pytest

from app.models.appointment import Appointment
from app.services.appointment_service import AppointmentService
from app.utils.constants import AppointmentStatus, BookingSource


def test_get_available_slots_blocks_overlaps(test_db, test_patient, test_doctor, test_user):
    target_date = date.today() + timedelta(days=1)
    scheduled = datetime.combine(target_date, time(10, 0), tzinfo=timezone.utc)
    appointment = Appointment(
        patient_id=test_patient.id,
        doctor_id=test_doctor.id,
        scheduled_datetime=scheduled,
        duration_minutes=60,
        status=AppointmentStatus.SCHEDULED,
        booking_source=BookingSource.ONLINE,
        reason="Test",
        created_by=test_user.id,
    )
    test_db.add(appointment)
    test_db.commit()

    service = AppointmentService(test_db)
    am_slots, pm_slots = service.get_available_slots(target_date, duration_minutes=30)
    slot_map = {slot.time: slot for slot in am_slots + pm_slots}

    assert slot_map[time(10, 0)].is_available is False
    assert slot_map[time(10, 30)].is_available is False


def test_create_appointment_conflict_raises(test_db, test_patient, test_user):
    target_date = date.today() + timedelta(days=2)
    scheduled = datetime.combine(target_date, time(9, 0), tzinfo=timezone.utc)
    existing = Appointment(
        patient_id=test_patient.id,
        doctor_id=None,
        scheduled_datetime=scheduled,
        duration_minutes=30,
        status=AppointmentStatus.PENDING,
        booking_source=BookingSource.ONLINE,
        reason="Existing",
        created_by=test_user.id,
    )
    test_db.add(existing)
    test_db.commit()

    service = AppointmentService(test_db)

    with pytest.raises(ValueError, match="Selected time is no longer available."):
        service.create_appointment(
            patient_id=test_patient.id,
            scheduled_datetime=scheduled,
            duration_minutes=30,
            reason="Conflicting",
            created_by_user_id=test_user.id,
        )
