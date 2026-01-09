"""Doctor message repository for database operations."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload

from app.models.doctor_message import DoctorMessage


class DoctorMessageRepository:
    """Repository for doctor message database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_doctor(
        self, doctor_id: int, unread_only: bool = False
    ) -> list[DoctorMessage]:
        """Return messages for a doctor."""
        query = (
            self.db.query(DoctorMessage)
            .options(joinedload(DoctorMessage.sent_by_user))
            .filter(DoctorMessage.doctor_id == doctor_id)
        )
        if unread_only:
            query = query.filter(DoctorMessage.is_read.is_(False))
        return query.order_by(DoctorMessage.created_at.desc()).all()

    def create(
        self,
        doctor_id: int,
        title: str,
        message: str,
        sent_by: int | None = None,
    ) -> DoctorMessage:
        """Create a new doctor message."""
        message_record = DoctorMessage(
            doctor_id=doctor_id,
            title=title,
            message=message,
            sent_by=sent_by,
            is_read=False,
            read_at=None,
        )
        self.db.add(message_record)
        self.db.commit()
        self.db.refresh(message_record)
        return message_record

    def mark_as_read(self, message_id: int) -> DoctorMessage | None:
        """Mark a single message as read."""
        message = (
            self.db.query(DoctorMessage).filter(DoctorMessage.id == message_id).first()
        )
        if message is None:
            return None
        if not message.is_read:
            message.is_read = True
            message.read_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(message)
        return message

    def mark_all_as_read(self, doctor_id: int) -> int:
        """Mark all doctor messages as read."""
        result = self.db.execute(
            update(DoctorMessage)
            .where(
                DoctorMessage.doctor_id == doctor_id,
                DoctorMessage.is_read.is_(False),
            )
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        self.db.commit()
        return result.rowcount or 0
