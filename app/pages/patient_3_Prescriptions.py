"""Prescriptions page."""

from __future__ import annotations

from html import escape

import streamlit as st

from app.db.session import SessionLocal
from app.services.patient_service import PatientService
from app.services.prescription_service import PrescriptionService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.ui.components.page_header import render_page_header


if not apply_dashboard_layout("Prescriptions", ["patient"]):
    st.stop()

user_id = st.session_state.get("user_id")

db = SessionLocal()
try:
    patient_service = PatientService(db)
    prescription_service = PrescriptionService(db)

    patient = patient_service.get_patient_by_user_id(user_id) if user_id else None
    if not patient:
        st.error("Patient profile not found.")
        st.stop()

    active_prescriptions = prescription_service.get_active_prescriptions(patient.id)
    history_prescriptions = prescription_service.get_prescription_history(patient.id)
finally:
    db.close()

render_page_header(
    "Prescriptions",
    "View your current medications and prescription history.",
)
st.markdown("---")

tab_active, tab_history = st.tabs(["Active", "History"])

with tab_active:
    if not active_prescriptions:
        st.info("You have no active prescriptions.")
    else:
        for rx in active_prescriptions:
            doctor = rx.prescribed_by_doctor
            doctor_name = (
                f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Prescriber"
            )
            notes = escape(rx.notes) if rx.notes else ""
            st.markdown(
                f"""
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 16px;
                    border: 1px solid #e2e8f0;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-size: 18px; font-weight: 700; color: #1e293b;">
                                {escape(rx.medication_name)}
                            </div>
                            <div style="font-size: 16px; color: #64748b; margin-top: 4px;">
                                {escape(rx.dosage)} - {escape(rx.frequency)}
                            </div>
                        </div>
                        <div style="
                            background: rgba(16, 185, 129, 0.12);
                            color: #10b981;
                            padding: 6px 14px;
                            border-radius: 999px;
                            font-size: 14px;
                            font-weight: 700;
                        ">Active</div>
                    </div>
                    <div style="font-size: 16px; color: #475569; margin-top: 12px;">
                        Started {rx.start_date.strftime("%B %d, %Y")} - Prescribed by {escape(doctor_name)}
                    </div>
                    {f'<div style="font-size: 16px; color: #64748b; margin-top: 8px;">Notes: {notes}</div>' if notes else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Request Refill",
                key=f"refill_{rx.id}",
                use_container_width=True,
            ):
                st.info("Refill requests will be available in a future update.")

with tab_history:
    if not history_prescriptions:
        st.info("No prescription history available.")
    else:
        for rx in history_prescriptions:
            doctor = rx.prescribed_by_doctor
            doctor_name = (
                f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Prescriber"
            )
            notes = escape(rx.notes) if rx.notes else ""
            end_date = rx.end_date.strftime("%B %d, %Y") if rx.end_date else "Ended"
            st.markdown(
                f"""
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 16px;
                    border: 1px solid #e2e8f0;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-size: 18px; font-weight: 700; color: #1e293b;">
                                {escape(rx.medication_name)}
                            </div>
                            <div style="font-size: 16px; color: #64748b; margin-top: 4px;">
                                {escape(rx.dosage)} - {escape(rx.frequency)}
                            </div>
                        </div>
                        <div style="
                            background: rgba(148, 163, 184, 0.2);
                            color: #475569;
                            padding: 6px 14px;
                            border-radius: 999px;
                            font-size: 14px;
                            font-weight: 700;
                        ">Inactive</div>
                    </div>
                    <div style="font-size: 16px; color: #475569; margin-top: 12px;">
                        {rx.start_date.strftime("%B %d, %Y")} - {end_date}
                    </div>
                    <div style="font-size: 16px; color: #64748b; margin-top: 6px;">
                        Prescribed by {escape(doctor_name)}
                    </div>
                    {f'<div style="font-size: 16px; color: #64748b; margin-top: 8px;">Notes: {notes}</div>' if notes else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )
