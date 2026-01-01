"""User model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.utils.constants import UserRole

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.notification import Notification
    from app.models.patient import Patient
    from app.models.doctor import Doctor
    from app.models.audit_log import AuditLog


class User(TimestampMixin, Base):
    """Represents an authenticated user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="userrole", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    patient: Mapped["Patient | None"] = relationship(
        "Patient", back_populates="user", uselist=False
    )
    doctor: Mapped["Doctor | None"] = relationship(
        "Doctor",
        back_populates="user",
        uselist=False,
        foreign_keys="Doctor.user_id",
    )
    appointments_created: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="created_by_user"
    )
    notifications_triggered: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="triggered_by_user"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )
