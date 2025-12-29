"""Doctor Lab Results Page - View and manage lab test results."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_LAB_RESULTS
import pandas as pd

from components.sidebar import doctor_sidebar

# Page config
st.set_page_config(
    page_title="Lab Results",
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

st.title("🔬 Lab Results Management")
st.caption("Review lab test results for your patients and order new tests.")
st.markdown("---")

# Filter options
col1, col2, col3 = st.columns(3)
with col1:
    filter_type = st.selectbox("Test Type", ["All", "Blood Work", "Lipid Panel", "Urinalysis", "X-Ray", "MRI", "CT Scan"])
with col2:
    date_range = st.selectbox("Date Range", ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year"])
with col3:
    search_patient = st.text_input("🔍 Search Patient", placeholder="Patient name...")

st.markdown("---")

# Action buttons
col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("➕ Order New Lab Test", use_container_width=True, type="primary"):
        st.session_state.show_new_lab_order = True

# Show new lab order form if button clicked
if st.session_state.get('show_new_lab_order', False):
    st.markdown("### Order New Lab Test")
    
    with st.form("new_lab_order_form"):
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            patient_name = st.text_input("Patient Name*")
            test_type = st.selectbox("Test Type*", [
                "Complete Blood Count (CBC)",
                "Lipid Panel",
                "Comprehensive Metabolic Panel",
                "Urinalysis",
                "Thyroid Panel",
                "Liver Function Tests",
                "X-Ray",
                "MRI",
                "CT Scan"
            ])
        
        with form_col2:
            priority = st.selectbox("Priority", ["Routine", "Urgent", "STAT"])
            collection_date = st.date_input("Collection Date")
        
        special_instructions = st.text_area("Special Instructions", placeholder="Fasting required, specific collection time, etc.")
        clinical_notes = st.text_area("Clinical Notes", placeholder="Reason for test, symptoms, etc.")
        
        submit_col1, submit_col2 = st.columns([1, 4])
        with submit_col1:
            submitted = st.form_submit_button("Submit Order", type="primary", use_container_width=True)
        with submit_col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
        
        if submitted:
            if patient_name and test_type:
                st.success(f"✅ Lab order for {test_type} created for {patient_name}")
                st.session_state.show_new_lab_order = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")
        
        if cancelled:
            st.session_state.show_new_lab_order = False
            st.rerun()
    
    st.markdown("---")

# Display lab results
st.markdown("### Recent Lab Results for Your Patients")

# Get current doctor's name
doctor_name = SessionManager.get_user_name()

# Filter lab results by doctor
doctor_lab_results = [
    lab for lab in MOCK_LAB_RESULTS 
    if lab.get("ordered_by") == doctor_name or lab.get("doctor_id") == SessionManager.get_user_id()
]

# Apply search filter
if search_patient:
    doctor_lab_results = [
        lab for lab in doctor_lab_results 
        if search_patient.lower() in lab.get("patient_name", "").lower()
    ]

# Apply test type filter
if filter_type != "All":
    doctor_lab_results = [
        lab for lab in doctor_lab_results 
        if lab.get("test_type", "") == filter_type
    ]

if doctor_lab_results:
    for lab in doctor_lab_results:
        status_color = "#00A896" if lab.get("status") == "Completed" else "#F77F00"
        
        with st.expander(
            f"**{lab.get('patient_name', 'Unknown Patient')}** - {lab['test_type']} ({lab['date']})", 
            expanded=False
        ):
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown(f"**Patient:** {lab.get('patient_name', 'Unknown')}")
                st.markdown(f"**Test Type:** {lab['test_type']}")
                st.markdown(f"**Date:** {lab['date']}")
            
            with col_info2:
                st.markdown(f"**Status:** <span style='color: {status_color};'>{lab['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Ordered by:** {lab.get('ordered_by', 'Dr. Unknown')}")
            
            st.markdown("---")
            st.markdown("**Results:**")
            
            results_data = []
            for test_name, result in lab['results'].items():
                results_data.append({
                    "Test": test_name,
                    "Result": result,
                    "Status": "Normal" if "Normal" in str(result) else "Review"
                })
            
            if results_data:
                results_df = pd.DataFrame(results_data)
                st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Doctor actions
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col1:
                if st.button("Add Interpretation", key=f"interpret_{lab['id']}", use_container_width=True):
                    st.session_state[f"show_interpretation_{lab['id']}"] = True
            
            with action_col2:
                if st.button("Download Report", key=f"download_{lab['id']}", use_container_width=True):
                    st.info("PDF download coming soon!")
            
            with action_col3:
                if st.button("Share with Patient", key=f"share_{lab['id']}", use_container_width=True):
                    st.success("Results shared with patient!")
            
            # Show interpretation form if requested
            if st.session_state.get(f"show_interpretation_{lab['id']}", False):
                st.markdown("**Add Clinical Interpretation:**")
                interpretation = st.text_area(
                    "Interpretation", 
                    key=f"interpretation_text_{lab['id']}",
                    placeholder="Enter your clinical interpretation of these results..."
                )
                
                interp_col1, interp_col2 = st.columns([1, 3])
                with interp_col1:
                    if st.button("Save Interpretation", key=f"save_interp_{lab['id']}", type="primary"):
                        st.success("Interpretation saved!")
                        st.session_state[f"show_interpretation_{lab['id']}"] = False
                        st.rerun()
                with interp_col2:
                    if st.button("Cancel", key=f"cancel_interp_{lab['id']}"):
                        st.session_state[f"show_interpretation_{lab['id']}"] = False
                        st.rerun()
else:
    st.info("No lab results found matching your criteria.")

st.markdown("---")

# Statistics
st.markdown("### Lab Test Statistics")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Tests Ordered", len(doctor_lab_results))
with stat_col2:
    completed_count = len([lab for lab in doctor_lab_results if lab.get("status") == "Completed"])
    st.metric("Completed", completed_count)
with stat_col3:
    pending_count = len([lab for lab in doctor_lab_results if lab.get("status") == "Pending"])
    st.metric("Pending", pending_count)
with stat_col4:
    st.metric("This Month", len(doctor_lab_results[:5]))
