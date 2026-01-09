"""Notification repository for database operations."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:
    """Repository for notification database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_patient(
        self, patient_id: int, unread_only: bool = False
    ) -> list[Notification]:
        """Return notifications for a patient."""
        query = self.db.query(Notification).filter(
            Notification.patient_id == patient_id
        )
        if unread_only:
            query = query.filter(Notification.is_read.is_(False))
        return query.order_by(Notification.created_at.desc()).all()

    def mark_as_read(self, notification_id: int) -> Notification | None:
        """Mark a single notification as read."""
        notification = (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
        if notification is None:
            return None
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, patient_id: int) -> int:
        """Mark all notifications as read for a patient."""
        result = self.db.execute(
            update(Notification)
            .where(
                Notification.patient_id == patient_id,
                Notification.is_read.is_(False),
            )
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        self.db.commit()
        return result.rowcount or 0
