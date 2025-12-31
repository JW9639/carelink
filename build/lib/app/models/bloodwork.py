"""Bloodwork model."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.doctor import Doctor


class Bloodwork(TimestampMixin, Base):
    """Represents a bloodwork or lab result."""

    __tablename__ = "bloodwork"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    test_type: Mapped[str] = mapped_column(String(255))
    test_date: Mapped[date] = mapped_column(Date)
    results: Mapped[dict] = mapped_column(JSON)
    reference_ranges: Mapped[dict] = mapped_column(JSON)
    notes: Mapped[str | None] = mapped_column(Text)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("doctors.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    patient: Mapped["Patient"] = relationship(
        "Patient", back_populates="bloodwork_results"
    )
    approved_by_doctor: Mapped["Doctor | None"] = relationship(
        "Doctor", back_populates="bloodwork_reviews"
    )
