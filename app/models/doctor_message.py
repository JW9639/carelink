"""Doctor message model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.doctor import Doctor
    from app.models.user import User


class DoctorMessage(TimestampMixin, Base):
    """Represents a message sent to a doctor by an admin."""

    __tablename__ = "doctor_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    sent_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="messages")
    sent_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="doctor_messages_sent",
        foreign_keys=[sent_by],
    )
