"""Doctor Dashboard - Manage patients, appointments, and medical records."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_STATS, MOCK_APPOINTMENTS, MOCK_PATIENTS
from components.cards import stat_card, appointment_card
import pandas as pd

from components.sidebar import doctor_sidebar

# Page config
st.set_page_config(
    page_title="Doctor Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    """Load custom CSS styles."""
    try:
        with open("styles/main.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        with open("styles/dashboard.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Initialize session and check authentication
SessionManager.init_session()
SessionManager.require_auth(allowed_roles=["doctor"])

# Header
st.title("Doctor Dashboard")
st.markdown(f"### Welcome, {st.session_state.user_name}!")

# Get doctor specialty
user_data = SessionManager.get_user_data()
specialty = user_data.get('specialty', 'General Medicine') if user_data else 'General Medicine'
st.caption(f"Specialty: {specialty}")

# Sidebar Navigation
doctor_sidebar()

st.markdown("---")

# Statistics Cards
st.markdown("### Today's Overview")
stats = MOCK_STATS["doctor"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    stat_card("Today's Appointments", str(stats["today_appointments"]), "📅", "#0066CC")
with col2:
    stat_card("Pending Reviews", str(stats["pending_reviews"]), "📋", "#FFB703")
with col3:
    stat_card("New Messages", str(stats["new_messages"]), "✉️", "#00A896")
with col4:
    stat_card("Total Patients", str(stats["patients_total"]), "👥", "#EF476F")

st.markdown("---")

# Main Content - Focused Dashboard View
st.markdown("### Today at a Glance")

# Today's Appointments - Show only next 2-3
doctor_appointments = [apt for apt in MOCK_APPOINTMENTS if apt["doctor_name"] == st.session_state.user_name]

col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown("#### Upcoming Appointments Today")
    
    if doctor_appointments:
        # Show only first 2 appointments
        for appointment in doctor_appointments[:2]:
            appointment_card(appointment)
        if len(doctor_appointments) > 2:
            st.info(f"+ {len(doctor_appointments) - 2} more appointments today")
    else:
        st.info("No appointments scheduled for today.")
    
    if st.button("View Full Schedule", use_container_width=True, type="primary"):
        st.info("Full calendar view coming soon!")
    
    st.markdown("---")
    
    # Priority Actions Only
    st.markdown("#### Priority Actions")
    
    high_priority_tasks = [
        {"task": "Review lab results for John Smith", "icon": ""},
        {"task": "Complete chart notes (3 pending)", "icon": ""},
        {"task": "Sign off on discharge - Robert Johnson", "icon": ""}
    ]
    
    for task in high_priority_tasks:
        st.markdown(f"""
            <div style="
                background: white;
                border-radius: 8px;
                padding: 14px;
                margin: 8px 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                border-left: 4px solid #EF476F;
            ">
                <span style="color: #2B2D42; font-size: 14px;">{task['icon']} {task['task']}</span>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("View All Tasks", use_container_width=True):
        st.info("Full task list coming soon!")

with col_side:
    # Quick Actions - Reduced to most common
    st.markdown("#### Quick Actions")
    
    if st.button("Add Note", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("Prescribe", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("Patient Chart", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("Order Lab", use_container_width=True):
        st.info("Feature coming soon!")
    
    st.markdown("---")
    
    # Today's Schedule - Simplified
    st.markdown("#### Today's Schedule")
    current_time = "10:00 AM"
    st.markdown(f"""
        <div style="background: white; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);">
            <p style="margin: 8px 0; color: #2B2D42; font-size: 14px; line-height: 1.8;">
                <strong style="color: #06D6A0;">➜ {current_time}</strong> - Patient Appointments<br>
                <span style="color: #6B7280;">12:00 PM - Lunch Break</span><br>
                <span style="color: #6B7280;">1:00 PM - Consultations</span><br>
                <span style="color: #6B7280;">4:00 PM - Chart Review</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Metrics
    st.markdown("#### This Week")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Patients", "42", "+5")
    with col_b:
        st.metric("Rating", "98%", "+2%")

st.markdown("---")

# Bottom row - Patient summary
st.markdown("### Recent Patients (Last 5)")
patient_data = pd.DataFrame(MOCK_PATIENTS[:5])

st.dataframe(
    patient_data[['name', 'age', 'last_visit', 'status']],
    use_container_width=True,
    hide_index=True,
    column_config={
        "name": "Patient Name",
        "age": "Age",
        "last_visit": "Last Visit",
        "status": "Status"
    }
)

if st.button("View All Patients", use_container_width=True):
    st.info("Full patient list coming soon!")
