"""Sidebar navigation components for different user roles."""
import streamlit as st
from services.session_manager import SessionManager


def load_sidebar_css():
    """Load sidebar-specific CSS styles."""
    try:
        with open("styles/sidebar.css") as f:
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
            // Prevent multiple initializations
            if (window.clSidebarInitialized) {
                return;
            }
            
            // Wait for Streamlit to fully load
            const initToggle = () => {
                const body = document.body;
                const toggleBtn = document.getElementById("clSidebarToggleBtn");
                const overlay = document.getElementById("clSidebarOverlay");
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                
                if (!toggleBtn || !sidebar) {
                    setTimeout(initToggle, 50);
                    return;
                }
                
                // Mark as initialized
                window.clSidebarInitialized = true;
                
                // Add class to body to indicate sidebar toggle is present
                body.classList.add("has-sidebar-toggle");
                
                // Start with sidebar closed (do NOT check localStorage on first load)
                body.classList.remove("sidebar-open");
                
                const setState = (open) => {
                    console.log("Setting sidebar state:", open);
                    if (open) {
                        body.classList.add("sidebar-open");
                    } else {
                        body.classList.remove("sidebar-open");
                    }
                    window.localStorage.setItem("clSidebarOpen", open);
                };
                
                // Button click handler
                toggleBtn.addEventListener("click", (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    const isOpen = body.classList.contains("sidebar-open");
                    console.log("Toggle clicked. Current state:", isOpen, "-> Setting to:", !isOpen);
                    setState(!isOpen);
                });
                
                // Overlay click handler
                if (overlay) {
                    overlay.addEventListener("click", () => {
                        console.log("Overlay clicked, closing sidebar");
                        setState(false);
                    });
                }
                
                console.log("Sidebar toggle initialized successfully");
            };
            
            // Initialize
            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", initToggle);
            } else {
                initToggle();
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
        
        st.page_link("pages/Patient_Patient_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Patient_Patient_Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("pages/Patient_Patient_Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("pages/Patient_Patient_Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("pages/Patient_Patient_Profile.py", label="• Profile", use_container_width=True)
        
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
        
        st.page_link("pages/Doctor_Doctor_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Doctor_Doctor_Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("pages/Doctor_Doctor_Prescriptions.py", label="• Prescriptions", use_container_width=True)
        st.page_link("pages/Doctor_Doctor_Lab_Results.py", label="• Lab Results", use_container_width=True)
        st.page_link("pages/Doctor_Doctor_Profile.py", label="• Profile", use_container_width=True)
        
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
        
        st.page_link("pages/Admin_Admin_Dashboard.py", label="• Dashboard", use_container_width=True)
        st.page_link("pages/Admin_Admin_Appointments.py", label="• Appointments", use_container_width=True)
        st.page_link("pages/Admin_Admin_Profile.py", label="• Profile", use_container_width=True)
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, type="primary"):
            SessionManager.logout()
            st.switch_page("Home.py")
        
        st.markdown("---")
        st.markdown("### System Status")
        st.success("✓ All systems operational")
        st.caption("Last backup: Today 2:00 AM")
