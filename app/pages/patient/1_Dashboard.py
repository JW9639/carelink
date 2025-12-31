"""Patient dashboard."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Patient Dashboard", ["patient"]):
    st.stop()

st.markdown(f"### Welcome back, {st.session_state.get('user_name', 'Patient')}!")
st.markdown("---")

st.markdown("## Quick Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">Appointments</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View Appointments", use_container_width=True):
        st.switch_page("pages/patient/4_Appointments.py")

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">Prescriptions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View Prescriptions", use_container_width=True):
        st.switch_page("pages/patient/3_Prescriptions.py")

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Notifications</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View Notifications", use_container_width=True):
        st.switch_page("pages/patient/5_Notifications.py")

with col4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">1</div>
            <div class="stat-label">Lab Results</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View Bloodwork", use_container_width=True):
        st.switch_page("pages/patient/2_Bloodwork.py")

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Next Appointment")
    st.markdown(
        """
        <div class="card">
            <p><strong>General Checkup</strong></p>
            <span class="status-badge status-success">Confirmed</span>
            <p>Dr. Johnson - 12 Jan 2026 - 10:30</p>
            <p>CareLink Clinic, Belfast</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("### Recent Messages")
    st.markdown(
        """
        <div class="activity-item unread">
            <strong>Lab Results Ready</strong>
            <p>Dr. Johnson - Today</p>
            <span class="status-badge status-success">NEW</span>
        </div>
        <div class="activity-item">
            <strong>Prescription Updated</strong>
            <p>Pharmacy - Yesterday</p>
        </div>
        <div class="activity-item">
            <strong>Appointment Reminder</strong>
            <p>CareLink - 2 days ago</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Health Summary")
    st.markdown(
        """
        <div class="card">
            <p><strong>Blood Type:</strong> O+</p>
            <p><strong>Allergies:</strong> None</p>
            <p><strong>Last Visit:</strong> 20 Dec 2025</p>
            <p class="status-badge status-warning">Updated 3 days ago</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("### Quick Actions")
    if st.button("Book Appointment", use_container_width=True):
        st.switch_page("pages/patient/4_Appointments.py")
    action_cols = st.columns(2)
    with action_cols[0]:
        st.button("Request Refill", use_container_width=True)
        st.button("Message Doctor", use_container_width=True)
    with action_cols[1]:
        st.button("Lab Results", use_container_width=True)
        st.button("Medical Records", use_container_width=True)
