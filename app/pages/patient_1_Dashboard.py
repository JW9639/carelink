"""Patient dashboard - Main overview page."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from app.db.session import SessionLocal
from app.services.patient_service import PatientService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Patient Dashboard", ["patient"]):
    st.stop()

# Get user info from session
user_id = st.session_state.get("user_id")
user_email = st.session_state.get("user_name", "Patient")
first_name = user_email.split("@")[0].replace(".", " ").title() if "@" in user_email else user_email

# Initialize database session and load real data
db = SessionLocal()
try:
    patient_service = PatientService(db)
    
    # Get patient profile
    patient = patient_service.get_patient_by_user_id(user_id) if user_id else None
    
    if patient:
        # Get real dashboard stats
        stats = patient_service.get_dashboard_stats(patient.id)
        next_appt_info = patient_service.get_next_appointment_info(patient.id)
        
        # Use real first name from patient record
        first_name = patient.first_name
    else:
        # Fallback to default stats if patient not found
        stats = None
        next_appt_info = None
finally:
    db.close()

# Current time for greeting
hour = datetime.now().hour
if hour < 12:
    greeting = "Good morning"
    emoji = "☀️"
elif hour < 18:
    greeting = "Good afternoon"
    emoji = "🌤️"
else:
    greeting = "Good evening"
    emoji = "🌙"

# Welcome Section with gradient background
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 168, 150, 0.08) 100%);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 102, 204, 0.1);
    ">
        <h1 style="color: #1e293b; margin: 0 0 8px 0; font-weight: 700; font-size: 2rem;">{greeting}, {first_name}!</h1>
        <p style="color: #64748b; margin: 0; font-size: 1.1rem;">Welcome back to your health dashboard. Here's what's happening today.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Quick Stats Row
st.markdown('<p style="color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; margin-bottom: 16px;">Your Health Summary</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# Use real stats or fallback to defaults
appt_count = stats.upcoming_appointments if stats else 0
rx_count = stats.active_prescriptions if stats else 0
pending_count = stats.pending_results if stats else 0
notif_count = stats.unread_notifications if stats else 0

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.15), rgba(0, 102, 204, 0.05)); color: #0066cc;">📅</div>
            <div class="stat-content">
                <div class="stat-number">{appt_count}</div>
                <div class="stat-label">Appointment{'s' if appt_count != 1 else ''}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, rgba(6, 214, 160, 0.15), rgba(6, 214, 160, 0.05)); color: #059669;">💊</div>
            <div class="stat-content">
                <div class="stat-number">{rx_count}</div>
                <div class="stat-label">Prescription{'s' if rx_count != 1 else ''}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05)); color: #d97706;">🔬</div>
            <div class="stat-content">
                <div class="stat-number">{pending_count}</div>
                <div class="stat-label">Pending Result{'s' if pending_count != 1 else ''}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05)); color: #dc2626;">🔔</div>
            <div class="stat-content">
                <div class="stat-number">{notif_count}</div>
                <div class="stat-label">Notification{'s' if notif_count != 1 else ''}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Main Content - Two Columns
left_col, right_col = st.columns([3, 2])

with left_col:
    # Next Appointment Card
    st.markdown('<p style="color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; margin-bottom: 16px;">Your Next Appointment</p>', unsafe_allow_html=True)
    
    if next_appt_info:
        # Format the appointment date/time
        appt_dt = next_appt_info.scheduled_datetime
        day_num = appt_dt.strftime("%d")
        month_abbr = appt_dt.strftime("%b").upper()
        time_str = appt_dt.strftime("%I:%M %p").lstrip("0")
        reason = next_appt_info.reason or "Appointment"
        
        # Status display based on pending or confirmed
        if next_appt_info.is_pending:
            status_html = '<span style="display: inline-block; padding: 6px 14px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05)); color: #d97706; border-radius: 20px; font-size: 13px; font-weight: 600;">⏳ Pending Review</span>'
        else:
            status_html = '<span style="display: inline-block; padding: 6px 14px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05)); color: #059669; border-radius: 20px; font-size: 13px; font-weight: 600;">✓ Confirmed</span>'
        
        st.markdown(
            f"""
            <div class="appointment-card">
                <div class="appointment-header">
                    <div class="appointment-date">
                        <span class="date-day">{day_num}</span>
                        <span class="date-month">{month_abbr}</span>
                    </div>
                    <div class="appointment-details">
                        <h4 style="margin: 0 0 8px 0; color: #1e293b; font-size: 1.25rem; font-weight: 700;">{reason}</h4>
                        <p style="margin: 0 0 6px 0; color: #475569; font-size: 15px;">
                            <strong style="color: #1e293b;">{next_appt_info.doctor_name}</strong> • {next_appt_info.specialty}
                        </p>
                        <p style="margin: 0; color: #64748b; font-size: 14px;">
                            🕐 {time_str}
                        </p>
                    </div>
                </div>
                <div class="appointment-status" style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
                    {status_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="appointment-card">
                <div style="text-align: center; padding: 24px;">
                    <p style="color: #64748b; font-size: 16px; margin: 0 0 12px 0;">No upcoming appointments</p>
                    <p style="color: #94a3b8; font-size: 14px; margin: 0;">Book an appointment to see your next visit here</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("View All Appointments", use_container_width=True, key="view_appts"):
            st.session_state.appointments_tab = "history"
            st.switch_page("pages/patient_4_Appointments.py")
    with col_b:
        if st.button("Book New Appointment", use_container_width=True, key="book_appt", type="primary"):
            st.session_state.appointments_tab = "book"
            st.switch_page("pages/patient_4_Appointments.py")

with right_col:
    # Quick Actions
    st.markdown('<p style="color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; margin-bottom: 16px;">Quick Actions</p>', unsafe_allow_html=True)
    
    # Quick action cards
    st.markdown(
        """
        <div style="
            background: linear-gradient(145deg, #ffffff, #f8fafc);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
        ">
            <p style="color: #64748b; font-size: 13px; margin: 0 0 4px 0;">Need help?</p>
            <p style="color: #1e293b; font-weight: 600; margin: 0;">Access all your health services below</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("View Bloodwork Results", use_container_width=True, key="view_blood"):
        st.switch_page("pages/patient_2_Bloodwork.py")
    
    if st.button("View Prescriptions", use_container_width=True, key="view_prescriptions"):
        st.switch_page("pages/patient_3_Prescriptions.py")
    
    if st.button("View Notifications", use_container_width=True, key="view_notifs"):
        st.switch_page("pages/patient_5_Notifications.py")
    
    if st.button("Update Profile", use_container_width=True, key="update_profile"):
        st.switch_page("pages/patient_6_Profile.py")
