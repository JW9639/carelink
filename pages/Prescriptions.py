"""Prescriptions Page - View and manage prescriptions."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_PRESCRIPTIONS
from components.cards import prescription_card

from components.sidebar import patient_sidebar

# Page config
st.set_page_config(
    page_title="Prescriptions",
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
st.title("Prescriptions")
role = SessionManager.get_user_role()

# Sidebar Navigation
patient_sidebar()

st.markdown("---")

# Filter options
col1, col2 = st.columns(2)
with col1:
    filter_status = st.selectbox("Status", ["All", "Active", "Expired", "Pending Refill"])
with col2:
    sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Medication Name"])

st.markdown("---")

# Display based on role
if role == "patient":
    st.markdown("### Your Active Prescriptions")
    
    for rx in MOCK_PRESCRIPTIONS:
        # Use columns to create card with button in header
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px 0 0 12px; padding: 20px 10px 20px 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid #00A896;">
                <h4 style="margin: 0 0 12px 0; color: #2B2D42;">{rx['medication']}</h4>
                <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                    • <strong>Dosage:</strong> {rx['dosage']}<br>
                    • <strong>Instructions:</strong> {rx['instructions']}<br>
                    • <strong>Refills:</strong> {rx['refills']} remaining<br>
                    • <strong>Prescribed by:</strong> {rx['prescribed_by']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='margin-top: -8px;'></div>", unsafe_allow_html=True)
            if st.button("Refill", key=f"refill_{rx['id']}", type="primary", use_container_width=True):
                st.success(f"Refill request sent for {rx['medication']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Prescription History")
    st.info("No expired prescriptions")

elif role == "doctor":
    st.markdown("### Recent Prescriptions Written")
    
    for rx in MOCK_PRESCRIPTIONS:
        prescription_card(rx)
    
    st.markdown("---")
    
    if st.button("Write New Prescription", use_container_width=True, type="primary"):
        st.info("Prescription writing feature coming soon!")

else:
    st.markdown("### All Prescriptions in System")
    st.info(f"Total Active Prescriptions: {len(MOCK_PRESCRIPTIONS)}")
    
    for rx in MOCK_PRESCRIPTIONS:
        prescription_card(rx)
