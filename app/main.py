"""CareLink - Main Application Entry Point."""

from __future__ import annotations

import streamlit as st

from app.security.session_manager import check_session_timeout, init_session_state


def main() -> None:
    """Route users based on authentication state."""
    st.set_page_config(
        page_title="CareLink - Healthcare Portal",
        page_icon="C",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    init_session_state()

    if st.session_state.get("is_authenticated", False):
        if check_session_timeout():
            role = st.session_state.get("role", "patient")
            role_value = role.value if hasattr(role, "value") else role
            if role_value == "patient":
                st.switch_page("pages/patient/1_Dashboard.py")
            elif role_value == "doctor":
                st.switch_page("pages/doctor/1_Dashboard.py")
            elif role_value == "admin":
                st.switch_page("pages/admin/1_Dashboard.py")
            else:
                st.switch_page("pages/Home.py")
        else:
            st.switch_page("pages/Home.py")
    else:
        st.switch_page("pages/Home.py")


if __name__ == "__main__":
    main()
