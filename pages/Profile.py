"""Profile Page - View and edit user profile."""
import streamlit as st
from services.session_manager import SessionManager
from utils.helpers import calculate_age

from components.sidebar import patient_sidebar

# Page config
st.set_page_config(
    page_title="Profile",
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
st.title("My Profile")

# Sidebar Navigation
patient_sidebar()

st.markdown("---")

# Get user data
user_data = SessionManager.get_user_data()
role = SessionManager.get_user_role()

# Profile sections
tab1, tab2, tab3 = st.tabs(["📋 Personal Info", "🔐 Security", "⚙️ Settings"])

with tab1:
    st.markdown("### Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", value=user_data.get('name', ''), disabled=False)
        st.text_input("Email", value=user_data.get('email', ''), disabled=False)
        st.text_input("Phone", value=user_data.get('phone', ''), disabled=False)
        
        if role == "patient":
            st.date_input("Date of Birth", value=None)
            st.text_input("Address", value=user_data.get('address', ''), disabled=False)
    
    with col2:
        st.text_input("Role", value=role.title(), disabled=True)
        st.text_input("User ID", value=user_data.get('id', ''), disabled=True)
        
        if role == "doctor":
            st.text_input("Specialty", value=user_data.get('specialty', ''), disabled=False)
            st.text_input("License Number", value=user_data.get('license', ''), disabled=True)
    
    st.markdown("---")
    
    if role == "patient":
        st.markdown("### Medical Information")
        col3, col4 = st.columns(2)
        with col3:
            st.text_input("Blood Type", value="O+", disabled=False)
            st.text_area("Allergies", value="None", height=100)
        with col4:
            st.text_area("Current Medications", value="See Prescriptions page", height=100)
            st.text_input("Emergency Contact", value="", disabled=False)
    
    st.markdown("---")
    
    if st.button("Save Changes", type="primary", use_container_width=True):
        st.success("Profile updated successfully! (Mock)")

with tab2:
    st.markdown("### Security Settings")
    
    st.markdown("#### Change Password")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Update Password", type="primary"):
        if new_password == confirm_password:
            st.success("Password updated successfully! (Mock)")
        else:
            st.error("Passwords do not match")
    
    st.markdown("---")
    
    st.markdown("#### Two-Factor Authentication")
    two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
    
    if two_factor:
        st.info("Two-factor authentication will be configured when you save.")
    
    st.markdown("---")
    
    st.markdown("#### Active Sessions")
    st.markdown("""
        <div style="background: white; border-radius: 8px; padding: 16px; margin: 8px 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);">
            <strong>Current Session</strong><br>
            <span style="color: #6B7280; font-size: 14px;">
                Device: Windows PC<br>
                Location: Local<br>
                Last Active: Now
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Sign Out All Other Devices"):
        st.info("All other sessions terminated (Mock)")

with tab3:
    st.markdown("### Preferences")
    
    st.markdown("#### Notifications")
    email_notif = st.checkbox("Email Notifications", value=True)
    sms_notif = st.checkbox("SMS Notifications", value=False)
    push_notif = st.checkbox("Push Notifications", value=True)
    
    st.markdown("---")
    
    st.markdown("#### Appearance")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    language = st.selectbox("Language", ["English", "Spanish", "French"])
    
    st.markdown("---")
    
    st.markdown("#### Privacy")
    share_data = st.checkbox("Share anonymous usage data to improve the platform", value=False)
    
    st.markdown("---")
    
    if st.button("Save Preferences", type="primary", use_container_width=True):
        st.success("Preferences saved successfully! (Mock)")
