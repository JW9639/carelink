"""Patient Dashboard - View appointments, medical records, prescriptions."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_STATS, MOCK_APPOINTMENTS, MOCK_MEDICAL_RECORDS, MOCK_PRESCRIPTIONS, MOCK_MESSAGES
from components.cards import stat_card, appointment_card, medical_record_card, prescription_card, message_card

from components.sidebar import patient_sidebar

# Page config
st.set_page_config(
    page_title="Patient Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
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
SessionManager.require_auth(allowed_roles=["patient"])

# Header
st.title("Patient Dashboard")
st.markdown(f"### Welcome back, {st.session_state.user_name}!")

# Sidebar Navigation
patient_sidebar()

st.markdown("---")

# Statistics Cards
st.markdown("## Quick Overview")
stats = MOCK_STATS["patient"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    stat_card("Upcoming Appointments", str(stats["upcoming_appointments"]), "📅", "#0066CC")
with col2:
    stat_card("Active Prescriptions", str(stats["active_prescriptions"]), "💊", "#00A896")
with col3:
    stat_card("Unread Messages", str(stats["unread_messages"]), "✉️", "#FFB703")
with col4:
    stat_card("Lab Work", str(stats["pending_bills"]), "🔬", "#EF476F")

st.markdown("---")

# Main Content - Focused Dashboard View
st.markdown("## Today's Overview")

# Next Appointment Highlight
patient_appointments = [apt for apt in MOCK_APPOINTMENTS if apt["patient_name"] == st.session_state.user_name]
if patient_appointments:
    st.markdown("#### Next Appointment")
    appointment_card(patient_appointments[0])
    if len(patient_appointments) > 1:
        st.info(f"You have {len(patient_appointments)} upcoming appointments. View all in Appointments page.")
else:
    st.info("No upcoming appointments. Click below to schedule one.")

if st.button("View All Appointments", use_container_width=True, type="primary"):
    st.info("Navigation to Appointments page coming soon!")

st.markdown("---")

# Two column layout for key information
col_left, col_right = st.columns(2)

with col_left:
    # Health Summary Card
    st.markdown("### Health Summary")
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0066CC15, #00A89615);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #0066CC;
        ">
            <p style="margin: 8px 0; color: #2B2D42; font-size: 14px;">
                <strong>Blood Type:</strong> O+<br>
                <strong>Allergies:</strong> None<br>
                <strong>Last Visit:</strong> Nov 20, 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # Quick Actions
    st.markdown("### Quick Actions")
    
    if st.button("Book Appointment", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("Request Refill", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("Message Doctor", use_container_width=True):
        st.info("Feature coming soon!")
    
    if st.button("View Lab Results", use_container_width=True):
        st.info("Feature coming soon!")

st.markdown("---")

# Messages Section
st.markdown("### Recent Messages")
patient_messages = [msg for msg in MOCK_MESSAGES if msg["to"] == st.session_state.user_name][:3]

if patient_messages:
    for message in patient_messages:
        message_card(message)
    
    if len([msg for msg in MOCK_MESSAGES if msg["to"] == st.session_state.user_name]) > 3:
        if st.button("📬 View All Messages", use_container_width=True, type="secondary"):
            st.info("Navigation to Messages page coming soon!")
else:
    st.info("No messages yet.")

st.markdown("---")

# Recent Prescriptions Section
st.markdown("### Active Prescriptions")
patient_prescriptions = [rx for rx in MOCK_PRESCRIPTIONS if rx["patient_name"] == st.session_state.user_name and rx.get("status") == "Active"][:3]

if patient_prescriptions:
    for prescription in patient_prescriptions:
        prescription_card(prescription)
    
    if len([rx for rx in MOCK_PRESCRIPTIONS if rx["patient_name"] == st.session_state.user_name and rx.get("status") == "Active"]) > 3:
        if st.button("💊 View All Prescriptions", use_container_width=True, type="secondary"):
            st.info("Navigation to Prescriptions page coming soon!")
else:
    st.info("No active prescriptions.")

st.markdown("---")

# Bottom section - Important notices