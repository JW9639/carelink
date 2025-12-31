"""Domain enums and application constants."""

from __future__ import annotations

from enum import Enum


class UserRole(str, Enum):
    """Supported user roles."""

    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class AppointmentStatus(str, Enum):
    """Appointment statuses."""

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class BookingSource(str, Enum):
    """Appointment booking sources."""

    ONLINE = "online"
    PHONE = "phone"


class NotificationType(str, Enum):
    """Notification types."""

    APPOINTMENT_REMINDER = "appointment_reminder"
    RESULTS_READY = "results_ready"
    FOLLOW_UP = "follow_up"
    PRESCRIPTION_UPDATE = "prescription_update"
    GENERAL = "general"


SESSION_TIMEOUT_MINUTES = 15
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30
ITEMS_PER_PAGE = 7
