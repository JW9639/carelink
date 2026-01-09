"""Doctor dashboard."""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from html import escape

import streamlit as st
from sqlalchemy import func

from app.db.repositories.appointment_repository import AppointmentRepository
from app.db.repositories.doctor_repository import DoctorRepository
from app.db.repositories.patient_repository import PatientRepository
from app.db.session import SessionLocal
from app.models.bloodwork import Bloodwork
from app.models.patient import Patient
from app.ui.components.page_header import render_page_header
from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.utils.constants import AppointmentStatus


def _format_time(value: datetime) -> str:
    if value.tzinfo:
        return value.astimezone().strftime("%H:%M")
    return value.strftime("%H:%M")


def _format_date(value: datetime) -> str:
    if value.tzinfo:
        return value.astimezone().strftime("%a, %b %d, %Y")
    return value.strftime("%a, %b %d, %Y")


def _patient_name(patient: Patient | None) -> str:
    if not patient:
        return "Unknown patient"
    return f"{patient.first_name} {patient.last_name}".strip()


if not apply_dashboard_layout("Doctor Dashboard", ["doctor"]):
    st.stop()

user_id = st.session_state.get("user_id")
doctor_name = st.session_state.get("user_name", "Doctor")
appointments_today: list = []
upcoming_appointments: list = []
patients: list[Patient] = []
pending_reviews = 0
unread_messages = 0

db = SessionLocal()
try:
    doctor_repo = DoctorRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_repo = PatientRepository(db)

    doctor = doctor_repo.get_by_user_id(user_id) if user_id else None
    if doctor:
        doctor_name = f"{doctor.first_name} {doctor.last_name}".strip() or doctor_name
        patients = patient_repo.get_by_doctor_id(doctor.id)

        today = date.today()
        start_of_day = datetime.combine(today, time.min).replace(
            tzinfo=timezone.utc
        )
        end_of_day = datetime.combine(today, time.max).replace(tzinfo=timezone.utc)

        appointments_today = appointment_repo.get_doctor_appointments(
            doctor.id, start_of_day, end_of_day
        )
        appointments_today = [
            appointment
            for appointment in appointments_today
            if appointment.status
            in {AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED}
        ]

        upcoming_appointments = appointment_repo.get_doctor_appointments(
            doctor.id, datetime.now(timezone.utc)
        )
        upcoming_appointments = [
            appointment
            for appointment in upcoming_appointments
            if appointment.status
            in {AppointmentStatus.PENDING, AppointmentStatus.SCHEDULED}
        ]

        pending_reviews = (
            db.query(func.count(Bloodwork.id))
            .join(Patient, Patient.id == Bloodwork.patient_id)
            .filter(
                Patient.doctor_id == doctor.id,
                Bloodwork.is_published.is_(False),
            )
            .scalar()
            or 0
        )
finally:
    db.close()

appointments_count = len(upcoming_appointments)
patients_count = len(patients)
priority_tasks = len(appointments_today) + pending_reviews

render_page_header(
    f"Welcome back, Dr. {doctor_name}!",
    "Here is a snapshot of today's workload.",
)

st.markdown("## Today at a Glance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-content">
                <div class="stat-number">{appointments_count}</div>
                <div class="stat-label">Appointments</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-content">
                <div class="stat-number">{unread_messages}</div>
                <div class="stat-label">Messages</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-content">
                <div class="stat-number">{patients_count}</div>
                <div class="stat-label">Patients</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-content">
                <div class="stat-number">{priority_tasks}</div>
                <div class="stat-label">Tasks</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Upcoming Schedule")
    if upcoming_appointments:
        schedule_rows = []
        for appointment in upcoming_appointments[:6]:
            patient_name = escape(_patient_name(appointment.patient))
            schedule_rows.append(
                f"<div class='schedule-row'>"
                f"<p><strong>{_format_date(appointment.scheduled_datetime)}</strong> "
                f"- {_format_time(appointment.scheduled_datetime)} - {patient_name}</p>"
                f"</div>"
            )
        schedule_html = "".join(schedule_rows)
    else:
        schedule_html = "<p>No upcoming appointments scheduled.</p>"

    st.markdown(
        f"""
        <div class="card">
            <style>
                .schedule-row p {{
                    margin: 0;
                }}
                .schedule-row {{
                    padding: 10px 0;
                    border-bottom: 1px solid #e2e8f0;
                }}
                .schedule-row:last-child {{
                    border-bottom: 0;
                }}
            </style>
            {schedule_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("### Quick Actions")
    action_cols = st.columns(2)
    with action_cols[0]:
        st.button("Prescribe", use_container_width=True)
        st.button("Patient Chart", use_container_width=True)
    with action_cols[1]:
        st.button("Order Lab", use_container_width=True)
