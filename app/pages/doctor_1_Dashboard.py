"""Doctor dashboard."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.ui.components.page_header import render_page_header


if not apply_dashboard_layout("Doctor Dashboard", ["doctor"]):
    st.stop()

render_page_header(
    f"Welcome back, Dr. {st.session_state.get('user_name', '')}!",
    "Here is a snapshot of today's workload.",
)

st.markdown("## Today at a Glance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">6</div>
            <div class="stat-label">Appointments</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">Pending Reviews</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">128</div>
            <div class="stat-label">Patients</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">Priority Tasks</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Priority Actions")
    st.markdown(
        """
        <div class="activity-item unread">
            <strong>Review Bloodwork</strong>
            <p>Patient: Emily Carter - Due Today</p>
        </div>
        <div class="activity-item">
            <strong>Approve Prescription</strong>
            <p>Patient: Mark Allen - Due Tomorrow</p>
        </div>
        <div class="activity-item">
            <strong>Follow-up Notes</strong>
            <p>Patient: Sarah Khan - Due This Week</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("### Today's Schedule")
    st.markdown(
        """
        <div class="card">
            <p><strong>09:00</strong> - Annual Review (C. Quinn)</p>
            <p><strong>10:30</strong> - Cardiology Follow-up (J. Singh)</p>
            <p><strong>13:00</strong> - Telehealth Consult (A. Murphy)</p>
            <p><strong>15:15</strong> - Lab Review (E. Carter)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Quick Actions")
    if st.button("Add Clinical Note", use_container_width=True):
        st.switch_page("pages/doctor_2_Patients.py")
    action_cols = st.columns(2)
    with action_cols[0]:
        st.button("Prescribe", use_container_width=True)
        st.button("Patient Chart", use_container_width=True)
    with action_cols[1]:
        st.button("Order Lab", use_container_width=True)
        st.button("Message Patient", use_container_width=True)

with col_right:
    st.markdown("### Recent Patients")
    st.markdown(
        """
        <div class="card">
            <p><strong>Emily Carter</strong> - Bloodwork Pending</p>
            <p><strong>Mark Allen</strong> - Follow-up Scheduled</p>
            <p><strong>Sarah Khan</strong> - Telehealth Complete</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
