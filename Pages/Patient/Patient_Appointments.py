"""Patient Appointments Page."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_APPOINTMENTS
from components.cards import appointment_card
from components.sidebar import patient_sidebar


st.set_page_config(
    page_title="My Appointments",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css():
    """Load custom CSS styles."""
    try:
        with open("styles/main.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css()

# Initialize session and restrict to patients
SessionManager.init_session()
SessionManager.require_auth(allowed_roles=["patient"])

patient_sidebar()

st.title("📅 Your Appointments")
st.caption("Track and manage every upcoming visit in one place.")
st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    filter_status = st.selectbox("Status", ["All", "Confirmed", "Pending", "Cancelled"])
with col2:
    filter_date = st.selectbox("Time Period", ["All", "Today", "This Week", "This Month"])
with col3:
    sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Doctor", "Type"])

st.markdown("---")

# Patient-specific appointments
user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()
appointments = [
    apt
    for apt in MOCK_APPOINTMENTS
    if apt.get("patient_id") == user_id or apt.get("patient_name") == user_name
]

st.subheader("Upcoming Visits")
if appointments:
    for appointment in appointments:
        appointment_card(appointment)
else:
    st.info("No appointments found. Once you schedule a visit, it will appear here.")

st.markdown("---")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("Schedule New Appointment", use_container_width=True, type="primary"):
        st.info("Appointment scheduling feature coming soon!")
with col_btn2:
    if st.button("Export My Schedule", use_container_width=True):
        st.info("Export feature coming soon!")
