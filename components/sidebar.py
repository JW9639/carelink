"""Sidebar navigation components for different user roles."""
import streamlit as st
import streamlit.components.v1 as components
from services.session_manager import SessionManager


def load_sidebar_css():
    """Load sidebar-specific CSS styles."""
    try:
        with open("styles/sidebar.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_sidebar_toggle():
    """Inject the custom floating button and toggle logic - no visible space taken."""
    # Put everything in one components.html call - both HTML and JavaScript
    # This creates only ONE iframe container at height=0, so no blank space
    components.html(
        """
        <!-- Inject button and overlay into parent document -->
        <script>
        (function() {
            const parentDoc = window.parent.document;
            const body = parentDoc.body;
            
            // Only inject once
            if (!parentDoc.getElementById("clSidebarToggleBtn")) {
                // Create toggle button
                const toggleDiv = parentDoc.createElement("div");
                toggleDiv.className = "cl-sidebar-toggle";
                toggleDiv.innerHTML = `
                    <button id="clSidebarToggleBtn" class="cl-sidebar-toggle__btn" type="button" aria-label="Toggle sidebar">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                `;
                body.appendChild(toggleDiv);
                
                // Create overlay
                const overlay = parentDoc.createElement("div");
                overlay.className = "cl-sidebar-overlay";
                overlay.id = "clSidebarOverlay";
                body.appendChild(overlay);
            }
            
            // Initialize toggle functionality
            const initToggle = () => {
                const toggleBtn = parentDoc.getElementById("clSidebarToggleBtn");
                const overlay = parentDoc.getElementById("clSidebarOverlay");
                const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
                
                if (!toggleBtn || !sidebar) {
                    setTimeout(initToggle, 100);
                    return;
                }
                
                // Force sidebar to use fixed positioning
                sidebar.style.setProperty("position", "fixed", "important");
                sidebar.style.setProperty("top", "0", "important");
                sidebar.style.setProperty("height", "100vh", "important");
                sidebar.style.setProperty("width", "21rem", "important");
                sidebar.style.setProperty("z-index", "99999", "important");
                sidebar.style.setProperty("transition", "left 0.3s ease", "important");
                sidebar.style.setProperty("transform", "none", "important");
                
                body.classList.add("has-sidebar-toggle");
                
                // Start with sidebar closed
                if (!window.parent.clSidebarInitialized) {
                    body.classList.remove("sidebar-open");
                    sidebar.style.setProperty("left", "-21rem", "important");
                    window.parent.clSidebarInitialized = true;
                }
                
                const setState = (open) => {
                    if (open) {
                        body.classList.add("sidebar-open");
                        sidebar.style.setProperty("left", "0", "important");
                        sidebar.style.setProperty("visibility", "visible", "important");
                        sidebar.style.setProperty("display", "block", "important");
                    } else {
                        body.classList.remove("sidebar-open");
                        sidebar.style.setProperty("left", "-21rem", "important");
                    }
                    try {
                        window.parent.localStorage.setItem("clSidebarOpen", open);
                    } catch(e) {}
                };
                
                // Remove old handler if exists
                if (toggleBtn._clickHandler) {
                    toggleBtn.removeEventListener("click", toggleBtn._clickHandler);
                }
                
                // Button click handler
                const clickHandler = (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    const isOpen = body.classList.contains("sidebar-open");
                    setState(!isOpen);
                };
                
                toggleBtn._clickHandler = clickHandler;
                toggleBtn.addEventListener("click", clickHandler);
                
                // Overlay click handler
                if (overlay) {
                    overlay.addEventListener("click", () => setState(false));
                }
            };
            
            setTimeout(initToggle, 100);
        })();
        </script>
        """,
        height=0,
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
