"""Patient Prescriptions Page."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_PRESCRIPTIONS
from components.sidebar import patient_sidebar


st.set_page_config(
    page_title="My Prescriptions",
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

st.title("💊 Active Prescriptions")
st.caption("Refill medications and review instructions prescribed by your doctors.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    filter_status = st.selectbox(
        "Status", ["All", "Active", "Expired", "Pending Refill"]
    )
with col2:
    sort_by = st.selectbox(
        "Sort By", ["Date (Newest)", "Date (Oldest)", "Medication Name"]
    )

st.markdown("---")

user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()
patient_prescriptions = [
    rx for rx in MOCK_PRESCRIPTIONS if rx.get("patient_id") == user_id
]
if not patient_prescriptions and user_name:
    patient_prescriptions = [
        rx for rx in MOCK_PRESCRIPTIONS if rx.get("patient_name") == user_name
    ]

if patient_prescriptions:
    for rx in patient_prescriptions:
        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(
                f"""
                <div style="background: white; border-radius: 12px 0 0 12px; padding: 20px 10px 20px 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid #00A896;">
                    <h4 style="margin: 0 0 12px 0; color: #2B2D42;">{rx['medication']}</h4>
                    <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                        • <strong>Dosage:</strong> {rx['dosage']}<br>
                        • <strong>Instructions:</strong> {rx['instructions']}<br>
                        • <strong>Refills:</strong> {rx['refills']} remaining<br>
                        • <strong>Prescribed by:</strong> {rx['prescribed_by']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("<div style='margin-top: -8px;'></div>", unsafe_allow_html=True)
            if st.button(
                "Refill", key=f"refill_{rx['id']}", type="primary", use_container_width=True
            ):
                st.success(f"Refill request sent for {rx['medication']}")

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Prescription History")
    st.info("No expired prescriptions")
else:
    st.info("No prescriptions found for your account.")
