"""Doctor message service for business logic."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.doctor_message_repository import DoctorMessageRepository
from app.models.doctor_message import DoctorMessage


class DoctorMessageService:
    """Service for doctor message business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.message_repo = DoctorMessageRepository(db)

    def get_messages(
        self, doctor_id: int, unread_only: bool = False
    ) -> list[DoctorMessage]:
        """Return messages for a doctor."""
        return self.message_repo.get_for_doctor(
            doctor_id=doctor_id, unread_only=unread_only
        )

    def send_message(
        self,
        doctor_id: int,
        title: str,
        message: str,
        sent_by: int | None = None,
    ) -> DoctorMessage:
        """Send a message to a doctor."""
        return self.message_repo.create(
            doctor_id=doctor_id,
            title=title,
            message=message,
            sent_by=sent_by,
        )

    def mark_as_read(self, message_id: int) -> DoctorMessage | None:
        """Mark a message as read."""
        return self.message_repo.mark_as_read(message_id)

    def mark_all_as_read(self, doctor_id: int) -> int:
        """Mark all messages as read."""
        return self.message_repo.mark_all_as_read(doctor_id)
