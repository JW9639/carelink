"""Admin dashboard."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.ui.components.page_header import render_page_header


if not apply_dashboard_layout("Admin Dashboard", ["admin"]):
    st.stop()

render_page_header("Admin Dashboard", "System overview and operational metrics.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">1,248</div>
            <div class="stat-label">Total Patients</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">42</div>
            <div class="stat-label">Total Doctors</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">86</div>
            <div class="stat-label">Today's Appointments</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Pending Approvals</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

tab_overview, tab_users, tab_system = st.tabs(["Analytics", "Users", "System Health"])

with tab_overview:
    st.markdown("### Weekly Activity")
    st.line_chart(
        {
            "Appointments": [50, 80, 65, 90, 120, 110, 140],
            "Registrations": [8, 12, 10, 15, 18, 20, 17],
        }
    )

with tab_users:
    st.markdown("### Quick Add User")
    with st.form("add_user"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Email")
        with col_b:
            st.selectbox("Role", ["patient", "doctor", "admin"])
        st.form_submit_button("Create User")

    st.markdown("### Recent Users")
    st.dataframe(
        {
            "Name": ["Emily Carter", "Mark Allen", "Sarah Khan"],
            "Role": ["patient", "doctor", "patient"],
            "Status": ["Active", "Active", "Pending"],
        },
        use_container_width=True,
    )

with tab_system:
    st.markdown("### System Status")
    st.markdown(
        """
        <div class="card">
            <p><strong>Database:</strong> Operational</p>
            <p><strong>Queue:</strong> Healthy</p>
            <p><strong>Uptime:</strong> 99.98%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Recent Activity")
    st.markdown(
        """
        <div class="activity-item">
            <strong>New doctor approval</strong>
            <p>Dr. Wilson - 2 hours ago</p>
        </div>
        <div class="activity-item">
            <strong>Audit log exported</strong>
            <p>Admin - 5 hours ago</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
