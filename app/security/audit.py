"""Audit logging utilities."""

from __future__ import annotations

import functools
from enum import Enum
from typing import Any, Callable

import streamlit as st
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditAction(str, Enum):
    """Common audit actions."""

    LOGIN = "login"
    LOGOUT = "logout"
    VIEW_RECORD = "view_record"
    UPDATE_RECORD = "update_record"
    CREATE_RECORD = "create_record"
    DELETE_RECORD = "delete_record"
    PUBLISH_RESULTS = "publish_results"
    BOOK_APPOINTMENT = "book_appointment"
    CANCEL_APPOINTMENT = "cancel_appointment"


def log_action(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int | None,
    details: dict[str, Any] | None = None,
) -> None:
    """Persist an audit log entry."""
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {},
        ip_address=st.session_state.get("ip_address"),
        user_agent=st.session_state.get("user_agent"),
    )
    db.add(entry)
    db.flush()


def audit_log(action: str, resource_type: str) -> Callable:
    """Decorator to log function executions."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            db = kwargs.get("db") or next(
                (arg for arg in args if isinstance(arg, Session)), None
            )
            if db is None:
                return result

            user = st.session_state.get("user")
            user_id = getattr(user, "id", None)
            if user_id is None:
                return result

            sanitized: dict[str, Any] = {}
            for key, value in kwargs.items():
                if "password" in key or isinstance(value, Session):
                    continue
                if isinstance(value, (str, int, float, bool, type(None), list, dict)):
                    sanitized[key] = value
                else:
                    sanitized[key] = str(value)
            log_action(
                db=db,
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=sanitized.get("resource_id"),
                details=sanitized,
            )
            return result

        return wrapper

    return decorator
