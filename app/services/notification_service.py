"""Notification service for business logic."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.notification_repository import NotificationRepository
from app.models.notification import Notification


class NotificationService:
    """Service for notification-related business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.notification_repo = NotificationRepository(db)

    def get_notifications(
        self, patient_id: int, unread_only: bool = False
    ) -> list[Notification]:
        """Return notifications for a patient."""
        return self.notification_repo.get_for_patient(
            patient_id=patient_id, unread_only=unread_only
        )

    def mark_as_read(self, notification_id: int) -> Notification | None:
        """Mark a notification as read."""
        return self.notification_repo.mark_as_read(notification_id)

    def mark_all_as_read(self, patient_id: int) -> int:
        """Mark all notifications as read for a patient."""
        return self.notification_repo.mark_all_as_read(patient_id)
