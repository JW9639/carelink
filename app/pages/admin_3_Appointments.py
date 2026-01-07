"""Admin Appointments page - Manage and assign doctors to appointments."""

from __future__ import annotations

from html import escape

import streamlit as st

from app.db.session import SessionLocal
from app.db.repositories.doctor_repository import DoctorRepository
from app.services.appointment_service import AppointmentService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Appointments", ["admin"]):
    st.stop()

# Initialize session state
if "assignment_success" not in st.session_state:
    st.session_state.assignment_success = False

# Database session
db = SessionLocal()
try:
    appointment_service = AppointmentService(db)
    doctor_repo = DoctorRepository(db)

    # Get all doctors for assignment
    all_doctors = doctor_repo.get_all_approved()
    doctor_options = {
        f"Dr. {d.first_name} {d.last_name} ({d.specialty})": d.id for d in all_doctors
    }

    # Page header
    st.markdown("### Appointment Management")
    st.markdown("Review pending appointments and assign doctors.")
    st.markdown("---")

    # Show success message
    if st.session_state.assignment_success:
        st.success("Doctor assigned successfully! The appointment is now confirmed.")
        st.session_state.assignment_success = False

    # Tabs for different views
    tab1, tab2 = st.tabs(["Pending Appointments", "All Appointments"])

    with tab1:
        # Get pending appointments
        pending_appointments = appointment_service.get_pending_appointments()

        if not pending_appointments:
            st.info("No pending appointments at this time.")
        else:
            st.markdown(
                f"**{len(pending_appointments)} appointment(s) awaiting doctor assignment**"
            )
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            if not doctor_options:
                st.warning("No approved doctors available for assignment.")

            for appt in pending_appointments:
                appt_date = appt.scheduled_datetime.strftime("%A, %B %d, %Y")
                appt_time = appt.scheduled_datetime.strftime("%I:%M %p")
                patient_name = (
                    f"{appt.patient.first_name} {appt.patient.last_name}"
                    if appt.patient
                    else "Unknown"
                )
                patient_name = escape(patient_name)
                reason = escape(appt.reason) if appt.reason else "No reason provided"

                with st.container():
                    st.markdown(
                        f"""
                    <div style="
                        background: white;
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 16px;
                        border-left: 4px solid #f59e0b;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <div>
                                <div style="font-weight: 700; color: #1e293b; font-size: 16px;">{patient_name}</div>
                                <div style="color: #64748b; font-size: 14px; margin-top: 4px;">
                                    {appt_date} at {appt_time} - {appt.duration_minutes} min
                                </div>
                            </div>
                            <div style="
                                background: #fef3c7;
                                color: #d97706;
                                padding: 4px 12px;
                                border-radius: 20px;
                                font-size: 12px;
                                font-weight: 600;
                            ">Pending</div>
                        </div>
                        <div style="
                            background: #f8fafc;
                            border-radius: 8px;
                            padding: 12px;
                            margin-top: 12px;
                        ">
                            <div style="color: #64748b; font-size: 12px; font-weight: 600; margin-bottom: 4px;">REASON FOR VISIT</div>
                            <div style="color: #1e293b; font-size: 14px;">{reason}</div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    if doctor_options:
                        # Assignment form
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            selected_doctor = st.selectbox(
                                "Assign Doctor",
                                options=list(doctor_options.keys()),
                                key=f"doctor_select_{appt.id}",
                                label_visibility="collapsed",
                                placeholder="Select a doctor...",
                            )
                        with col2:
                            if st.button(
                                "Assign",
                                key=f"assign_{appt.id}",
                                type="primary",
                                use_container_width=True,
                            ):
                                if selected_doctor:
                                    doctor_id = doctor_options[selected_doctor]
                                    try:
                                        appointment_service.assign_doctor_to_appointment(
                                            appt.id,
                                            doctor_id,
                                            assigned_by_user_id=st.session_state.get(
                                                "user_id"
                                            ),
                                        )
                                    except ValueError as exc:
                                        st.error(str(exc))
                                    else:
                                        st.session_state.assignment_success = True
                                        st.rerun()
                                else:
                                    st.error("Please select a doctor.")

                    st.markdown(
                        "<div style='height: 8px;'></div>", unsafe_allow_html=True
                    )

    with tab2:
        st.markdown("**All Scheduled Appointments**")
        st.info("Full appointment list coming soon...")

finally:
    db.close()
