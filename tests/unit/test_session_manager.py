"""Tests for Streamlit session manager utilities."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import streamlit as st

from app.security import session_manager
from app.schemas.user import UserResponse
from app.utils.constants import UserRole


def _reset_state() -> None:
    st.session_state.clear()
    session_manager.init_session_state()


def test_set_and_get_user():
    _reset_state()
    user = UserResponse(
        id=1,
        email="patient@example.com",
        role=UserRole.PATIENT,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    session_manager.set_user(user)
    assert session_manager.get_current_user() == user
    assert st.session_state.is_authenticated is True
    assert st.session_state.role == UserRole.PATIENT.value
    assert st.session_state.user_name == "patient@example.com"


def test_session_timeout_logic():
    _reset_state()
    assert session_manager.check_session_timeout() is False

    session_manager.update_last_activity()
    assert session_manager.check_session_timeout() is True

    st.session_state.last_activity = datetime.now(timezone.utc) - timedelta(minutes=120)
    assert session_manager.check_session_timeout() is False


def test_clear_session():
    _reset_state()
    st.session_state.user = "test"
    session_manager.clear_session()
    assert st.session_state.user is None
    assert st.session_state.is_authenticated is False
