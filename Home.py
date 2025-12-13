"""
MediCare Health System - Login Page
Main entry point for the application.
"""
import streamlit as st
from Services.session_manager import SessionManager
from Components.login_Portal import login_form, mock_login_buttons
from Config.settings import APP_NAME

# Page configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# Initialize session
SessionManager.init_session()

# Load CSS
def load_css():
    """Load custom CSS styles."""
    try:
        with open("Styles/main.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        with open("Styles/login.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS files not found. Using default styling.")

load_css()

# Check if already logged in
if SessionManager.is_authenticated():
    role = SessionManager.get_user_role()
    if role == "patient":
        st.switch_page("Pages/Patient/Patient_Dashboard.py")
    elif role == "doctor":
        st.switch_page("Pages/Doctor/Doctor_Dashboard.py")
    elif role == "admin":
        st.switch_page("Pages/Admin/Admin_Dashboard.py")
    else:
        st.warning("Unable to determine your role. Please log in again.")
        SessionManager.logout()
        st.rerun()

# Login Page Header
st.markdown("""
    <div style="text-align: center; padding: 10px 20px;">
        <div style="font-size: 72px; margin-bottom: 16px;"></div>
        <h1 style="color: #0066CC; margin-bottom: 4px; font-size: 42px;">CARELINK</h1>
        <p style="color: #6B7280; font-size: 18px; margin-top: 0;">Modern Healthcare Management Platform</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Center content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Traditional Login Form (Non-functional for now)
    login_form()
    
   
    # Divider
    st.markdown("---")
    
    # Mock Login Section
    mock_login_buttons()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 14px; padding: 20px;">
        <p>Your health information is secure and private</p>
        <p style="margin-top: 8px;">© 2025 CARELINK Health System. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
