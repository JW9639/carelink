"""CareLink login page."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from app.db.session import SessionLocal
from app.schemas.user import UserResponse
from app.security.session_manager import init_session_state, set_user
from app.services.auth_service import authenticate_user
from app.utils.constants import UserRole


def load_css(filename: str) -> None:
    """Load a CSS file from the styles directory."""
    css_path = Path(__file__).parent.parent / "styles" / filename
    try:
        css = css_path.read_text()
    except FileNotFoundError:
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _demo_credentials() -> dict[str, dict[str, str]]:
    """Return demo credentials for quick access."""
    return {
        "patient": {
            "email": os.getenv("DEMO_PATIENT_EMAIL", ""),
            "password": os.getenv("DEMO_PATIENT_PASSWORD", ""),
        },
        "doctor": {
            "email": os.getenv("DEMO_DOCTOR_EMAIL", ""),
            "password": os.getenv("DEMO_DOCTOR_PASSWORD", ""),
        },
        "admin": {
            "email": os.getenv("DEMO_ADMIN_EMAIL", ""),
            "password": os.getenv("DEMO_ADMIN_PASSWORD", ""),
        },
    }


def _handle_login(email: str, password: str) -> None:
    """Authenticate and route to dashboards."""
    if not email or not password:
        st.error("Missing credentials. Check your demo settings.")
        return
    db = SessionLocal()
    try:
        with st.spinner("Authenticating..."):
            user = authenticate_user(db, email=email, password=password)
        if user is None:
            st.error("Invalid credentials. Please try again.")
            return
        user_response = UserResponse.model_validate(user)
        set_user(user_response)
        st.session_state.user_name = user.email
        role = user.role.value if isinstance(user.role, UserRole) else str(user.role)
        st.session_state.role = role
        if role == "patient":
            st.switch_page("pages/patient/1_Dashboard.py")
        elif role == "doctor":
            st.switch_page("pages/doctor/1_Dashboard.py")
        elif role == "admin":
            st.switch_page("pages/admin/1_Dashboard.py")
    finally:
        db.close()


def main() -> None:
    """Render the login page."""
    st.set_page_config(
        page_title="CareLink - Login",
        page_icon="C",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    load_css("main.css")
    load_css("login.css")
    init_session_state()

    st.markdown(
        """
        <div class="login-page">
            <div class="login-header">
                <h1>CARELINK - Healthcare Management</h1>
            </div>
            <div class="login-card-wrapper">
                <div class="login-card">
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-icon">CL</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">CARELINK</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="login-subtitle">Secure Healthcare Portal</div>',
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@carelink.nhs.uk")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        if submitted:
            _handle_login(email=email, password=password)

    st.markdown('<div class="login-divider">Quick Access</div>', unsafe_allow_html=True)

    demo = _demo_credentials()
    st.markdown('<div class="quick-access">', unsafe_allow_html=True)
    if st.button("Patient Demo Login", use_container_width=True, key="demo_patient"):
        _handle_login(demo["patient"]["email"], demo["patient"]["password"])
    if st.button("Doctor Demo Login", use_container_width=True, key="demo_doctor"):
        _handle_login(demo["doctor"]["email"], demo["doctor"]["password"])
    if st.button("Admin Demo Login", use_container_width=True, key="demo_admin"):
        _handle_login(demo["admin"]["email"], demo["admin"]["password"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
                </div>
            </div>
            <div class="login-footer">
                (c) 2025 CareLink Healthcare System
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
