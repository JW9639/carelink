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

# Initialize appointments in session state if not exists
if 'appointments' not in st.session_state:
    st.session_state.appointments = MOCK_APPOINTMENTS.copy()

# Patient-specific appointments
user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()
appointments = [
    apt
    for apt in st.session_state.appointments
    if apt.get("patient_id") == user_id or apt.get("patient_name") == user_name
]

# Apply filters
if filter_status != "All":
    appointments = [apt for apt in appointments if apt.get("status") == filter_status]

st.subheader("Upcoming Visits")
if appointments:
    for appointment in appointments:
        appointment_card(appointment)
else:
    st.info("No appointments found matching your criteria.")

st.markdown("---")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📅 Schedule New Appointment", use_container_width=True, type="primary"):
        st.session_state.show_booking_form = True
with col_btn2:
    if st.button("📊 Export My Schedule", use_container_width=True, disabled=True):
        st.info("Export feature coming soon!")
    st.caption("Coming soon")

# Appointment Booking Form
if st.session_state.get('show_booking_form', False):
    st.markdown("---")
    st.markdown("### 📝 Schedule New Appointment")
    
    with st.form("book_appointment_form"):
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            doctor_choice = st.selectbox(
                "Select Doctor*",
                ["Dr. Sarah Johnson - Cardiology", "Dr. Michael Chen - General Practice", "Dr. Emily Brown - Pediatrics"]
            )
            appointment_type = st.selectbox(
                "Appointment Type*",
                ["General Checkup", "Follow-up", "Consultation", "Urgent Care", "Annual Physical"]
            )
            preferred_date = st.date_input("Preferred Date*")
        
        with form_col2:
            preferred_time = st.selectbox(
                "Preferred Time*",
                ["9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
            )
            duration = st.selectbox("Estimated Duration", ["15 minutes", "30 minutes", "45 minutes", "1 hour"])
        
        reason = st.text_area(
            "Reason for Visit (Optional)",
            placeholder="Briefly describe the reason for your appointment...",
            height=100
        )
        
        st.markdown("---")
        submit_col1, submit_col2 = st.columns([1, 4])
        with submit_col1:
            submitted = st.form_submit_button("📤 Submit Request", type="primary", use_container_width=True)
        with submit_col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
        
        if submitted:
            if doctor_choice and appointment_type and preferred_date and preferred_time:
                # Create new appointment
                new_appointment = {
                    "id": f"APT{len(st.session_state.appointments) + 1:03d}",
                    "patient_id": user_id,
                    "patient_name": user_name,
                    "doctor_id": "D001",  # Would map from doctor_choice
                    "doctor_name": doctor_choice.split(" - ")[0],
                    "date": str(preferred_date),
                    "time": preferred_time,
                    "type": appointment_type,
                    "status": "Pending",
                    "notes": reason if reason else "No additional notes"
                }
                
                # Add to session state
                st.session_state.appointments.append(new_appointment)
                st.session_state.show_booking_form = False
                
                st.success(f"✅ Appointment request sent to {doctor_choice.split(' - ')[0]}!\n\nYou'll receive confirmation within 24 hours.")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Please fill in all required fields (*)")
        
        if cancelled:
            st.session_state.show_booking_form = False
            st.rerun()
