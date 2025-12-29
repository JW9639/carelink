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

# Initialize prescriptions in session state if not exists
if 'prescriptions' not in st.session_state:
    st.session_state.prescriptions = MOCK_PRESCRIPTIONS.copy()

user_id = SessionManager.get_user_id()
user_name = SessionManager.get_user_name()
patient_prescriptions = [
    rx for rx in st.session_state.prescriptions
    if rx.get("patient_id") == user_id or rx.get("patient_name") == user_name
]

# Apply filters
if filter_status != "All":
    if filter_status == "Pending Refill":
        patient_prescriptions = [rx for rx in patient_prescriptions if rx.get("refill_status") == "Pending"]
    elif filter_status == "Active":
        patient_prescriptions = [rx for rx in patient_prescriptions if rx.get("status") == "Active"]

if patient_prescriptions:
    for rx in patient_prescriptions:
        refill_status = rx.get("refill_status", "None")
        refills_remaining = rx.get("refills_remaining", 0)
        
        # Status badge
        if refill_status == "Pending":
            status_badge = "🕐 Refill Pending"
            badge_color = "#F77F00"
        elif refill_status == "Approved":
            status_badge = "✅ Refill Approved"
            badge_color = "#00A896"
        elif refills_remaining == 0:
            status_badge = "⚠️ No Refills Remaining"
            badge_color = "#E63946"
        else:
            status_badge = "✓ Active"
            badge_color = "#00A896"
        
        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(
                f"""
                <div style="background: white; border-radius: 12px 0 0 12px; padding: 20px 10px 20px 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border-left: 4px solid {badge_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h4 style="margin: 0; color: #2B2D42;">{rx['medication']}</h4>
                        <span style="color: {badge_color}; font-weight: 600; font-size: 14px;">{status_badge}</span>
                    </div>
                    <p style="margin: 4px 0; color: #6B7280; font-size: 15px; line-height: 1.8;">
                        • <strong>Dosage:</strong> {rx['dosage']}<br>
                        • <strong>Instructions:</strong> {rx['instructions']}<br>
                        • <strong>Refills Remaining:</strong> {refills_remaining} of {rx.get('refills_authorized', 0)}<br>
                        • <strong>Prescribed by:</strong> {rx['prescribed_by']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("<div style='margin-top: -8px;'></div>", unsafe_allow_html=True)
            
            # Refill button logic
            can_request_refill = (refill_status == "None" and refills_remaining > 0) or refill_status == "Approved"
            button_disabled = not can_request_refill
            
            if refill_status == "Pending":
                st.button("⏳ Pending", key=f"refill_{rx['id']}", use_container_width=True, disabled=True)
                st.caption("Request sent")
            elif refill_status == "Approved":
                if st.button("✅ Pick Up", key=f"pickup_{rx['id']}", use_container_width=True, type="primary"):
                    st.success("Prescription ready at pharmacy!")
            elif refills_remaining == 0:
                st.button("❌ No Refills", key=f"no_refill_{rx['id']}", use_container_width=True, disabled=True)
                st.caption("Contact doctor")
            else:
                if st.button("📝 Request Refill", key=f"refill_{rx['id']}", type="primary", use_container_width=True):
                    # Update refill status
                    for i, prescription in enumerate(st.session_state.prescriptions):
                        if prescription['id'] == rx['id']:
                            st.session_state.prescriptions[i]['refill_status'] = "Pending"
                            st.session_state.prescriptions[i]['refill_requested'] = True
                    st.success(f"✅ Refill request sent to {rx['prescribed_by']}!")
                    st.balloons()
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Summary stats
    total_active = len([rx for rx in patient_prescriptions if rx.get("status") == "Active"])
    pending_refills = len([rx for rx in patient_prescriptions if rx.get("refill_status") == "Pending"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Prescriptions", total_active)
    with col2:
        st.metric("Pending Refills", pending_refills)
    with col3:
        need_refills = len([rx for rx in patient_prescriptions if rx.get("refills_remaining", 0) == 0])
        st.metric("Need Doctor Contact", need_refills)
else:
    st.info("No prescriptions found for your account.")
