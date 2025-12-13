"""Patient Lab Results Page."""
import streamlit as st
from Services.session_manager import SessionManager
from Database.mock_Data import MOCK_LAB_RESULTS
from Components.sidebar import patient_sidebar


st.set_page_config(
    page_title="My Lab Results",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css():
    """Load custom CSS styles."""
    try:
        with open("Styles/main.css") as f:
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

user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()
patient_results = [lab for lab in MOCK_LAB_RESULTS if lab.get("patient_id") == user_id]
if not patient_results and user_name:
    patient_results = [
        lab for lab in MOCK_LAB_RESULTS if lab.get("patient_name") == user_name
    ]

if patient_results:
    for lab in patient_results:
        with st.expander(f"**{lab['test_type']}** - {lab['date']}", expanded=False):
            st.markdown(f"**Ordered by:** {lab['ordered_by']}")
            st.markdown(f"**Status:** {lab['status']}")
            st.markdown("---")
            st.markdown("**Results:**")
            for test_name, result in lab["results"].items():
                st.markdown(f"- **{test_name}:** {result}")

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button(
                    "Download PDF",
                    key=f"download_{lab['id']}",
                    use_container_width=True,
                ):
                    st.info("PDF download coming soon!")
            with col_d2:
                if st.button(
                    "Share with Doctor",
                    key=f"share_{lab['id']}",
                    use_container_width=True,
                ):
                    st.info("Sharing feature coming soon!")
else:
    st.info("No lab results available yet. New tests will appear here automatically.")
