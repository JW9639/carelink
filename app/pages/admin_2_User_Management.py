"""User Management page."""

from __future__ import annotations

import streamlit as st

from app.db.repositories.doctor_repository import DoctorRepository
from app.db.session import SessionLocal
from app.services.doctor_message_service import DoctorMessageService
from app.ui.components.page_header import render_page_header
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


def _doctor_label(doctor) -> str:
    name = f"{doctor.first_name} {doctor.last_name}".strip()
    specialty = doctor.specialty or "General"
    return f"Dr. {name} ({specialty})"


if not apply_dashboard_layout("User Management", ["admin"]):
    st.stop()

render_page_header("User Management", "Create, update, and manage user accounts.")
st.markdown("---")

st.markdown("### Send Message to Doctor")

db = SessionLocal()
try:
    doctor_repo = DoctorRepository(db)
    doctors = doctor_repo.get_all()
finally:
    db.close()

if not doctors:
    st.info("No doctors are available to message yet.")
else:
    with st.form("send_doctor_message"):
        selected_doctor = st.selectbox("Doctor", doctors, format_func=_doctor_label)
        title = st.text_input("Subject")
        body = st.text_area("Message")
        submitted = st.form_submit_button("Send Message")

    if submitted:
        if not title.strip() or not body.strip():
            st.error("Please enter both a subject and message.")
        else:
            db = SessionLocal()
            try:
                DoctorMessageService(db).send_message(
                    doctor_id=selected_doctor.id,
                    title=title.strip(),
                    message=body.strip(),
                    sent_by=st.session_state.get("user_id"),
                )
            finally:
                db.close()
            st.success("Message sent to the doctor.")
