"""Admin Appointments Page - View and manage all appointments."""
import streamlit as st
from Services.session_manager import SessionManager
from Database.mock_Data import MOCK_APPOINTMENTS
from Components.cards import appointment_card
import pandas as pd
from datetime import datetime

from Components.sidebar import admin_sidebar

# Page config
st.set_page_config(
    page_title="Appointments Management",
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
SessionManager.require_auth(allowed_roles=["admin"])

admin_sidebar()

st.title("📅 Appointments Management")
st.caption("System-wide appointment oversight and scheduling.")
st.markdown("---")

# Filter options
col1, col2, col3, col4 = st.columns(4)
with col1:
    filter_status = st.selectbox("Status", ["All", "Confirmed", "Pending", "Cancelled", "Completed"])
with col2:
    filter_date = st.selectbox("Time Period", ["Today", "This Week", "This Month", "All"])
with col3:
    filter_doctor = st.selectbox("Doctor", ["All Doctors", "Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Davis"])
with col4:
    search = st.text_input("🔍 Search", placeholder="Patient or doctor name...")

st.markdown("---")

# Quick stats
st.markdown("### System Overview")
stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

with stat_col1:
    st.metric("Total Today", "47")
with stat_col2:
    st.metric("Confirmed", "42")
with stat_col3:
    st.metric("Pending", "5")
with stat_col4:
    st.metric("Cancelled", "2")
with stat_col5:
    st.metric("This Week", len(MOCK_APPOINTMENTS))

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 All Appointments", "📊 Analytics", "⚙️ Management"])

with tab1:
    st.markdown("### All Appointments")
    
    # Apply filters
    appointments = MOCK_APPOINTMENTS
    
    if search:
        appointments = [
            apt for apt in appointments 
            if search.lower() in apt.get("patient_name", "").lower() 
            or search.lower() in apt.get("doctor_name", "").lower()
        ]
    
    if filter_status != "All":
        appointments = [
            apt for apt in appointments 
            if apt.get("status", "Confirmed") == filter_status
        ]
    
    if filter_doctor != "All Doctors":
        appointments = [
            apt for apt in appointments 
            if apt.get("doctor_name") == filter_doctor
        ]
    
    if appointments:
        # Display as expandable cards with actions
        for appointment in appointments:
            with st.expander(
                f"**{appointment.get('patient_name', 'Unknown')}** - {appointment.get('doctor_name', 'Unknown')} ({appointment.get('date', 'TBD')} at {appointment.get('time', 'TBD')})",
                expanded=False
            ):
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown(f"**Patient:** {appointment.get('patient_name', 'Unknown')}")
                    st.markdown(f"**Doctor:** {appointment.get('doctor_name', 'Unknown')}")
                    st.markdown(f"**Type:** {appointment.get('type', 'General Consultation')}")
                
                with col_info2:
                    status_color = "#00A896" if appointment.get("status") == "Confirmed" else "#F77F00"
                    st.markdown(f"**Date:** {appointment.get('date', 'TBD')}")
                    st.markdown(f"**Time:** {appointment.get('time', 'TBD')}")
                    st.markdown(f"**Status:** <span style='color: {status_color};'>{appointment.get('status', 'Confirmed')}</span>", unsafe_allow_html=True)
                
                if appointment.get('reason'):
                    st.markdown(f"**Reason:** {appointment['reason']}")
                
                st.markdown("---")
                
                # Admin actions
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button("✏️ Edit", key=f"edit_{appointment['id']}", use_container_width=True):
                        st.info("Edit feature coming soon!")
                
                with action_col2:
                    if st.button("🔄 Reschedule", key=f"reschedule_{appointment['id']}", use_container_width=True):
                        st.info("Rescheduling feature coming soon!")
                
                with action_col3:
                    if st.button("✅ Confirm", key=f"confirm_{appointment['id']}", use_container_width=True):
                        st.success("Appointment confirmed!")
                
                with action_col4:
                    if st.button("❌ Cancel", key=f"cancel_{appointment['id']}", use_container_width=True):
                        st.warning("Appointment cancelled!")
    else:
        st.info("No appointments found matching your criteria.")

with tab2:
    st.markdown("### Appointment Analytics")
    
    # Appointment distribution by doctor
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Appointments by Doctor")
        doctor_data = pd.DataFrame({
            "Doctor": ["Dr. Johnson", "Dr. Chen", "Dr. Davis", "Dr. Wilson"],
            "Appointments": [15, 12, 10, 8]
        })
        st.bar_chart(doctor_data.set_index("Doctor"))
    
    with col_chart2:
        st.markdown("#### Appointments by Status")
        status_data = pd.DataFrame({
            "Status": ["Confirmed", "Pending", "Cancelled", "Completed"],
            "Count": [42, 5, 2, 28]
        })
        st.bar_chart(status_data.set_index("Status"))
    
    st.markdown("---")
    
    # Weekly trend
    st.markdown("#### Weekly Appointment Trend")
    weekly_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Appointments": [45, 52, 48, 50, 47]
    })
    st.line_chart(weekly_data.set_index("Day"))

with tab3:
    st.markdown("### Appointment Management")
    
    # Bulk actions
    st.markdown("#### Bulk Actions")
    col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
    
    with col_bulk1:
        if st.button("📧 Send Reminders", use_container_width=True, type="primary"):
            st.success("Reminder emails sent to all patients with appointments tomorrow!")
    
    with col_bulk2:
        if st.button("📥 Export All Data", use_container_width=True):
            st.info("Export feature coming soon!")
    
    with col_bulk3:
        if st.button("🔄 Sync Calendar", use_container_width=True):
            st.info("Calendar sync feature coming soon!")
    
    st.markdown("---")
    
    # System settings
    st.markdown("#### Appointment Settings")
    
    settings_col1, settings_col2 = st.columns(2)
    
    with settings_col1:
        st.checkbox("Automatic confirmation emails", value=True)
        st.checkbox("Send reminder 24 hours before", value=True)
        st.checkbox("Allow patient self-scheduling", value=True)
    
    with settings_col2:
        st.number_input("Default appointment duration (minutes)", value=30, min_value=15, max_value=120, step=15)
        st.number_input("Maximum appointments per day", value=20, min_value=5, max_value=50)
        st.selectbox("Cancellation policy", ["24 hours notice", "48 hours notice", "72 hours notice"])
    
    st.markdown("---")
    
    if st.button("💾 Save Settings", use_container_width=True, type="primary"):
        st.success("Settings saved successfully!")
