"""Doctor model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.patient import Patient
    from app.models.appointment import Appointment
    from app.models.prescription import Prescription
    from app.models.bloodwork import Bloodwork


class Doctor(TimestampMixin, Base):
    """Represents a doctor profile."""

    __tablename__ = "doctors"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_doctor_user"),
        UniqueConstraint("gmc_number", name="uq_doctor_gmc_number"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    gmc_number: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    specialty: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship("User", back_populates="doctor")
    patients: Mapped[list["Patient"]] = relationship(
        "Patient", back_populates="doctor"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="doctor"
    )
    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription",
        back_populates="prescribed_by_doctor",
        foreign_keys="Prescription.prescribed_by",
    )
    bloodwork_reviews: Mapped[list["Bloodwork"]] = relationship(
        "Bloodwork", back_populates="approved_by_doctor"
    )
