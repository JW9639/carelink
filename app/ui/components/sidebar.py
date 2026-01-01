"""Sidebar navigation components."""

from __future__ import annotations

import streamlit as st

from app.security.session_manager import clear_session


def render_sidebar_toggle() -> None:
    """Render a hamburger menu toggle button."""
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True
    # Sidebar toggle removed - using native Streamlit sidebar


def _nav_button(label: str, page: str) -> None:
    if st.button(label, use_container_width=True):
        st.switch_page(page)


def render_sidebar(role: str) -> None:
    """Render role-specific sidebar navigation."""
    if not st.session_state.get("sidebar_open", True):
        return

    with st.sidebar:
        st.markdown("## CareLink")
        st.markdown("---")

        if role == "patient":
            _nav_button("Dashboard", "pages/patient_1_Dashboard.py")
            _nav_button("Bloodwork", "pages/patient_2_Bloodwork.py")
            _nav_button("Prescriptions", "pages/patient_3_Prescriptions.py")
            _nav_button("Appointments", "pages/patient_4_Appointments.py")
            _nav_button("Notifications", "pages/patient_5_Notifications.py")
            _nav_button("Profile", "pages/patient_6_Profile.py")
        elif role == "doctor":
            _nav_button("Dashboard", "pages/doctor_1_Dashboard.py")
            _nav_button("Patients", "pages/doctor_2_Patients.py")
            _nav_button("Results Review", "pages/doctor_3_Results_Review.py")
            _nav_button("Appointments", "pages/doctor_4_Appointments.py")
            _nav_button("Profile", "pages/doctor_5_Profile.py")
        elif role == "admin":
            _nav_button("Dashboard", "pages/admin_1_Dashboard.py")
            _nav_button("User Management", "pages/admin_2_User_Management.py")
            _nav_button("Appointments", "pages/admin_3_Appointments.py")
            _nav_button("Audit Log", "pages/admin_4_Audit_Log.py")
            _nav_button("Profile", "pages/admin_5_Profile.py")

        st.markdown("---")

        st.markdown(f"**{st.session_state.get('user_name', 'Unknown')}**")
        st.caption(role.capitalize())

        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            clear_session()
            st.switch_page("pages/Home.py")
