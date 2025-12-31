"""Role-based access control utilities."""

from __future__ import annotations

from enum import Enum
from functools import wraps
from typing import Callable, Iterable

import streamlit as st

from app.security import session_manager
from app.utils.constants import UserRole


class Permission(str, Enum):
    """Application permissions."""

    VIEW_OWN_RECORDS = "view_own_records"
    VIEW_PATIENT_RECORDS = "view_patient_records"
    PUBLISH_RESULTS = "publish_results"
    MANAGE_APPOINTMENTS = "manage_appointments"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOG = "view_audit_log"
    MANAGE_PRESCRIPTIONS = "manage_prescriptions"
    MANAGE_NOTIFICATIONS = "manage_notifications"
    VIEW_DASHBOARD = "view_dashboard"


ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.PATIENT: {
        Permission.VIEW_OWN_RECORDS,
        Permission.MANAGE_APPOINTMENTS,
        Permission.VIEW_DASHBOARD,
        Permission.MANAGE_NOTIFICATIONS,
    },
    UserRole.DOCTOR: {
        Permission.VIEW_PATIENT_RECORDS,
        Permission.PUBLISH_RESULTS,
        Permission.MANAGE_APPOINTMENTS,
        Permission.MANAGE_PRESCRIPTIONS,
        Permission.VIEW_DASHBOARD,
    },
    UserRole.ADMIN: set(Permission),
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a given permission."""
    if role is UserRole.ADMIN:
        return True
    allowed = ROLE_PERMISSIONS.get(role, set())
    return permission in allowed


def _user_role() -> UserRole | None:
    user_role = st.session_state.get("role")
    if user_role is None:
        return None
    try:
        return UserRole(user_role)
    except ValueError:
        return None


def require_permission(permission: Permission) -> Callable:
    """Decorator enforcing a permission on a Streamlit page."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = _user_role()
            if role is None or not has_permission(role, permission):
                st.error("You do not have permission to view this page.")
                st.stop()
            session_manager.update_last_activity()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_role(allowed_roles: Iterable[UserRole]) -> Callable:
    """Decorator enforcing allowed roles on a page."""

    allowed_set = {UserRole(role) for role in allowed_roles}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = _user_role()
            if role is None or role not in allowed_set:
                st.error("You do not have access to this page.")
                st.stop()
            session_manager.update_last_activity()
            return func(*args, **kwargs)

        return wrapper

    return decorator
