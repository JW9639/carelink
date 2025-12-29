"""Doctor Profile Page."""
import streamlit as st
from services.session_manager import SessionManager

from components.sidebar import doctor_sidebar


st.set_page_config(
    page_title="Doctor Profile",
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

SessionManager.init_session()
SessionManager.require_auth(allowed_roles=["doctor"])

doctor_sidebar()

st.title("👨‍⚕️ Doctor Profile")
st.caption("Manage your professional profile and credentials.")
st.markdown("---")

user_data = SessionManager.get_user_data() or {}

tab1, tab2, tab3 = st.tabs(["📋 Personal Info", "🔐 Security", "⚙️ Preferences"])

with tab1:
    st.markdown("### Personal Information")
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Full Name", value=user_data.get("name", ""), disabled=False)
        st.text_input("Email", value=user_data.get("email", ""), disabled=False)
        st.text_input("Phone", value=user_data.get("phone", ""), disabled=False)

    with col2:
        st.text_input("Role", value="Doctor", disabled=True)
        st.text_input("Doctor ID", value=user_data.get("id", ""), disabled=True)

    st.markdown("---")
    st.markdown("### Professional Information")
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("Specialty", value=user_data.get("specialty", ""), disabled=False)
        st.text_input("License Number", value=user_data.get("license", ""), disabled=True)
    with col4:
        st.text_input("Department", value=user_data.get("department", ""), disabled=False)
        st.text_input("Years of Experience", value=user_data.get("experience", ""), disabled=False)

    st.markdown("---")
    if st.button("Save Profile Changes", type="primary", use_container_width=True):
        st.success("Profile updated successfully! (Mock)")

with tab2:
    st.markdown("### Security Settings")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password", type="primary"):
        if new_password == confirm_password:
            st.success("Password updated successfully! (Mock)")
        else:
            st.error("Passwords do not match")

    st.markdown("---")
    two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
    if two_factor:
        st.info("Two-factor authentication will be configured when you save.")

    st.markdown("---")
    st.markdown("#### Active Session")
    st.markdown(
        """
        <div style="background: white; border-radius: 8px; padding: 16px; margin: 8px 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);">
            <strong>Current Session</strong><br>
            <span style="color: #6B7280; font-size: 14px;">
                Device: Local Browser<br>
                Location: Localhost<br>
                Last Active: Now
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Sign Out All Other Devices"):
        st.info("All other sessions terminated (Mock)")

with tab3:
    st.markdown("### Preferences")
    st.markdown("#### Notifications")
    col5, col6 = st.columns(2)
    with col5:
        st.checkbox("Email Notifications", value=True)
        st.checkbox("SMS Notifications", value=False)
    with col6:
        st.checkbox("Push Notifications", value=True)
        st.checkbox("Patient Update Alerts", value=True)

    st.markdown("---")
    st.markdown("#### Appearance")
    st.selectbox("Theme", ["Light", "Dark", "Auto"])
    st.selectbox("Language", ["English", "Spanish", "French"])

    st.markdown("---")
    st.checkbox(
        "Share anonymous usage data to improve the platform",
        value=False,
        help="Turning this on helps us improve doctor tools.",
    )

    st.markdown("---")
    if st.button("Save Preferences", type="primary", use_container_width=True):
        st.success("Preferences saved successfully! (Mock)")
