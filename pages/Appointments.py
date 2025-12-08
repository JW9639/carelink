"""Appointments Page - View and manage appointments."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_APPOINTMENTS
from components.cards import appointment_card

from components.sidebar import patient_sidebar

# Page config
st.set_page_config(
    page_title="Appointments",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    """Load custom CSS styles."""
    try:
        with open("styles/main.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Initialize session and check authentication
SessionManager.init_session()
SessionManager.require_auth()

# Header
st.title("Appointments")
role = SessionManager.get_user_role()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### Patient Portal")
    st.info(f"**{st.session_state.user_name}**")
    st.caption("Patient Account")
    
    st.markdown("---")
    st.markdown("### Quick Links")
    
    # Add CSS for tighter spacing
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stSidebar"] button[kind="secondary"] {
        padding: 0.25rem 0.75rem !important;
        margin-bottom: 0.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.page_link("pages/Patient_Dashboard.py", label="• Dashboard", use_container_width=True)
    st.page_link("pages/Appointments.py", label="• Appointments", use_container_width=True)
    st.page_link("pages/Prescriptions.py", label="• Prescriptions", use_container_width=True)
    st.page_link("pages/Lab_Results.py", label="• Lab Results", use_container_width=True)
    st.page_link("pages/Profile.py", label="• Profile", use_container_width=True)
    
    st.markdown("---")
    if st.button("Logout", use_container_width=True, type="primary"):
        SessionManager.logout()
        st.switch_page("Home.py")
    
    st.markdown("---")
    st.markdown("### 📞 Emergency")
    st.error("**911** - Emergency")
    st.caption("Hospital: (555) 999-8888")

st.markdown("---")

# Filter options
col1, col2, col3 = st.columns(3)
with col1:
    filter_status = st.selectbox("Status", ["All", "Confirmed", "Pending", "Cancelled"])
with col2:
    filter_date = st.selectbox("Time Period", ["All", "Today", "This Week", "This Month"])
with col3:
    sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Doctor", "Type"])

st.markdown("---")

# Display appointments based on role
if role == "patient":
    st.markdown("### Your Appointments")
    appointments = [apt for apt in MOCK_APPOINTMENTS if apt["patient_name"] == st.session_state.user_name]
elif role == "doctor":
    st.markdown("### Your Schedule")
    appointments = [apt for apt in MOCK_APPOINTMENTS if apt["doctor_name"] == st.session_state.user_name]
else:
    st.markdown("### All Appointments")
    appointments = MOCK_APPOINTMENTS

if appointments:
    for appointment in appointments:
        appointment_card(appointment)
else:
    st.info("No appointments found.")

st.markdown("---")

# Action buttons
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("Schedule New Appointment", use_container_width=True, type="primary"):
        st.info("Appointment scheduling feature coming soon!")
with col_btn2:
    if st.button("Export Schedule", use_container_width=True):
        st.info("Export feature coming soon!")
