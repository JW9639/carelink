"""Tests for audit utilities."""

from __future__ import annotations

import streamlit as st
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.security.audit import AuditAction, audit_log, log_action


def test_log_action_creates_entry(test_db: Session, test_user):
    st.session_state.clear()
    st.session_state.ip_address = "127.0.0.1"
    st.session_state.user_agent = "pytest"
    test_db.query(AuditLog).delete()
    test_db.commit()

    log_action(
        db=test_db,
        user_id=test_user.id,
        action=AuditAction.LOGIN,
        resource_type="user",
        resource_id=test_user.id,
        details={"info": "login"},
    )
    count = test_db.execute(select(AuditLog)).scalars().all()
    assert len(count) == 1


def test_audit_log_decorator(test_db: Session, test_user):
    st.session_state.clear()
    st.session_state.user = test_user
    st.session_state.ip_address = "127.0.0.1"
    st.session_state.user_agent = "pytest"
    test_db.query(AuditLog).delete()
    test_db.commit()

    @audit_log(AuditAction.UPDATE_RECORD, "user")
    def update_user(db: Session, resource_id: int):
        return "ok"

    result = update_user(db=test_db, resource_id=test_user.id)
    assert result == "ok"
    logged = test_db.execute(select(AuditLog)).scalars().all()
    assert len(logged) == 1
    assert logged[0].resource_id == test_user.id
