"""Streamlit entry point for CareLink."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st
import streamlit_authenticator as stauth

from app.config import get_settings
from app.schemas.user import UserResponse
from app.security import session_manager
from app.ui.theme import apply_theme
from app.utils.constants import UserRole


settings = get_settings()


def _credentials() -> dict:
    """Return placeholder credentials for development."""
    passwords = {
        "patient@example.com": "Patient123!",
        "doctor@example.com": "Doctor123!",
        "admin@example.com": "Admin123!",
    }
    hashed = stauth.Hasher().hash_list(list(passwords.values()))
    emails = list(passwords.keys())
    return {
        "usernames": {
            emails[0]: {
                "email": emails[0],
                "name": "Patient One",
                "password": hashed[0],
                "role": UserRole.PATIENT.value,
                "id": 1,
            },
            emails[1]: {
                "email": emails[1],
                "name": "Doctor One",
                "password": hashed[1],
                "role": UserRole.DOCTOR.value,
                "id": 2,
            },
            emails[2]: {
                "email": emails[2],
                "name": "Admin One",
                "password": hashed[2],
                "role": UserRole.ADMIN.value,
                "id": 3,
            },
        }
    }


def render_login(authenticator: stauth.Authenticate) -> None:
    """Render login page."""
    st.title("CareLink")
    st.subheader("Secure login")
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status:
        user_info = authenticator.credentials["usernames"][username]
        user = UserResponse(
            id=user_info["id"],
            email=user_info["email"],
            role=UserRole(user_info["role"]),
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        session_manager.set_user(user)
        st.success(f"Welcome back, {name}!")
    elif auth_status is False:
        st.error("Invalid credentials")
    else:
        st.info("Enter your credentials to continue.")


def render_dashboard(role: UserRole) -> None:
    """Render dashboard placeholder based on role."""
    st.sidebar.title("Navigation")
    if role is UserRole.PATIENT:
        st.sidebar.success("Patient Dashboard")
        st.header("Patient Dashboard")
        st.write("View your appointments, results, and notifications.")
    elif role is UserRole.DOCTOR:
        st.sidebar.success("Doctor Dashboard")
        st.header("Doctor Dashboard")
        st.write("Review patient records and publish results.")
    elif role is UserRole.ADMIN:
        st.sidebar.success("Admin Dashboard")
        st.header("Admin Dashboard")
        st.write("Manage users, appointments, and audit logs.")


def main() -> None:
    """Main Streamlit application entry."""
    st.set_page_config(page_title=settings.APP_NAME, page_icon="🏥", layout="wide")
    apply_theme()
    session_manager.init_session_state()

    credentials = _credentials()
    authenticator = stauth.Authenticate(
        credentials,
        "carelink_cookie",
        settings.SECRET_KEY,
        cookie_expiry_days=1,
    )

    if st.session_state.is_authenticated:
        if not session_manager.check_session_timeout():
            st.warning("Session expired. Please log in again.")
    if not st.session_state.is_authenticated:
        render_login(authenticator)
        return

    if authenticator.logout("Logout", "sidebar"):
        session_manager.clear_session()
        st.experimental_rerun()

    role = UserRole(st.session_state.role)
    session_manager.update_last_activity()
    render_dashboard(role)


if __name__ == "__main__":
    main()
