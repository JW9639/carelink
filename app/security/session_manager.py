"""Streamlit session state helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import streamlit as st

from app.config import get_settings
from app.schemas.user import UserResponse

settings = get_settings()


def init_session_state() -> None:
    """Initialize session state keys."""
    defaults: dict[str, Any] = {
        "user": None,
        "role": None,
        "last_activity": None,
        "is_authenticated": False,
        "session_timeout_minutes": settings.SESSION_TIMEOUT_MINUTES,
        "user_name": "Unknown",
        "sidebar_open": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_user(user: UserResponse) -> None:
    """Store the authenticated user in session state."""
    role_value = user.role.value if hasattr(user.role, "value") else user.role
    st.session_state.user = user
    st.session_state.role = role_value
    st.session_state.is_authenticated = True
    st.session_state.user_name = user.email
    update_last_activity()


def get_current_user() -> UserResponse | None:
    """Return the current authenticated user."""
    return st.session_state.get("user")


def clear_session() -> None:
    """Clear all session data."""
    st.session_state.clear()
    init_session_state()


def check_session_timeout() -> bool:
    """Check if the session is still valid based on inactivity."""
    last_activity: datetime | None = st.session_state.get("last_activity")
    if last_activity is None:
        return False
    timeout_at = last_activity + timedelta(
        minutes=st.session_state.get(
            "session_timeout_minutes", settings.SESSION_TIMEOUT_MINUTES
        )
    )
    if datetime.now(timezone.utc) > timeout_at:
        clear_session()
        return False
    return True


def update_last_activity() -> None:
    """Update the last activity timestamp."""
    st.session_state.last_activity = datetime.now(timezone.utc)
