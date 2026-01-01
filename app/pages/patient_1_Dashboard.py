"""Patient dashboard - Main overview page."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Patient Dashboard", ["patient"]):
    st.stop()

# Get user's first name for greeting
user_email = st.session_state.get("user_name", "Patient")
first_name = user_email.split("@")[0].replace(".", " ").title() if "@" in user_email else user_email

# Current time for greeting
hour = datetime.now().hour
if hour < 12:
    greeting = "Good morning"
elif hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# Welcome Section
st.markdown(
    f"""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #2b2d42; margin: 0; font-weight: 600;">{greeting}, {first_name}!</h2>
        <p style="color: #6b7280; margin-top: 0.5rem;">Here's your health overview for today.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Quick Stats Row
st.markdown("#### At a Glance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(0, 102, 204, 0.1); color: #0066cc;">📅</div>
            <div class="stat-content">
                <div class="stat-number">1</div>
                <div class="stat-label">Upcoming Appointment</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(6, 214, 160, 0.1); color: #06d6a0;">💊</div>
            <div class="stat-content">
                <div class="stat-number">2</div>
                <div class="stat-label">Active Prescriptions</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(255, 183, 3, 0.1); color: #ffb703;">🔬</div>
            <div class="stat-content">
                <div class="stat-number">1</div>
                <div class="stat-label">Pending Results</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(239, 71, 111, 0.1); color: #ef476f;">🔔</div>
            <div class="stat-content">
                <div class="stat-number">3</div>
                <div class="stat-label">Notifications</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Main Content - Two Columns
left_col, right_col = st.columns([3, 2])

with left_col:
    # Next Appointment Card
    st.markdown("#### Next Appointment")
    st.markdown(
        """
        <div class="appointment-card">
            <div class="appointment-header">
                <div class="appointment-date">
                    <span class="date-day">12</span>
                    <span class="date-month">JAN</span>
                </div>
                <div class="appointment-details">
                    <h4 style="margin: 0; color: #2b2d42;">General Health Checkup</h4>
                    <p style="margin: 0.25rem 0; color: #6b7280;">
                        <strong>Dr. Sarah Johnson</strong> • General Practice
                    </p>
                    <p style="margin: 0; color: #6b7280;">
                        🕐 10:30 AM • 📍 CareLink Clinic, Belfast
                    </p>
                </div>
            </div>
            <div class="appointment-status">
                <span class="status-badge status-success">Confirmed</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📅 View All Appointments", use_container_width=True, key="view_appts"):
            st.switch_page("pages/patient_4_Appointments.py")
    with col_b:
        if st.button("➕ Book New Appointment", use_container_width=True, key="book_appt"):
            st.switch_page("pages/patient_4_Appointments.py")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Active Prescriptions
    st.markdown("#### Active Prescriptions")
    
    st.markdown(
        """
        <div class="prescription-item">
            <div class="prescription-icon">💊</div>
            <div class="prescription-details">
                <strong>Metformin 500mg</strong>
                <p style="margin: 0; color: #6b7280; font-size: 14px;">Take 1 tablet twice daily with meals</p>
                <span class="prescription-refill">Refill available: 15 Jan 2026</span>
            </div>
        </div>
        <div class="prescription-item">
            <div class="prescription-icon">💊</div>
            <div class="prescription-details">
                <strong>Lisinopril 10mg</strong>
                <p style="margin: 0; color: #6b7280; font-size: 14px;">Take 1 tablet once daily in the morning</p>
                <span class="prescription-refill">Refill available: 20 Jan 2026</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("💊 View All Prescriptions", use_container_width=True, key="view_prescriptions"):
        st.switch_page("pages/patient_3_Prescriptions.py")

with right_col:
    # Recent Activity / Notifications
    st.markdown("#### Recent Activity")
    
    st.markdown(
        """
        <div class="activity-item unread">
            <div class="activity-dot"></div>
            <div class="activity-content">
                <strong>Lab Results Ready</strong>
                <p>Your blood test results are now available for review.</p>
                <span class="activity-time">Today, 9:30 AM</span>
            </div>
        </div>
        <div class="activity-item">
            <div class="activity-dot read"></div>
            <div class="activity-content">
                <strong>Appointment Confirmed</strong>
                <p>Your appointment with Dr. Johnson has been confirmed.</p>
                <span class="activity-time">Yesterday, 2:15 PM</span>
            </div>
        </div>
        <div class="activity-item">
            <div class="activity-dot read"></div>
            <div class="activity-content">
                <strong>Prescription Renewed</strong>
                <p>Your Metformin prescription has been renewed.</p>
                <span class="activity-time">28 Dec 2025</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("🔔 View All Notifications", use_container_width=True, key="view_notifs"):
        st.switch_page("pages/patient_5_Notifications.py")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("#### Quick Actions")
    
    if st.button("🔬 View Bloodwork Results", use_container_width=True, key="view_blood"):
        st.switch_page("pages/patient_2_Bloodwork.py")
    
    if st.button("💬 Message Your Doctor", use_container_width=True, key="msg_doc"):
        st.info("Messaging feature coming soon!")
    
    if st.button("👤 Update Profile", use_container_width=True, key="update_profile"):
        st.switch_page("pages/patient_6_Profile.py")
