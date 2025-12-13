"""Sidebar navigation components for different user roles."""
import streamlit as st
from Services.session_manager import SessionManager


def load_sidebar_css():
    """Load sidebar-specific CSS styles."""
    try:
        with open("Styles/sidebar.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_sidebar_toggle():
    """Inject the custom floating button used to open/close the sidebar."""
    st.markdown(
        """
        <div class="cl-sidebar-toggle">
            <button id="clSidebarToggleBtn" class="cl-sidebar-toggle__btn" type="button" aria-label="Toggle sidebar">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
        <div class="cl-sidebar-overlay" id="clSidebarOverlay"></div>
        <script>
        (function() {
            const body = document.body;
            const toggleBtn = document.getElementById("clSidebarToggleBtn");
            const overlay = document.getElementById("clSidebarOverlay");
            if (!toggleBtn || toggleBtn.dataset.bound === "true") {
                return;
            }
            toggleBtn.dataset.bound = "true";
            const saved = window.localStorage.getItem("clSidebarOpen") === "true";
            if (saved) {
                body.classList.add("sidebar-open");
            }
            const setState = (open) => {
                if (open) {
                    body.classList.add("sidebar-open");
                } else {
                    body.classList.remove("sidebar-open");
                }
                window.localStorage.setItem("clSidebarOpen", open);
            };
            toggleBtn.addEventListener("click", (event) => {
                event.preventDefault();
                const open = !body.classList.contains("sidebar-open");
                setState(open);
            });
            if (overlay) {
                overlay.addEventListener("click", () => setState(false));
            }
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def patient_sidebar():
    """Display patient portal sidebar navigation."""
    load_sidebar_css()
    render_sidebar_toggle()
    with st.sidebar:
        st.markdown("### Patient Portal")
        st.info(f"**{st.session_state.user_name}**")
        st.caption("Patient Account")
        
        st.markdown("---")
        st.markdown("### Quick Links")
        
        st.page_link("Pages/Patient/Patient_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("Pages/Patient/Patient_Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("Pages/Patient/Patient_Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("Pages/Patient/Patient_Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("Pages/Patient/Patient_Profile.py", label="• Profile", use_container_width=True)
        
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
    
    load_sidebar_css()
    render_sidebar_toggle()
    with st.sidebar:
        st.markdown("### Doctor Portal")
        st.info(f"**{st.session_state.user_name}**")
        st.caption(f"{specialty}")
        
        st.markdown("---")
        st.markdown("### Quick Links")
        
        st.page_link("Pages/Doctor/Doctor_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("Pages/Doctor/Doctor_Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("Pages/Doctor/Doctor_Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("Pages/Doctor/Doctor_Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("Pages/Doctor/Doctor_Profile.py", label="• Profile", use_container_width=True)
        
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
    load_sidebar_css()
    render_sidebar_toggle()
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
        st.markdown("---")
        st.markdown("### Management")
        
        st.page_link("Pages/Admin/Admin_Dashboard.py", label="• Dashboard", use_container_width=True)
