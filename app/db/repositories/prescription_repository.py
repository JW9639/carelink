"""Prescription repository for database operations."""

from __future__ import annotations

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from app.models.prescription import Prescription


class PrescriptionRepository:
    """Repository for prescription database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active_for_patient(self, patient_id: int) -> list[Prescription]:
        """Return active prescriptions for a patient."""
        return (
            self.db.query(Prescription)
            .options(joinedload(Prescription.prescribed_by_doctor))
            .filter(
                and_(
                    Prescription.patient_id == patient_id,
                    Prescription.is_active.is_(True),
                )
            )
            .order_by(Prescription.start_date.desc())
            .all()
        )

    def get_history_for_patient(self, patient_id: int) -> list[Prescription]:
        """Return inactive prescriptions for a patient."""
        return (
            self.db.query(Prescription)
            .options(joinedload(Prescription.prescribed_by_doctor))
            .filter(
                and_(
                    Prescription.patient_id == patient_id,
                    Prescription.is_active.is_(False),
                )
            )
            .order_by(Prescription.end_date.desc())
            .all()
        )
