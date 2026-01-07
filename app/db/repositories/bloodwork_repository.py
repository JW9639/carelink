"""Bloodwork repository for database operations."""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.bloodwork import Bloodwork


class BloodworkRepository:
    """Repository for bloodwork database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_published_for_patient(self, patient_id: int) -> list[Bloodwork]:
        """Return published bloodwork results for a patient."""
        return (
            self.db.query(Bloodwork)
            .options(joinedload(Bloodwork.approved_by_doctor))
            .filter(
                Bloodwork.patient_id == patient_id,
                Bloodwork.is_published.is_(True),
            )
            .order_by(Bloodwork.test_date.desc())
            .all()
        )

    def get_by_id(self, bloodwork_id: int) -> Bloodwork | None:
        """Return a bloodwork result by ID."""
        return (
            self.db.query(Bloodwork)
            .options(joinedload(Bloodwork.approved_by_doctor))
            .filter(Bloodwork.id == bloodwork_id)
            .first()
        )
