"""Doctor Prescriptions Page - View and manage prescriptions."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_PRESCRIPTIONS
from components.cards import prescription_card

from components.sidebar import doctor_sidebar

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
        with open("styles/main.css") as f:
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
st.markdown("### Prescription Management")

# Initialize prescriptions in session state (shared with patient workflow)
if 'prescriptions' not in st.session_state:
    st.session_state.prescriptions = MOCK_PRESCRIPTIONS.copy()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Active Prescriptions", "Refill Requests", "History"])

# Get current doctor's name
doctor_name = SessionManager.get_user_name()

with tab1:
    # Filter prescriptions by doctor
    doctor_prescriptions = [
        rx for rx in st.session_state.prescriptions
        if rx.get("prescribed_by") == doctor_name or rx.get("doctor_id") == SessionManager.get_user_id()
    ]
    
    # Apply search filter
    if search_patient:
        doctor_prescriptions = [
            rx for rx in doctor_prescriptions 
            if search_patient.lower() in rx.get("patient_name", "").lower()
        ]
    
    # Filter to active only for this tab
    active_prescriptions = [rx for rx in doctor_prescriptions if rx.get("status") == "Active"]
    
    if active_prescriptions:
        for rx in active_prescriptions:
            col1, col2 = st.columns([5, 1])
            
            with col1:
                status_color = "#00A896"
                refills_remaining = rx.get("refills_remaining", 0)
                refill_warning = "⚠️ Low refills" if refills_remaining <= 1 else ""
                
                st.markdown(
                    f"""
                    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid {status_color}; margin-bottom: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #2B2D42;">{rx['medication']} {refill_warning}</h4>
                        <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                            • <strong>Patient:</strong> {rx.get('patient_name', 'Unknown')}<br>
                            • <strong>Dosage:</strong> {rx['dosage']}<br>
                            • <strong>Instructions:</strong> {rx['instructions']}<br>
                            • <strong>Refills Remaining:</strong> {refills_remaining} of {rx.get('refills_authorized', 0)}<br>
                            • <strong>Prescribed:</strong> {rx.get('date', 'N/A')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with col2:
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                if st.button("👁️ View", key=f"view_{rx['id']}", use_container_width=True):
                    st.info(f"Viewing details for {rx['medication']}")
                if st.button("✏️ Modify", key=f"modify_{rx['id']}", use_container_width=True, disabled=True):
                    st.warning("Modification feature coming soon")
                st.caption("Coming soon")
    else:
        st.info("No active prescriptions found.")

with tab2:
    # Refill Requests Tab
    st.markdown("#### Pending Refill Requests")
    
    refill_requests = [
        rx for rx in st.session_state.prescriptions
        if (rx.get("prescribed_by") == doctor_name or rx.get("doctor_id") == SessionManager.get_user_id())
        and rx.get("refill_status") == "Pending"
    ]
    
    if refill_requests:
        st.info(f"🔔 {len(refill_requests)} refill request(s) awaiting approval")
        
        for rx in refill_requests:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(
                        f"""
                        <div style="background: #FFF8E1; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid #F77F00; margin-bottom: 16px;">
                            <h4 style="margin: 0 0 12px 0; color: #2B2D42;">🕐 {rx['medication']}</h4>
                            <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                                • <strong>Patient:</strong> {rx.get('patient_name', 'Unknown')}<br>
                                • <strong>Dosage:</strong> {rx['dosage']}<br>
                                • <strong>Current Refills Remaining:</strong> {rx.get('refills_remaining', 0)} of {rx.get('refills_authorized', 0)}<br>
                                • <strong>Original Date:</strong> {rx.get('date', 'N/A')}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with col2:
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    
                    if st.button("✅ Approve", key=f"approve_{rx['id']}", use_container_width=True, type="primary"):
                        # Update refill status
                        for i, prescription in enumerate(st.session_state.prescriptions):
                            if prescription['id'] == rx['id']:
                                st.session_state.prescriptions[i]['refill_status'] = "Approved"
                                # Don't decrement refills yet - that happens when picked up
                        st.success(f"✅ Refill approved for {rx['patient_name']}! Notification sent to patient and pharmacy.")
                        st.balloons()
                        st.rerun()
                    
                    if st.button("❌ Deny", key=f"deny_{rx['id']}", use_container_width=True):
                        for i, prescription in enumerate(st.session_state.prescriptions):
                            if prescription['id'] == rx['id']:
                                st.session_state.prescriptions[i]['refill_status'] = "Denied"
                                st.session_state.prescriptions[i]['refill_requested'] = False
                        st.warning("Refill request denied")
                        st.rerun()
    else:
        st.success("✅ No pending refill requests")

with tab3:
    # History Tab
    all_prescriptions = [
        rx for rx in st.session_state.prescriptions
        if rx.get("prescribed_by") == doctor_name or rx.get("doctor_id") == SessionManager.get_user_id()
    ]
    
    st.markdown(f"Total prescriptions written: **{len(all_prescriptions)}**")
    
    # Simple table view
    if all_prescriptions:
        import pandas as pd
        df_data = []
        for rx in all_prescriptions:
            df_data.append({
                "Patient": rx.get('patient_name', 'Unknown'),
                "Medication": rx['medication'],
                "Date": rx.get('date', 'N/A'),
                "Status": rx.get('status', 'Active'),
                "Refills": f"{rx.get('refills_remaining', 0)}/{rx.get('refills_authorized', 0)}"
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No prescription history found.")

st.markdown("---")

# Statistics
st.markdown("### Prescription Statistics")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

# Get all doctor prescriptions for stats
all_doctor_rx = [
    rx for rx in st.session_state.prescriptions
    if rx.get("prescribed_by") == doctor_name or rx.get("doctor_id") == SessionManager.get_user_id()
]

with stat_col1:
    st.metric("Total Prescribed", len(all_doctor_rx))
with stat_col2:
    active_count = len([rx for rx in all_doctor_rx if rx.get("status") == "Active"])
    st.metric("Active", active_count)
with stat_col3:
    pending_refills = len([rx for rx in all_doctor_rx if rx.get("refill_status") == "Pending"])
    st.metric("Pending Refill Requests", pending_refills)
with stat_col4:
    low_refills = len([rx for rx in all_doctor_rx if rx.get("refills_remaining", 0) <= 1 and rx.get("status") == "Active"])
    st.metric("Low Refills", low_refills)
