"""Tests for RBAC helper functions."""

import streamlit as st
import pytest

from app.security import session_manager
from app.security.rbac import (
    Permission,
    has_permission,
    require_permission,
    require_role,
)
from app.utils.constants import UserRole


def test_patient_permissions():
    assert has_permission(UserRole.PATIENT, Permission.VIEW_OWN_RECORDS)
    assert not has_permission(UserRole.PATIENT, Permission.MANAGE_USERS)


def test_doctor_permissions():
    assert has_permission(UserRole.DOCTOR, Permission.VIEW_PATIENT_RECORDS)
    assert has_permission(UserRole.DOCTOR, Permission.MANAGE_APPOINTMENTS)
    assert not has_permission(UserRole.DOCTOR, Permission.MANAGE_USERS)


def test_admin_permissions():
    for permission in Permission:
        assert has_permission(UserRole.ADMIN, permission)


def test_unknown_permission_denied():
    assert not has_permission(UserRole.PATIENT, Permission.VIEW_AUDIT_LOG)


class StopCalled(Exception):
    """Raised when Streamlit stop is invoked in tests."""


def test_require_permission_allows(monkeypatch):
    st.session_state.clear()
    session_manager.init_session_state()
    st.session_state.role = UserRole.PATIENT.value

    called = {"ran": False, "updated": False}

    def _mark():
        called["updated"] = True

    monkeypatch.setattr(session_manager, "update_last_activity", _mark)

    @require_permission(Permission.VIEW_OWN_RECORDS)
    def _view():
        called["ran"] = True

    _view()
    assert called["ran"] is True
    assert called["updated"] is True


def test_require_permission_denies(monkeypatch):
    st.session_state.clear()
    session_manager.init_session_state()
    st.session_state.role = UserRole.PATIENT.value
    flags: dict[str, str] = {}

    monkeypatch.setattr(st, "error", lambda msg: flags.__setitem__("error", msg))
    monkeypatch.setattr(
        st,
        "stop",
        lambda: (_ for _ in ()).throw(StopCalled()),
    )

    @require_permission(Permission.MANAGE_USERS)
    def _admin():
        flags["ran"] = "yes"

    with pytest.raises(StopCalled):
        _admin()
    assert "error" in flags
    assert "ran" not in flags


def test_require_role_allows(monkeypatch):
    st.session_state.clear()
    session_manager.init_session_state()
    st.session_state.role = UserRole.ADMIN.value
    monkeypatch.setattr(session_manager, "update_last_activity", lambda: None)

    @require_role([UserRole.ADMIN])
    def _admin():
        return "ok"

    assert _admin() == "ok"
