"""Bloodwork repository for database operations."""

from __future__ import annotations

from datetime import date, datetime

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

    def create(
        self,
        patient_id: int,
        test_type: str,
        test_date: date,
        results: dict,
        reference_ranges: dict,
        notes: str | None = None,
        is_published: bool = False,
        approved_by: int | None = None,
        approved_at: datetime | None = None,
        published_at: datetime | None = None,
    ) -> Bloodwork:
        """Create a bloodwork result."""
        bloodwork = Bloodwork(
            patient_id=patient_id,
            test_type=test_type,
            test_date=test_date,
            results=results,
            reference_ranges=reference_ranges,
            notes=notes,
            is_published=is_published,
            approved_by=approved_by,
            approved_at=approved_at,
            published_at=published_at,
        )
        self.db.add(bloodwork)
        self.db.commit()
        self.db.refresh(bloodwork)
        return bloodwork

    def save(self, bloodwork: Bloodwork) -> Bloodwork:
        """Persist changes to a bloodwork result."""
        self.db.add(bloodwork)
        self.db.commit()
        self.db.refresh(bloodwork)
        return bloodwork
