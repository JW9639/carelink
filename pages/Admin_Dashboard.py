"""Admin Dashboard - System management, user management, analytics."""
import streamlit as st
from services.session_manager import SessionManager
from database.mock_data import MOCK_STATS, MOCK_PATIENTS
from components.cards import stat_card
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.sidebar import admin_sidebar

# Page config
st.set_page_config(
    page_title="Admin Dashboard",
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
        with open("styles/dashboard.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Initialize session and check authentication
SessionManager.init_session()
SessionManager.require_auth(allowed_roles=["admin"])

# Header
st.title("Admin Dashboard")
st.markdown(f"### System Management Portal")
st.caption(f"Logged in as: {st.session_state.user_name}")

# Sidebar Navigation
admin_sidebar()

st.markdown("---")

# Statistics Cards
st.markdown("### System Overview")
stats = MOCK_STATS["admin"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    stat_card("Total Patients", str(stats["total_patients"]), "👥", "#0066CC")
with col2:
    stat_card("Total Doctors", str(stats["total_doctors"]), "⚕️", "#00A896")
with col3:
    stat_card("Today's Appointments", str(stats["today_appointments"]), "📅", "#FFB703")
with col4:
    stat_card("Pending Approvals", str(stats["pending_approvals"]), "⏰", "#EF476F")

st.markdown("---")

# Main Content - Simplified Tabs (Miller's 7±2)
tab1, tab2, tab3 = st.tabs(["Analytics", "Users", "System"])

with tab1:
    st.markdown("### Key Metrics")
    
    # Single row of charts - Most important metrics only
    col1, col2 = st.columns(2)
    
    with col1:
        # Appointments trend
        appointment_data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "Appointments": [75, 85, 90, 80, 95]
        })
        
        fig1 = px.line(
            appointment_data, 
            x="Day", 
            y="Appointments", 
            title="Appointments This Week",
            markers=True
        )
        fig1.update_traces(line_color='#0066CC', line_width=3)
        fig1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif"),
            height=300
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Patient satisfaction gauge
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=98,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Patient Satisfaction"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#06D6A0"},
                'steps': [
                    {'range': [0, 70], 'color': "#FEE2E2"},
                    {'range': [70, 85], 'color': "#FEF3C7"},
                    {'range': [85, 100], 'color': "#D1FAE5"}
                ]
            }
        ))
        fig2.update_layout(
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif"),
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Department Overview - Top 5 only
    st.markdown("### Top Departments")
    dept_data = pd.DataFrame({
        "Department": ["General Medicine", "Pediatrics", "Cardiology", "Orthopedics", "Neurology"],
        "Patients": [520, 380, 245, 180, 125],
        "Today": [24, 25, 18, 12, 8]
    })
    st.dataframe(dept_data, use_container_width=True, hide_index=True)
    
    if st.button("View Full Analytics", use_container_width=True):
        st.info("Full analytics dashboard coming soon!")

with tab2:
    st.markdown("### User Management")
    
    # Quick add user - Simplified
    st.markdown("#### Quick Add User")
    col1, col2, col3 = st.columns(3)
    with col1:
        new_user_name = st.text_input("Full Name")
    with col2:
        new_user_email = st.text_input("Email")
    with col3:
        new_user_role = st.selectbox("Role", ["Patient", "Doctor", "Admin"])
    
    if st.button("Create User", type="primary", use_container_width=True):
        if new_user_name and new_user_email:
            st.success(f"User '{new_user_name}' created successfully! (Mock)")
        else:
            st.warning("Please fill in required fields")
    
    st.markdown("---")
    
    # Recent users only - Top 6
    st.markdown("#### Recent Users")
    
    users_data = pd.DataFrame({
        "Name": ["John Smith", "Dr. Sarah Johnson", "Jane Doe", "Admin User", "Dr. Michael Chen", "Mary Williams"],
        "Role": ["Patient", "Doctor", "Patient", "Admin", "Doctor", "Patient"],
        "Status": ["Active", "Active", "Active", "Active", "Active", "Active"],
        "Last Login": ["2025-12-08", "2025-12-08", "2025-12-07", "2025-12-08", "2025-12-08", "2025-12-06"]
    })
    
    st.dataframe(users_data, use_container_width=True, hide_index=True)
    
    if st.button("View All Users", use_container_width=True):
        st.info("Full user management page coming soon!")

with tab3:
    st.markdown("### System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #06D6A0; margin: 0; font-size: 24px;">System Online</h3>
                <p style="color: #6B7280; margin: 12px 0 0 0; font-size: 16px;">Uptime: 99.9%</p>
                <p style="color: #6B7280; margin: 4px 0 0 0; font-size: 14px;">Last restart: 30 days ago</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #0066CC; margin: 0; font-size: 24px;">Database</h3>
                <p style="color: #6B7280; margin: 12px 0 0 0; font-size: 16px;">Healthy - 2.4GB used</p>
                <p style="color: #6B7280; margin: 4px 0 0 0; font-size: 14px;">Last backup: 2 hours ago</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
with tab3:
    st.markdown("### System Overview")
    
    # System health - 3 key indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #06D6A0; margin: 0; font-size: 24px;">Online</h3>
                <p style="color: #6B7280; margin: 12px 0 0 0; font-size: 14px;">Uptime: 99.9%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #0066CC; margin: 0; font-size: 24px;">Database</h3>
                <p style="color: #6B7280; margin: 12px 0 0 0; font-size: 14px;">2.4GB / Healthy</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #00A896; margin: 0; font-size: 24px;">Secure</h3>
                <p style="color: #6B7280; margin: 12px 0 0 0; font-size: 14px;">No threats</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key metrics only
    st.markdown("#### Current Activity")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Active Users", "234")
    with col_m2:
        st.metric("CPU", "45%")
    with col_m3:
        st.metric("Memory", "6.2GB")
    with col_m4:
        st.metric("Requests/min", "1,250")
    
    st.markdown("---")
    
    # Recent activity - Top 5 only
    st.markdown("#### Recent Activity")
    activity_data = pd.DataFrame({
        "Time": ["10:45 AM", "10:30 AM", "10:15 AM", "10:00 AM", "9:45 AM"],
        "User": ["Dr. Johnson", "Admin", "John Smith", "System", "Dr. Chen"],
        "Action": ["Updated patient record", "Created new user", "Booked appointment", "Backup completed", "Signed prescription"],
        "Status": ["✅", "✅", "✅", "✅", "✅"]
    })
    st.dataframe(activity_data, use_container_width=True, hide_index=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("View Full Logs", use_container_width=True):
            st.info("Full audit log coming soon!")
    with col_btn2:
        if st.button("System Settings", use_container_width=True):
            st.info("Settings page coming soon!")