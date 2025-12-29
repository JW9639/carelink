"""Authentication and login form components."""
import streamlit as st
from services.auth_service import AuthService
from services.session_manager import SessionManager

def login_form():
    """
    Display traditional login form.
    Returns True if login is successful.
    """
    st.markdown("## Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if username and password:
                # TODO: Implement real authentication
                user = AuthService.authenticate(username, password)
                if user:
                    SessionManager.login(
                        user['id'],
                        user['name'],
                        user['role'],
                        user
                    )
                    return True
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    return False


def mock_login_buttons():
    """
    Display mock login buttons for testing.
    """
    st.markdown("### Mock Login (For Testing)")
    st.info("Click one of the buttons below to simulate login as different user roles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Login as Patient", use_container_width=True, type="primary"):
            user = AuthService.mock_login("patient")
            if user:
                SessionManager.login(user['id'], user['name'], user['role'], user)
                st.success(f"Logged in as {user['name']} (Patient)")
                st.balloons()
                st.switch_page("pages/Patient_Patient_Dashboard.py")
    
    with col2:
        if st.button("Login as Doctor", use_container_width=True, type="primary"):
            user = AuthService.mock_login("doctor")
            if user:
                SessionManager.login(user['id'], user['name'], user['role'], user)
                st.success(f"Logged in as {user['name']} (Doctor)")
                st.balloons()
                st.switch_page("pages/Doctor_Doctor_Dashboard.py")
    
    with col3:
        if st.button("Login as Admin", use_container_width=True, type="primary"):
            user = AuthService.mock_login("admin")
            if user:
                SessionManager.login(user['id'], user['name'], user['role'], user)
                st.success(f"Logged in as {user['name']} (Admin)")
                st.balloons()
                st.switch_page("pages/Admin_Admin_Dashboard.py")


def logout_button():
    """Display logout button in sidebar."""
    if st.button("Logout", use_container_width=True):
        SessionManager.logout()
        st.success("Logged out successfully")
        st.rerun()
