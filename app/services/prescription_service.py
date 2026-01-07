"""Prescription service for business logic."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.prescription_repository import PrescriptionRepository
from app.models.prescription import Prescription


class PrescriptionService:
    """Service for prescription-related business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.prescription_repo = PrescriptionRepository(db)

    def get_active_prescriptions(self, patient_id: int) -> list[Prescription]:
        """Return active prescriptions for a patient."""
        return self.prescription_repo.get_active_for_patient(patient_id)

    def get_prescription_history(self, patient_id: int) -> list[Prescription]:
        """Return inactive prescriptions for a patient."""
        return self.prescription_repo.get_history_for_patient(patient_id)
