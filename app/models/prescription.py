"""Prescription model."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.doctor import Doctor


class Prescription(TimestampMixin, Base):
    """Represents a prescription for a patient."""

    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    medication_name: Mapped[str] = mapped_column(String(255))
    dosage: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    prescribed_by: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    discontinued_by: Mapped[int | None] = mapped_column(ForeignKey("doctors.id"))
    discontinued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    discontinuation_reason: Mapped[str | None] = mapped_column(Text)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="prescriptions")
    prescribed_by_doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="prescriptions",
        foreign_keys=[prescribed_by],
    )
    discontinued_by_doctor: Mapped["Doctor | None"] = relationship(
        "Doctor",
        foreign_keys=[discontinued_by],
    )
