"""Sidebar navigation components for different user roles."""
import streamlit as st
from services.session_manager import SessionManager


def patient_sidebar():
    """Display patient portal sidebar navigation."""
    with st.sidebar:
        st.markdown("### Patient Portal")
        st.info(f"**{st.session_state.user_name}**")
        st.caption("Patient Account")
        
        st.markdown("---")
        st.markdown("### Quick Links")
        
        # Add CSS for hiding Streamlit nav and tighter spacing
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebar"] button[kind="secondary"] {
            padding: 0.25rem 0.75rem !important;
            margin-bottom: 0.25rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.page_link("pages/Patient_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("pages/Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("pages/Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("pages/Profile.py", label="• Profile", use_container_width=True)
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, type="primary"):
            SessionManager.logout()
            st.switch_page("Home.py")
        
        st.markdown("---")
        st.markdown("### Emergency")
        st.error("**911** - Emergency")
        st.caption("Hospital: (555) 999-8888")


def doctor_sidebar():
    """Display doctor portal sidebar navigation."""
    # Get doctor specialty from user data
    user_data = SessionManager.get_user_data()
    specialty = user_data.get('specialty', 'General Medicine') if user_data else 'General Medicine'
    
    with st.sidebar:
        st.markdown("### Doctor Portal")
        st.info(f"**{st.session_state.user_name}**")
        st.caption(f"{specialty}")
        
        st.markdown("---")
        st.markdown("### Quick Links")
        
        # Add CSS for hiding Streamlit nav and tighter spacing
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebar"] button[kind="secondary"] {
            padding: 0.25rem 0.75rem !important;
            margin-bottom: 0.25rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.page_link("pages/Doctor_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Appointments.py", label="• Schedule", use_container_width=True)
        st.page_link("pages/Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("pages/Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("pages/Profile.py", label="• Profile", use_container_width=True)
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, type="primary"):
            SessionManager.logout()
            st.switch_page("Home.py")
        
        st.markdown("---")
        st.markdown("### Quick Contact")
        st.caption("Emergency: 911")
        st.caption("Nurse: (555) 999-8890")


def admin_sidebar():
    """Display admin portal sidebar navigation."""
    with st.sidebar:
        st.markdown("### Admin Portal")
        st.info(f"**{st.session_state.user_name}**")
        st.caption("System Administrator")
        
        st.markdown("---")
        st.markdown("### Management")
        
        # Add CSS for hiding Streamlit nav and tighter spacing
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebar"] button[kind="secondary"] {
            padding: 0.25rem 0.75rem !important;
            margin-bottom: 0.25rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.page_link("pages/Admin_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("pages/Profile.py", label="• Profile", use_container_width=True)
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, type="primary"):
            SessionManager.logout()
            st.switch_page("Home.py")
        
        st.markdown("---")
        st.markdown("### System Status")
        st.success("Operational")
        st.caption("Database: Healthy")
        st.caption("Security: Active")
