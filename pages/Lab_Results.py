"""Lab Results Page - View lab test results."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_LAB_RESULTS
import pandas as pd

from components.sidebar import patient_sidebar

# Page config
st.set_page_config(
    page_title="Lab Results",
    page_icon="🔬",
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
st.title("🔬 Lab Results")
role = SessionManager.get_user_role()

# Sidebar Navigation
patient_sidebar()

st.markdown("---")

# Filter options
col1, col2 = st.columns(2)
with col1:
    filter_type = st.selectbox("Test Type", ["All", "Blood Work", "Lipid Panel", "Urinalysis", "X-Ray"])
with col2:
    date_range = st.selectbox("Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "Last Year"])

st.markdown("---")

# Display lab results
if role == "patient":
    st.markdown("### Your Lab Results")
    
    for lab in MOCK_LAB_RESULTS:
        with st.expander(f"**{lab['test_type']}** - {lab['date']}", expanded=False):
            st.markdown(f"**Ordered by:** {lab['ordered_by']}")
            st.markdown(f"**Status:** {lab['status']}")
            st.markdown("---")
            st.markdown("**Results:**")
            
            for test_name, result in lab['results'].items():
                st.markdown(f"- **{test_name}:** {result}")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("Download PDF", key=f"download_{lab['id']}", use_container_width=True):
                    st.info("PDF download coming soon!")
            with col_d2:
                if st.button("Share with Doctor", key=f"share_{lab['id']}", use_container_width=True):
                    st.info("Sharing feature coming soon!")

elif role == "doctor":
    st.markdown("### Recent Lab Results for Your Patients")
    
    for lab in MOCK_LAB_RESULTS:
        with st.expander(f"**Patient P001** - {lab['test_type']} ({lab['date']})", expanded=False):
            st.markdown("**Results:**")
            for test_name, result in lab['results'].items():
                st.markdown(f"- **{test_name}:** {result}")
            
            if st.button("Add Interpretation", key=f"interpret_{lab['id']}", use_container_width=True):
                st.info("Interpretation feature coming soon!")

else:
    st.markdown("### All Lab Results")
    
    lab_summary = pd.DataFrame({
        "Date": ["2025-11-19", "2025-11-19"],
        "Patient": ["P001", "P001"],
        "Test Type": ["Complete Blood Count", "Lipid Panel"],
        "Status": ["Completed", "Completed"],
        "Results": ["All Normal", "All Normal"]
    })
    
    st.dataframe(lab_summary, use_container_width=True, hide_index=True)

st.markdown("---")

if role == "doctor":
    if st.button("Order New Lab Test", use_container_width=True, type="primary"):
        st.info("Lab ordering feature coming soon!")
