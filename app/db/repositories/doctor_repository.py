"""Doctor repository for database operations."""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.doctor import Doctor


class DoctorRepository:
    """Repository for doctor database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, doctor_id: int) -> Doctor | None:
        """Get doctor by ID."""
        return (
            self.db.query(Doctor)
            .options(joinedload(Doctor.user))
            .filter(Doctor.id == doctor_id)
            .first()
        )

    def get_by_user_id(self, user_id: int) -> Doctor | None:
        """Get doctor by user ID."""
        return (
            self.db.query(Doctor)
            .options(joinedload(Doctor.user))
            .filter(Doctor.user_id == user_id)
            .first()
        )

    def get_all_approved(self) -> list[Doctor]:
        """Get all approved doctors."""
        return (
            self.db.query(Doctor)
            .options(joinedload(Doctor.user))
            .filter(Doctor.is_approved == True)
            .all()
        )

    def get_all(self) -> list[Doctor]:
        """Get all doctors."""
        return (
            self.db.query(Doctor)
            .options(joinedload(Doctor.user))
            .all()
        )
