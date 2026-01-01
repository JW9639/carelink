"""Appointment model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.utils.constants import AppointmentStatus, BookingSource

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.doctor import Doctor
    from app.models.user import User


class Appointment(TimestampMixin, Base):
    """Represents an appointment between a patient and doctor."""

    __tablename__ = "appointments"
    __table_args__ = (
        Index("idx_appointments_scheduled", "scheduled_datetime"),
        Index("idx_appointments_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int | None] = mapped_column(
        ForeignKey("doctors.id"), nullable=True
    )  # Nullable for pending appointments
    scheduled_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name="appointmentstatus",
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=AppointmentStatus.PENDING,
    )
    booking_source: Mapped[BookingSource] = mapped_column(
        Enum(
            BookingSource,
            name="bookingsource",
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=BookingSource.ONLINE,
    )
    reason: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancellation_reason: Mapped[str | None] = mapped_column(Text)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="appointments")
    doctor: Mapped["Doctor | None"] = relationship(
        "Doctor", back_populates="appointments"
    )
    created_by_user: Mapped["User"] = relationship(
        "User", back_populates="appointments_created"
    )
