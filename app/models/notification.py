"""Notification model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.utils.constants import NotificationType

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.user import User


class Notification(TimestampMixin, Base):
    """Represents a patient notification."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        Enum(
            NotificationType,
            name="notificationtype",
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        )
    )
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    action_url: Mapped[str | None] = mapped_column(String(255))
    triggered_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    patient: Mapped["Patient"] = relationship("Patient", back_populates="notifications")
    triggered_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="notifications_triggered"
    )
