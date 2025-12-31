"""Sidebar navigation components."""

from __future__ import annotations

import streamlit as st

from app.security.session_manager import clear_session


def render_sidebar_toggle() -> None:
    """Render a hamburger menu toggle button."""
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True

    st.markdown('<div class="sidebar-toggle">', unsafe_allow_html=True)
    if st.button("Menu", key="sidebar_toggle"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.sidebar_open:
        st.markdown('<div class="sidebar-overlay"></div>', unsafe_allow_html=True)


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
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

        if role == "patient":
            _nav_button("Dashboard", "pages/patient/1_Dashboard.py")
            _nav_button("Bloodwork", "pages/patient/2_Bloodwork.py")
            _nav_button("Prescriptions", "pages/patient/3_Prescriptions.py")
            _nav_button("Appointments", "pages/patient/4_Appointments.py")
            _nav_button("Notifications", "pages/patient/5_Notifications.py")
            _nav_button("Profile", "pages/patient/6_Profile.py")
        elif role == "doctor":
            _nav_button("Dashboard", "pages/doctor/1_Dashboard.py")
            _nav_button("Patients", "pages/doctor/2_Patients.py")
            _nav_button("Results Review", "pages/doctor/3_Results_Review.py")
            _nav_button("Appointments", "pages/doctor/4_Appointments.py")
            _nav_button("Profile", "pages/doctor/5_Profile.py")
        elif role == "admin":
            _nav_button("Dashboard", "pages/admin/1_Dashboard.py")
            _nav_button("User Management", "pages/admin/2_User_Management.py")
            _nav_button("Appointments", "pages/admin/3_Appointments.py")
            _nav_button("Audit Log", "pages/admin/4_Audit_Log.py")
            _nav_button("Profile", "pages/admin/5_Profile.py")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown('<div class="sidebar-user">', unsafe_allow_html=True)
        st.markdown(f"**{st.session_state.get('user_name', 'Unknown')}**")
        st.caption(role.capitalize())
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            clear_session()
            st.switch_page("pages/Home.py")
