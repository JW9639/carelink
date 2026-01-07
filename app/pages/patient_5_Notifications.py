"""Notifications page."""

from __future__ import annotations

from html import escape

import streamlit as st

from app.db.session import SessionLocal
from app.services.notification_service import NotificationService
from app.services.patient_service import PatientService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.utils.constants import NotificationType


if not apply_dashboard_layout("Notifications", ["patient"]):
    st.stop()

TYPE_LABELS = {
    NotificationType.APPOINTMENT_REMINDER.value: "Appointment",
    NotificationType.RESULTS_READY.value: "Results",
    NotificationType.FOLLOW_UP.value: "Follow Up",
    NotificationType.PRESCRIPTION_UPDATE.value: "Prescription",
    NotificationType.GENERAL.value: "General",
}


def _type_label(raw_type: str) -> str:
    return TYPE_LABELS.get(raw_type, "General")


user_id = st.session_state.get("user_id")

db = SessionLocal()
try:
    patient_service = PatientService(db)
    notification_service = NotificationService(db)

    patient = patient_service.get_patient_by_user_id(user_id) if user_id else None
    if not patient:
        st.error("Patient profile not found.")
        st.stop()

    notifications = notification_service.get_notifications(patient.id)
finally:
    db.close()

st.markdown("## Notifications")
st.markdown("Stay up to date with messages from your care team.")
st.markdown("---")

unread_notifications = [n for n in notifications if not n.is_read]

tab_all, tab_unread = st.tabs(["All", "Unread"])

with tab_all:
    if unread_notifications:
        if st.button("Mark All as Read", use_container_width=True):
            db = SessionLocal()
            try:
                NotificationService(db).mark_all_as_read(patient.id)
            finally:
                db.close()
            st.rerun()

    if not notifications:
        st.info("You have no notifications.")
    else:
        for notification in notifications:
            raw_type = (
                notification.type.value
                if hasattr(notification.type, "value")
                else str(notification.type)
            )
            label = _type_label(raw_type)
            title = escape(notification.title)
            message = escape(notification.message)
            created_at = notification.created_at.strftime("%B %d, %Y")
            is_unread = not notification.is_read

            st.markdown(
                f"""
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 16px;
                    border: 1px solid {'#93c5fd' if is_unread else '#e2e8f0'};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-size: 14px; text-transform: uppercase; color: #64748b; font-weight: 600;">
                                {label}
                            </div>
                            <div style="font-size: 18px; font-weight: 700; color: #1e293b; margin-top: 6px;">
                                {title}
                            </div>
                            <div style="font-size: 16px; color: #475569; margin-top: 8px;">
                                {message}
                            </div>
                            <div style="font-size: 14px; color: #94a3b8; margin-top: 10px;">
                                {created_at}
                            </div>
                        </div>
                        <div style="
                            background: {'rgba(59, 130, 246, 0.12)' if is_unread else 'rgba(148, 163, 184, 0.2)'};
                            color: {'#2563eb' if is_unread else '#475569'};
                            padding: 6px 12px;
                            border-radius: 999px;
                            font-size: 14px;
                            font-weight: 700;
                        ">{'Unread' if is_unread else 'Read'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if is_unread:
                if st.button(
                    "Mark as Read",
                    key=f"mark_read_{notification.id}",
                    use_container_width=True,
                ):
                    db = SessionLocal()
                    try:
                        NotificationService(db).mark_as_read(notification.id)
                    finally:
                        db.close()
                    st.rerun()

with tab_unread:
    if not unread_notifications:
        st.info("No unread notifications.")
    else:
        for notification in unread_notifications:
            raw_type = (
                notification.type.value
                if hasattr(notification.type, "value")
                else str(notification.type)
            )
            label = _type_label(raw_type)
            title = escape(notification.title)
            message = escape(notification.message)
            created_at = notification.created_at.strftime("%B %d, %Y")

            st.markdown(
                f"""
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 16px;
                    border: 1px solid #93c5fd;
                ">
                    <div style="font-size: 14px; text-transform: uppercase; color: #64748b; font-weight: 600;">
                        {label}
                    </div>
                    <div style="font-size: 18px; font-weight: 700; color: #1e293b; margin-top: 6px;">
                        {title}
                    </div>
                    <div style="font-size: 16px; color: #475569; margin-top: 8px;">
                        {message}
                    </div>
                    <div style="font-size: 14px; color: #94a3b8; margin-top: 10px;">
                        {created_at}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Mark as Read",
                key=f"mark_read_unread_{notification.id}",
                use_container_width=True,
            ):
                db = SessionLocal()
                try:
                    NotificationService(db).mark_as_read(notification.id)
                finally:
                    db.close()
                st.rerun()
