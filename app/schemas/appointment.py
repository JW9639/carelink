"""Appointment schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.constants import AppointmentStatus, BookingSource


class AppointmentBase(BaseModel):
    """Shared appointment fields."""

    scheduled_datetime: datetime
    duration_minutes: int
    reason: str | None = None


class AppointmentCreate(AppointmentBase):
    """Payload for creating an appointment."""

    patient_id: int
    doctor_id: int
    booking_source: BookingSource


class AppointmentResponse(AppointmentBase):
    """Response model including identifiers."""

    id: int
    patient_id: int
    doctor_id: int
    status: AppointmentStatus
    booking_source: BookingSource
    notes: str | None = None
    created_by: int
    cancelled_at: datetime | None = None
    cancellation_reason: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AppointmentCancel(BaseModel):
    """Payload for cancelling an appointment."""

    cancellation_reason: str
