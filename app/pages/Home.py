"""CareLink login page."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from app.db.session import SessionLocal
from app.schemas.user import UserResponse
from app.security.session_manager import init_session_state, set_user
from app.services.auth_service import authenticate_user
from app.ui.components.header import render_app_header
from app.utils.constants import UserRole


def load_css(filename: str) -> None:
    """Load a CSS file from the styles directory."""
    possible_paths = [
        Path(__file__).resolve().parent.parent / "styles" / filename,
        Path(__file__).resolve().parent.parent.parent / "styles" / filename,
        Path("/app/app/styles") / filename,
    ]

    for css_path in possible_paths:
        if css_path.exists():
            try:
                css_content = css_path.read_text()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
                return
            except Exception:
                continue


def _demo_credentials() -> dict[str, dict[str, str]]:
    """Return demo credentials for quick access."""
    return {
        "patient": {
            "email": os.getenv("DEMO_PATIENT_EMAIL", "patient@carelink.nhs.uk"),
            "password": os.getenv("DEMO_PATIENT_PASSWORD", "Patient123!"),
        },
        "doctor": {
            "email": os.getenv("DEMO_DOCTOR_EMAIL", "dr.johnson@carelink.nhs.uk"),
            "password": os.getenv("DEMO_DOCTOR_PASSWORD", "Doctor123!"),
        },
        "admin": {
            "email": os.getenv("DEMO_ADMIN_EMAIL", "admin@carelink.nhs.uk"),
            "password": os.getenv("DEMO_ADMIN_PASSWORD", "Admin123!"),
        },
    }


def _handle_login(email: str, password: str) -> None:
    """Authenticate and route to dashboards."""
    if not email or not password:
        st.error("Please enter both email and password.")
        return
    db = SessionLocal()
    try:
        user = authenticate_user(db, email=email, password=password)
        if user is None:
            st.error("Invalid credentials. Please try again.")
            return
        user_response = UserResponse.model_validate(user)
        set_user(user_response)  # This sets is_authenticated, role, and user_name
        
        # Route to appropriate dashboard based on role
        role = st.session_state.get("role", "")
        if role == UserRole.PATIENT.value:
            st.switch_page("pages/patient_1_Dashboard.py")
        elif role == UserRole.DOCTOR.value:
            st.switch_page("pages/doctor_1_Dashboard.py")
        elif role == UserRole.ADMIN.value:
            st.switch_page("pages/admin_1_Dashboard.py")
        else:
            st.error(f"Unknown role: {role}")
    finally:
        db.close()


def main() -> None:
    """Render the login page."""
    st.set_page_config(
        page_title="CareLink - Login",
        page_icon="C",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Load CSS FIRST before any content
    load_css("main.css")
    load_css("login.css")

    init_session_state()

    # Render header with subtitle (no menu toggle on login page)
    render_app_header(show_subtitle=True, show_menu_toggle=False)
    
    # Create centered columns - wider middle column for larger screens
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
    
    with col2:
        # Login form header
        st.markdown('<h2 style="text-align: center; color: #2b2d42; font-weight: 700; margin-bottom: 1.5rem;">Sign In to CareLink</h2>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email Address", placeholder="you@carelink.nhs.uk")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                _handle_login(email=email, password=password)

        st.markdown('<div class="divider-section"><span>Quick Access</span></div>', unsafe_allow_html=True)

        demo = _demo_credentials()

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Patient\nDemo", use_container_width=True, key="demo_patient"):
                _handle_login(demo["patient"]["email"], demo["patient"]["password"])
        with col_b:
            if st.button("Doctor\nDemo", use_container_width=True, key="demo_doctor"):
                _handle_login(demo["doctor"]["email"], demo["doctor"]["password"])
        with col_c:
            if st.button("Admin\nDemo", use_container_width=True, key="demo_admin"):
                _handle_login(demo["admin"]["email"], demo["admin"]["password"])
    
    # Fixed footer
    st.markdown('<div class="app-footer">© 2025 CareLink Healthcare System</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
