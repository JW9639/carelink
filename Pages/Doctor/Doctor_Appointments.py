"""Doctor Appointments Page - View and manage patient appointments."""
import streamlit as st
from Services.session_manager import SessionManager
from Database.mock_Data import MOCK_APPOINTMENTS
from Components.cards import appointment_card
import pandas as pd
from datetime import datetime

from Components.sidebar import doctor_sidebar

# Page config
st.set_page_config(
    page_title="Appointments",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    """Load custom CSS styles."""
    try:
        with open("Styles/main.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Initialize session and check authentication
SessionManager.init_session()
SessionManager.require_auth(allowed_roles=["doctor"])

doctor_sidebar()

st.title("📅 Appointment Schedule")
st.caption("Manage your patient appointments and availability.")
st.markdown("---")

# Filter options
col1, col2, col3 = st.columns(3)
with col1:
    filter_status = st.selectbox("Status", ["All", "Confirmed", "Pending", "Cancelled", "Completed"])
with col2:
    filter_date = st.selectbox("Time Period", ["Today", "This Week", "This Month", "All"])
with col3:
    search_patient = st.text_input("🔍 Search Patient", placeholder="Patient name...")

st.markdown("---")

# Action buttons
col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("➕ Schedule Appointment", use_container_width=True, type="primary"):
        st.session_state.show_new_appointment_form = True

# Show new appointment form if button clicked
if st.session_state.get('show_new_appointment_form', False):
    st.markdown("### Schedule New Appointment")
    
    with st.form("new_appointment_form"):
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            patient_name = st.text_input("Patient Name*")
            appointment_type = st.selectbox("Appointment Type*", [
                "General Consultation",
                "Follow-up Visit",
                "Annual Physical",
                "Urgent Care",
                "Specialist Consultation",
                "Procedure"
            ])
            appointment_date = st.date_input("Date*")
        
        with form_col2:
            appointment_time = st.time_input("Time*")
            duration = st.selectbox("Duration", ["15 min", "30 min", "45 min", "60 min"], index=1)
            priority = st.selectbox("Priority", ["Normal", "Urgent"])
        
        notes = st.text_area("Appointment Notes", placeholder="Reason for visit, symptoms, etc.")
        
        submit_col1, submit_col2 = st.columns([1, 4])
        with submit_col1:
            submitted = st.form_submit_button("Schedule Appointment", type="primary", use_container_width=True)
        with submit_col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
        
        if submitted:
            if patient_name and appointment_type and appointment_date:
                st.success(f"✅ Appointment scheduled for {patient_name} on {appointment_date}")
                st.session_state.show_new_appointment_form = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")
        
        if cancelled:
            st.session_state.show_new_appointment_form = False
            st.rerun()
    
    st.markdown("---")

# Display appointments for doctor
st.markdown("### Your Schedule")

# Get current doctor's name
doctor_name = SessionManager.get_user_name()

# Filter appointments by doctor
doctor_appointments = [
    apt for apt in MOCK_APPOINTMENTS 
    if apt.get("doctor_name") == doctor_name or apt.get("doctor_id") == SessionManager.get_user_id()
]

# Apply search filter
if search_patient:
    doctor_appointments = [
        apt for apt in doctor_appointments 
        if search_patient.lower() in apt.get("patient_name", "").lower()
    ]

# Apply status filter
if filter_status != "All":
    doctor_appointments = [
        apt for apt in doctor_appointments 
        if apt.get("status", "Confirmed") == filter_status
    ]

if doctor_appointments:
    # Group by date for better organization
    st.markdown("#### Today's Appointments")
    today_appointments = [apt for apt in doctor_appointments[:3]]  # Mock: first 3 as today
    
    if today_appointments:
        for appointment in today_appointments:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                appointment_card(appointment)
            
            with col2:
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                if st.button("Start Visit", key=f"start_{appointment['id']}", use_container_width=True, type="primary"):
                    st.success("Starting virtual visit...")
                if st.button("Reschedule", key=f"reschedule_{appointment['id']}", use_container_width=True):
                    st.info("Rescheduling...")
                if st.button("Cancel", key=f"cancel_{appointment['id']}", use_container_width=True):
                    st.warning("Cancelling...")
    else:
        st.info("No appointments scheduled for today.")
    
    st.markdown("---")
    
    # Upcoming appointments
    st.markdown("#### Upcoming Appointments")
    upcoming_appointments = [apt for apt in doctor_appointments[3:]]  # Mock: rest as upcoming
    
    if upcoming_appointments:
        for appointment in upcoming_appointments:
            appointment_card(appointment)
    else:
        st.info("No upcoming appointments.")
else:
    st.info("No appointments found matching your criteria.")

st.markdown("---")

# Quick stats
st.markdown("### Appointment Statistics")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Today", len(today_appointments) if 'today_appointments' in locals() else 0)
with stat_col2:
    st.metric("This Week", len(doctor_appointments))
with stat_col3:
    confirmed_count = len([apt for apt in doctor_appointments if apt.get("status", "Confirmed") == "Confirmed"])
    st.metric("Confirmed", confirmed_count)
with stat_col4:
    pending_count = len([apt for apt in doctor_appointments if apt.get("status") == "Pending"])
    st.metric("Pending", pending_count)

st.markdown("---")

# Additional actions
col_action1, col_action2, col_action3 = st.columns(3)
with col_action1:
    if st.button("📊 View Calendar", use_container_width=True):
        st.info("Calendar view coming soon!")
with col_action2:
    if st.button("⚙️ Manage Availability", use_container_width=True):
        st.info("Availability settings coming soon!")
with col_action3:
    if st.button("📥 Export Schedule", use_container_width=True):
        st.info("Export feature coming soon!")
