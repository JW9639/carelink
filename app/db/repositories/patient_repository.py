"""Patient repository for database operations."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.bloodwork import Bloodwork
from app.models.notification import Notification
from app.models.patient import Patient
from app.models.prescription import Prescription


class PatientRepository:
    """Repository for patient database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, patient_id: int) -> Patient | None:
        """Get patient by ID."""
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def get_by_user_id(self, user_id: int) -> Patient | None:
        """Get patient by user ID."""
        return (
            self.db.query(Patient)
            .options(joinedload(Patient.user))
            .filter(Patient.user_id == user_id)
            .first()
        )

    def get_by_doctor_id(self, doctor_id: int) -> list[Patient]:
        """Get patients assigned to a doctor."""
        return (
            self.db.query(Patient)
            .options(joinedload(Patient.user))
            .filter(Patient.doctor_id == doctor_id)
            .order_by(Patient.last_name.asc(), Patient.first_name.asc())
            .all()
        )

    def get_active_prescriptions_count(self, patient_id: int) -> int:
        """Count active prescriptions for a patient."""
        return (
            self.db.query(func.count(Prescription.id))
            .filter(
                Prescription.patient_id == patient_id,
                Prescription.is_active.is_(True),
            )
            .scalar()
        )

    def get_pending_results_count(self, patient_id: int) -> int:
        """Count pending (unpublished) bloodwork results for a patient."""
        return (
            self.db.query(func.count(Bloodwork.id))
            .filter(
                Bloodwork.patient_id == patient_id,
                Bloodwork.is_published.is_(False),
            )
            .scalar()
        )

    def get_unread_notifications_count(self, patient_id: int) -> int:
        """Count unread notifications for a patient."""
        return (
            self.db.query(func.count(Notification.id))
            .filter(
                Notification.patient_id == patient_id,
                Notification.is_read.is_(False),
            )
            .scalar()
        )

    def get_active_prescriptions(self, patient_id: int) -> list[Prescription]:
        """Get active prescriptions for a patient."""
        return (
            self.db.query(Prescription)
            .options(joinedload(Prescription.prescribed_by_doctor))
            .filter(
                Prescription.patient_id == patient_id,
                Prescription.is_active.is_(True),
            )
            .order_by(Prescription.start_date.desc())
            .all()
        )

    def get_recent_bloodwork(self, patient_id: int, limit: int = 5) -> list[Bloodwork]:
        """Get recent bloodwork results for a patient."""
        return (
            self.db.query(Bloodwork)
            .filter(
                Bloodwork.patient_id == patient_id,
                Bloodwork.is_published.is_(True),
            )
            .order_by(Bloodwork.test_date.desc())
            .limit(limit)
            .all()
        )

    def get_notifications(
        self, patient_id: int, unread_only: bool = False, limit: int = 10
    ) -> list[Notification]:
        """Get notifications for a patient."""
        query = self.db.query(Notification).filter(
            Notification.patient_id == patient_id
        )

        if unread_only:
            query = query.filter(Notification.is_read.is_(False))

        return query.order_by(Notification.created_at.desc()).limit(limit).all()
