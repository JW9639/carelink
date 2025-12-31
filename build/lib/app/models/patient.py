"""Patient model."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.doctor import Doctor
    from app.models.appointment import Appointment
    from app.models.prescription import Prescription
    from app.models.bloodwork import Bloodwork
    from app.models.notification import Notification


class Patient(TimestampMixin, Base):
    """Represents a patient profile."""

    __tablename__ = "patients"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_patient_user"),
        UniqueConstraint("nhs_number", name="uq_patient_nhs_number"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    nhs_number: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column()
    phone_number: Mapped[str] = mapped_column(String(20))
    address_line_1: Mapped[str] = mapped_column(String(255))
    address_line_2: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    postcode: Mapped[str] = mapped_column(String(10))
    emergency_contact_name: Mapped[str] = mapped_column(String(255))
    emergency_contact_relationship: Mapped[str] = mapped_column(String(50))
    emergency_contact_phone: Mapped[str] = mapped_column(String(20))
    doctor_id: Mapped[int | None] = mapped_column(ForeignKey("doctors.id"))

    user: Mapped["User"] = relationship("User", back_populates="patient")
    doctor: Mapped["Doctor | None"] = relationship(
        "Doctor", back_populates="patients"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="patient"
    )
    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription", back_populates="patient"
    )
    bloodwork_results: Mapped[list["Bloodwork"]] = relationship(
        "Bloodwork", back_populates="patient"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="patient"
    )
