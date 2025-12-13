"""Doctor Prescriptions Page - View and manage prescriptions."""
import streamlit as st
from Services.session_manager import SessionManager
from Database.mock_Data import MOCK_PRESCRIPTIONS
from Components.cards import prescription_card

from Components.sidebar import doctor_sidebar

# Page config
st.set_page_config(
    page_title="Prescriptions",
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

st.title("💊 Prescriptions Management")
st.caption("View and manage prescriptions for your patients.")
st.markdown("---")

# Filter options
col1, col2, col3 = st.columns(3)
with col1:
    filter_status = st.selectbox("Status", ["All", "Active", "Expired", "Pending Refill"])
with col2:
    sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Medication Name", "Patient Name"])
with col3:
    search_patient = st.text_input("🔍 Search Patient", placeholder="Patient name...")

st.markdown("---")

# Action buttons
col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("➕ Write New Prescription", use_container_width=True, type="primary"):
        st.session_state.show_new_prescription_form = True

# Show new prescription form if button clicked
if st.session_state.get('show_new_prescription_form', False):
    st.markdown("### Write New Prescription")
    
    with st.form("new_prescription_form"):
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            patient_name = st.text_input("Patient Name*")
            medication = st.text_input("Medication Name*")
            dosage = st.text_input("Dosage*", placeholder="e.g., 500mg")
        
        with form_col2:
            frequency = st.text_input("Frequency*", placeholder="e.g., Twice daily")
            duration = st.text_input("Duration", placeholder="e.g., 30 days")
            refills = st.number_input("Refills Allowed", min_value=0, max_value=12, value=3)
        
        instructions = st.text_area("Special Instructions", placeholder="Take with food, avoid alcohol, etc.")
        
        submit_col1, submit_col2 = st.columns([1, 4])
        with submit_col1:
            submitted = st.form_submit_button("Submit Prescription", type="primary", use_container_width=True)
        with submit_col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
        
        if submitted:
            if patient_name and medication and dosage and frequency:
                st.success(f"✅ Prescription for {medication} created for {patient_name}")
                st.session_state.show_new_prescription_form = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")
        
        if cancelled:
            st.session_state.show_new_prescription_form = False
            st.rerun()
    
    st.markdown("---")

# Display recent prescriptions written by doctor
st.markdown("### Recent Prescriptions Written")

# Get current doctor's name
doctor_name = SessionManager.get_user_name()

# Filter prescriptions by doctor
doctor_prescriptions = [
    rx for rx in MOCK_PRESCRIPTIONS 
    if rx.get("prescribed_by") == doctor_name or rx.get("doctor_id") == SessionManager.get_user_id()
]

# Apply search filter
if search_patient:
    doctor_prescriptions = [
        rx for rx in doctor_prescriptions 
        if search_patient.lower() in rx.get("patient_name", "").lower()
    ]

# Apply status filter
if filter_status != "All":
    doctor_prescriptions = [
        rx for rx in doctor_prescriptions 
        if rx.get("status", "Active") == filter_status
    ]

if doctor_prescriptions:
    for rx in doctor_prescriptions:
        col1, col2 = st.columns([5, 1])
        
        with col1:
            status_color = "#00A896" if rx.get("status", "Active") == "Active" else "#F77F00"
            st.markdown(
                f"""
                <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid {status_color}; margin-bottom: 16px;">
                    <h4 style="margin: 0 0 12px 0; color: #2B2D42;">{rx['medication']}</h4>
                    <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                        • <strong>Patient:</strong> {rx.get('patient_name', 'Unknown')}<br>
                        • <strong>Dosage:</strong> {rx['dosage']}<br>
                        • <strong>Instructions:</strong> {rx['instructions']}<br>
                        • <strong>Refills Remaining:</strong> {rx.get('refills', 0)}<br>
                        • <strong>Status:</strong> <span style="color: {status_color};">{rx.get('status', 'Active')}</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col2:
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            if st.button("View Details", key=f"view_{rx['id']}", use_container_width=True):
                st.info(f"Viewing details for {rx['medication']}")
            if st.button("Modify", key=f"modify_{rx['id']}", use_container_width=True):
                st.warning(f"Modification feature coming soon")
else:
    st.info("No prescriptions found matching your criteria.")

st.markdown("---")

# Statistics
st.markdown("### Prescription Statistics")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Prescribed", len(doctor_prescriptions))
with stat_col2:
    active_count = len([rx for rx in doctor_prescriptions if rx.get("status", "Active") == "Active"])
    st.metric("Active", active_count)
with stat_col3:
    refill_pending = len([rx for rx in doctor_prescriptions if rx.get("refills", 0) == 0])
    st.metric("Pending Refill", refill_pending)
with stat_col4:
    st.metric("This Month", len(doctor_prescriptions[:5]))
