"""Patient Lab Results Page."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_LAB_RESULTS
from components.sidebar import patient_sidebar


st.set_page_config(
    page_title="My Lab Results",
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

st.title("🧪 Lab Results")
st.caption("Access every lab test ordered for you, including downloadable reports.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    filter_type = st.selectbox(
        "Test Type", ["All", "Blood Work", "Lipid Panel", "Urinalysis", "X-Ray"]
    )
with col2:
    date_range = st.selectbox(
        "Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "Last Year"]
    )

st.markdown("---")

# Initialize lab results in session state if not exists (shared from doctor workflow)
if 'lab_results' not in st.session_state:
    st.session_state.lab_results = MOCK_LAB_RESULTS.copy()

user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()

# Filter to only show shared results
patient_results = [
    lab for lab in st.session_state.lab_results
    if (lab.get("patient_id") == user_id or lab.get("patient_name") == user_name)
    and lab.get("review_status") == "Shared with Patient"  # ONLY show shared results
]

if patient_results:
    st.success(f"✅ {len(patient_results)} lab result(s) available")
    
    for lab in patient_results:
        # Green status for shared results
        with st.expander(f"✅ **{lab['test_type']}** - {lab['date']}", expanded=False):
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown(f"**Test Type:** {lab['test_type']}")
                st.markdown(f"**Date:** {lab['date']}")
            
            with col_info2:
                st.markdown(f"**Ordered by:** {lab['ordered_by']}")
                st.markdown("**Status:** <span style='color: #00A896; font-weight: bold;'>✓ Results Reviewed</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Lab Values:**")
            
            # Display results in a more readable format
            for test_name, result in lab["results"].items():
                # Color code based on normal/abnormal
                if "Normal" in str(result):
                    st.markdown(f"- ✓ **{test_name}:** {result}")
                else:
                    st.markdown(f"- ⚠️ **{test_name}:** {result}")
            
            # Show doctor's interpretation
            st.markdown("---")
            st.markdown("**Doctor's Interpretation:**")
            interpretation = lab.get('interpretation', '')
            if interpretation:
                st.info(f"📝 {interpretation}")
            else:
                st.caption("No additional notes from your doctor.")

            st.markdown("---")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button(
                    "📄 Download PDF",
                    key=f"download_{lab['id']}",
                    use_container_width=True,
                    disabled=True
                ):
                    st.info("PDF download coming soon!")
                st.caption("Coming soon")
            
            with col_d2:
                if st.button(
                    "📧 Email to Me",
                    key=f"email_{lab['id']}",
                    use_container_width=True,
                    disabled=True
                ):
                    st.info("Email feature coming soon!")
                st.caption("Coming soon")
else:
    st.info("📋 No lab results available yet.\n\nNew test results will appear here automatically once your doctor has reviewed and shared them.")
