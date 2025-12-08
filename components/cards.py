"""Reusable card components for dashboards."""
import streamlit as st

def stat_card(title: str, value: str, icon: str = "📊", color: str = "#0066CC"):
    """
    Create a statistics card with gradient background.
    
    Args:
        title: Card title/label
        value: Main value to display
        icon: Emoji icon
        color: Primary color for gradient
    """
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}, {color}DD);
            color: white;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <div style="font-size: 32px; margin-bottom: 8px; line-height: 1;">{icon}</div>
            <div style="font-size: 36px; font-weight: 700; margin: 8px 0; line-height: 1;">{value}</div>
            <div style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
                {title}
            </div>
        </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, card_type: str = "primary"):
    """
    Create an information card with colored left border.
    
    Args:
        title: Card title
        content: Card content
        card_type: Type of card (primary, success, warning, error)
    """
    colors = {
        "primary": "#0066CC",
        "success": "#06D6A0",
        "warning": "#FFB703",
        "error": "#EF476F"
    }
    
    border_color = colors.get(card_type, colors["primary"])
    
    st.markdown(f"""
        <div style="
            background-color: white;
            border-left: 4px solid {border_color};
            border-radius: 8px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        ">
            <h3 style="margin: 0 0 12px 0; color: #2B2D42; font-size: 18px;">{title}</h3>
            <p style="margin: 0; color: #6B7280; font-size: 14px; line-height: 1.6;">{content}</p>
        </div>
    """, unsafe_allow_html=True)


def appointment_card(appointment: dict):
    """
    Create an appointment card with details.
    
    Args:
        appointment: Dictionary with appointment details
    """
    status_colors = {
        "Confirmed": "#06D6A0",
        "Pending": "#FFB703",
        "Cancelled": "#EF476F",
        "Completed": "#0066CC"
    }
    
    status = appointment.get("status", "Pending")
    status_color = status_colors.get(status, "#6B7280")
    
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-top: 3px solid {status_color};
        ">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #2B2D42; font-size: 18px;">
                    {appointment.get('type', 'Appointment')}
                </h3>
                <span style="
                    background-color: {status_color}20;
                    color: {status_color};
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                ">
                    {status}
                </span>
            </div>
            <div style="color: #6B7280; font-size: 14px; line-height: 1.8;">
                <p style="margin: 4px 0;">
                    • <strong>Date:</strong> {appointment.get('date', 'N/A')} at {appointment.get('time', 'N/A')}
                </p>
                <p style="margin: 4px 0;">
                    • <strong>Patient:</strong> {appointment.get('patient_name', 'N/A')}
                </p>
                <p style="margin: 4px 0;">
                    • <strong>Doctor:</strong> {appointment.get('doctor_name', 'N/A')}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def medical_record_card(record: dict):
    """
    Create a medical record card.
    
    Args:
        record: Dictionary with medical record details
    """
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #0066CC;
        ">
            <div style="margin-bottom: 12px;">
                <h3 style="margin: 0; color: #2B2D42; font-size: 18px;">
                    {record.get('diagnosis', 'Medical Record')}
                </h3>
                <p style="margin: 4px 0 0 0; color: #6B7280; font-size: 12px;">
                    {record.get('date', 'N/A')}
                </p>
            </div>
            <div style="color: #6B7280; font-size: 14px; line-height: 1.8;">
                <p style="margin: 8px 0;">
                    <strong>Doctor:</strong> {record.get('doctor', 'N/A')}
                </p>
                <p style="margin: 8px 0;">
                    <strong>Notes:</strong> {record.get('notes', 'No notes available')}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def prescription_card(prescription: dict):
    """
    Create a prescription card.
    
    Args:
        prescription: Dictionary with prescription details
    """
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-left: 3px solid #00A896;
        ">
            <strong style="color: #2B2D42; font-size: 18px;">{prescription.get('medication', 'N/A')}</strong><br>
            <span style="color: #6B7280; font-size: 15px; line-height: 1.8;">
                • {prescription.get('dosage', 'N/A')}<br>
                • Refills: {prescription.get('refills', 0)} remaining<br>
                • Prescribed by: {prescription.get('prescribed_by', 'N/A')}
            </span>
        </div>
    """, unsafe_allow_html=True)


def message_card(message: dict):
    """
    Create a message card.
    
    Args:
        message: Dictionary with message details
    """
    read_style = "" if message.get('read', False) else "background-color: #F0F9FF;"
    
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            {read_style}
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <strong style="color: #2B2D42;">{message.get('subject', 'No Subject')}</strong>
                <span style="color: #6B7280; font-size: 12px;">{message.get('date', 'N/A')}</span>
            </div>
            <p style="color: #6B7280; font-size: 14px; margin: 4px 0;">
                From: {message.get('from', 'Unknown')}
            </p>
            <p style="color: #2B2D42; font-size: 14px; margin: 8px 0;">
                {message.get('message', 'No message content')}
            </p>
        </div>
    """, unsafe_allow_html=True)
