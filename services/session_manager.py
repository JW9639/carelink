"""Session state management for authentication and user roles."""
import streamlit as st
from datetime import datetime, timedelta

class SessionManager:
    """Manage user session state."""
    
    @staticmethod
    def init_session():
        """Initialize session state variables."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'user_name' not in st.session_state:
            st.session_state.user_name = None
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
    
    @staticmethod
    def login(user_id: str, user_name: str, role: str, user_data: dict = None):
        """Set user session after successful login."""
        st.session_state.authenticated = True
        st.session_state.user_id = user_id
        st.session_state.user_name = user_name
        st.session_state.user_role = role
        st.session_state.login_time = datetime.now()
        st.session_state.user_data = user_data
    
    @staticmethod
    def logout():
        """Clear user session."""
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.session_state.login_time = None
        st.session_state.user_data = None
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated."""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_user_role():
        """Get current user's role."""
        return st.session_state.get('user_role', None)
    
    @staticmethod
    def get_user_name():
        """Get current user's name."""
        return st.session_state.get('user_name', None)
    
    @staticmethod
    def get_user_id():
        """Get current user's ID."""
        return st.session_state.get('user_id', None)
    
    @staticmethod
    def get_user_data():
        """Get current user's full data."""
        return st.session_state.get('user_data', None)
    
    @staticmethod
    def require_auth(allowed_roles=None):
        """
        Require authentication to access a page.
        Optionally restrict to specific roles.
        """
        if not SessionManager.is_authenticated():
            st.warning("⚠️ Please log in to access this page.")
            st.info("👈 Use the Home page to log in")
            st.stop()
        
        if allowed_roles:
            current_role = SessionManager.get_user_role()
            if current_role not in allowed_roles:
                st.error("🚫 You don't have permission to access this page.")
                st.info(f"This page is restricted to: {', '.join(allowed_roles)}")
                st.stop()
    
    @staticmethod
    def check_session_timeout(timeout_seconds: int = 3600):
        """Check if session has timed out."""
        if not SessionManager.is_authenticated():
            return False
        
        login_time = st.session_state.get('login_time')
        if login_time:
            elapsed = (datetime.now() - login_time).seconds
            if elapsed > timeout_seconds:
                SessionManager.logout()
                return True
        return False
