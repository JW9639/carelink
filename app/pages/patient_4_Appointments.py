"""Patient Appointments page - Book and view appointments with tabbed interface."""

from __future__ import annotations

import calendar
import math
from datetime import datetime, date, timezone

import streamlit as st

from app.db.session import SessionLocal
from app.services.appointment_service import AppointmentService
from app.services.patient_service import PatientService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.utils.constants import AppointmentStatus


if not apply_dashboard_layout("Appointments", ["patient"]):
    st.stop()

# Initialize session state for booking flow
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None
if "selected_time" not in st.session_state:
    st.session_state.selected_time = None
if "selected_duration" not in st.session_state:
    st.session_state.selected_duration = 30
if "show_booking_modal" not in st.session_state:
    st.session_state.show_booking_modal = False
if "booking_success" not in st.session_state:
    st.session_state.booking_success = False
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = date.today().month
if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = date.today().year
if "history_page" not in st.session_state:
    st.session_state.history_page = 0
if "upcoming_page" not in st.session_state:
    st.session_state.upcoming_page = 0

# Check for tab navigation from other pages
default_tab_index = 0  # Default to "My Appointments" tab
if "appointments_tab" in st.session_state:
    if st.session_state.appointments_tab == "book":
        default_tab_index = 1
    # Clear after reading to avoid persisting
    del st.session_state.appointments_tab

# Get user info
user_id = st.session_state.get("user_id")

# Initialize database session
db = SessionLocal()
try:
    patient_service = PatientService(db)
    appointment_service = AppointmentService(db)

    patient = patient_service.get_patient_by_user_id(user_id) if user_id else None

    if not patient:
        st.error("Patient profile not found.")
        st.stop()

    # Page header
    st.markdown(
        """
    <h2 style="color: #1e293b; margin-bottom: 8px;">Appointments</h2>
    <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">View your appointments or book a new visit.</p>
    """,
        unsafe_allow_html=True,
    )

    # Show success message if just booked
    if st.session_state.booking_success:
        st.success(
            "Your appointment has been booked successfully! It is now pending review by our staff who will assign a doctor."
        )
        st.session_state.booking_success = False

    # Create tabs
    tab1, tab2 = st.tabs(["My Appointments", "Book Appointment"])

    # ========== TAB 1: MY APPOINTMENTS (History & Upcoming) ==========
    with tab1:
        # Upcoming Appointments Section
        st.markdown(
            "<h4 style='color: #1e293b; font-weight: 600; margin-top: 16px; margin-bottom: 16px;'>Upcoming Appointments</h4>",
            unsafe_allow_html=True,
        )

        # Pagination settings for upcoming
        UPCOMING_PER_PAGE = 3
        total_upcoming = appointment_service.count_patient_upcoming_appointments(
            patient.id
        )
        total_upcoming_pages = max(1, math.ceil(total_upcoming / UPCOMING_PER_PAGE))

        # Ensure current page is valid
        if st.session_state.upcoming_page >= total_upcoming_pages:
            st.session_state.upcoming_page = max(0, total_upcoming_pages - 1)

        # Get paginated upcoming appointments
        upcoming_offset = st.session_state.upcoming_page * UPCOMING_PER_PAGE
        upcoming_appointments = (
            appointment_service.get_patient_upcoming_appointments_paginated(
                patient.id, limit=UPCOMING_PER_PAGE, offset=upcoming_offset
            )
        )

        if upcoming_appointments:
            # Show paginated upcoming appointments
            for appt in upcoming_appointments:
                status_color = (
                    "#f59e0b" if appt.status == AppointmentStatus.PENDING else "#10b981"
                )
                status_text = (
                    "Pending Review"
                    if appt.status == AppointmentStatus.PENDING
                    else "Confirmed"
                )
                doctor_info = (
                    f"Dr. {appt.doctor.last_name}" if appt.doctor else "Doctor TBD"
                )

                appt_date = appt.scheduled_datetime.strftime("%A, %B %d, %Y")
                appt_time = appt.scheduled_datetime.strftime("%I:%M %p")

                st.markdown(
                    f"""
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 16px 20px;
                    margin-bottom: 12px;
                    border-left: 4px solid {status_color};
                    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #1e293b; font-size: 15px;">{appt_date}</div>
                            <div style="color: #64748b; font-size: 14px; margin-top: 4px;">{appt_time} • {appt.duration_minutes} min • {doctor_info}</div>
                            {f'<div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Reason: {appt.reason}</div>' if appt.reason else ''}
                        </div>
                        <div style="
                            background: {status_color}15;
                            color: {status_color};
                            padding: 4px 12px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                        ">{status_text}</div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Pagination controls for upcoming
            if total_upcoming_pages > 1:
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 2, 1])

                with col1:
                    if st.button(
                        "◀ Previous",
                        disabled=st.session_state.upcoming_page == 0,
                        key="prev_upcoming",
                    ):
                        st.session_state.upcoming_page -= 1
                        st.rerun()

                with col2:
                    st.markdown(
                        f"<p style='text-align: center; color: #64748b; margin: 8px 0;'>Page {st.session_state.upcoming_page + 1} of {total_upcoming_pages}</p>",
                        unsafe_allow_html=True,
                    )

                with col3:
                    if st.button(
                        "Next ▶",
                        disabled=st.session_state.upcoming_page
                        >= total_upcoming_pages - 1,
                        key="next_upcoming",
                    ):
                        st.session_state.upcoming_page += 1
                        st.rerun()
        else:
            st.markdown(
                """
            <div style="
                background: #f8fafc;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                border: 1px dashed #e2e8f0;
            ">
                <p style="color: #64748b; font-size: 15px; margin: 0;">No upcoming appointments</p>
                <p style="color: #94a3b8; font-size: 13px; margin-top: 8px;">Use the "Book Appointment" tab to schedule a visit</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
        st.markdown("---")

        # Past Appointments (History) Section
        st.markdown(
            "<h4 style='color: #1e293b; font-weight: 600; margin-top: 16px; margin-bottom: 16px;'>Appointment History</h4>",
            unsafe_allow_html=True,
        )

        # Pagination settings
        ITEMS_PER_PAGE = 3
        total_past = appointment_service.count_patient_past_appointments(patient.id)
        total_pages = max(1, math.ceil(total_past / ITEMS_PER_PAGE))

        # Ensure current page is valid
        if st.session_state.history_page >= total_pages:
            st.session_state.history_page = max(0, total_pages - 1)

        # Get paginated past appointments
        offset = st.session_state.history_page * ITEMS_PER_PAGE
        past_appointments = appointment_service.get_patient_past_appointments(
            patient.id, limit=ITEMS_PER_PAGE, offset=offset
        )

        if past_appointments:
            for appt in past_appointments:
                # Determine status styling
                if appt.status == AppointmentStatus.COMPLETED:
                    status_color = "#10b981"
                    status_text = "Completed"
                elif appt.status == AppointmentStatus.CANCELLED:
                    status_color = "#ef4444"
                    status_text = "Cancelled"
                elif appt.status == AppointmentStatus.NO_SHOW:
                    status_color = "#6b7280"
                    status_text = "No Show"
                else:
                    status_color = "#64748b"
                    status_text = "Past"

                doctor_info = f"Dr. {appt.doctor.last_name}" if appt.doctor else "N/A"
                appt_date = appt.scheduled_datetime.strftime("%A, %B %d, %Y")
                appt_time = appt.scheduled_datetime.strftime("%I:%M %p")

                st.markdown(
                    f"""
                <div style="
                    background: #f8fafc;
                    border-radius: 12px;
                    padding: 16px 20px;
                    margin-bottom: 12px;
                    border-left: 4px solid {status_color};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #475569; font-size: 15px;">{appt_date}</div>
                            <div style="color: #64748b; font-size: 14px; margin-top: 4px;">{appt_time} • {appt.duration_minutes} min • {doctor_info}</div>
                            {f'<div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Reason: {appt.reason}</div>' if appt.reason else ''}
                        </div>
                        <div style="
                            background: {status_color}15;
                            color: {status_color};
                            padding: 4px 12px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 600;
                        ">{status_text}</div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Pagination controls
            if total_pages > 1:
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 2, 1])

                with col1:
                    if st.button(
                        "◀ Previous",
                        disabled=st.session_state.history_page == 0,
                        key="prev_history",
                    ):
                        st.session_state.history_page -= 1
                        st.rerun()

                with col2:
                    st.markdown(
                        f"<p style='text-align: center; color: #64748b; margin: 8px 0;'>Page {st.session_state.history_page + 1} of {total_pages}</p>",
                        unsafe_allow_html=True,
                    )

                with col3:
                    if st.button(
                        "Next ▶",
                        disabled=st.session_state.history_page >= total_pages - 1,
                        key="next_history",
                    ):
                        st.session_state.history_page += 1
                        st.rerun()
        else:
            st.markdown(
                """
            <div style="
                background: #f8fafc;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                border: 1px dashed #e2e8f0;
            ">
                <p style="color: #64748b; font-size: 15px; margin: 0;">No appointment history yet</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ========== TAB 2: BOOK APPOINTMENT ==========
    with tab2:
        # Professional styling - target parent containers using :has() selector
        st.markdown(
            """
            <style>
            /* Calendar section card */
            [data-testid="stColumn"]:has(.calendar-marker) {
                background: white !important;
                border-radius: 12px !important;
                padding: 24px !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
                border: 1px solid #e5e7eb !important;
            }
            .calendar-marker { display: none; }
            .time-marker { display: none; }
            .confirm-marker { display: none; }

            /* Time section card */
            [data-testid="stVerticalBlock"]:has(.time-marker) > div {
                background: white;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border: 1px solid #e5e7eb;
                margin-top: 16px;
            }

            /* Confirm section card */
            [data-testid="stColumn"]:has(.confirm-marker) {
                background: white !important;
                border-radius: 12px !important;
                padding: 24px !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
                border: 1px solid #e5e7eb !important;
            }

            .section-label {
                font-size: 13px;
                font-weight: 600;
                color: #6b7280;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            }
            .selected-info {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
            }
            .selected-info-row {
                display: flex;
                justify-content: space-between;
                padding: 4px 0;
                font-size: 14px;
            }
            .selected-info-label {
                color: #6b7280;
            }
            .selected-info-value {
                color: #111827;
                font-weight: 500;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Center the booking interface
        spacer_l, main_col, spacer_r = st.columns([1, 4, 1])

        with main_col:
            # Marker for CSS targeting
            st.markdown('<div class="calendar-marker"></div>', unsafe_allow_html=True)

            # Calendar header
            st.markdown(
                "<h3 style='color: #111827; font-size: 20px; font-weight: 600; margin-bottom: 16px;'>📅 Select a Date</h3>",
                unsafe_allow_html=True,
            )

            # Calendar navigation
            nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

            with nav_col1:
                if st.button("← Prev", key="prev_month", use_container_width=True):
                    if st.session_state.calendar_month == 1:
                        st.session_state.calendar_month = 12
                        st.session_state.calendar_year -= 1
                    else:
                        st.session_state.calendar_month -= 1
                    st.session_state.selected_date = None
                    st.session_state.selected_time = None
                    st.rerun()

            with nav_col2:
                month_name = calendar.month_name[st.session_state.calendar_month]
                st.markdown(
                    f"<p style='text-align: center; font-weight: 700; font-size: 20px; color: #111827; margin: 4px 0;'>{month_name} {st.session_state.calendar_year}</p>",
                    unsafe_allow_html=True,
                )

            with nav_col3:
                if st.button("Next →", key="next_month", use_container_width=True):
                    if st.session_state.calendar_month == 12:
                        st.session_state.calendar_month = 1
                        st.session_state.calendar_year += 1
                    else:
                        st.session_state.calendar_month += 1
                    st.session_state.selected_date = None
                    st.session_state.selected_time = None
                    st.rerun()

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            # Build calendar
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdayscalendar(
                st.session_state.calendar_year, st.session_state.calendar_month
            )
            today = date.today()

            # Day headers
            header_cols = st.columns(7)
            for idx, day_name in enumerate(
                ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            ):
                with header_cols[idx]:
                    st.markdown(
                        f"<div style='text-align:center;font-size:12px;font-weight:600;color:#6b7280;padding:8px 0;border-bottom:1px solid #e5e7eb;'>{day_name}</div>",
                        unsafe_allow_html=True,
                    )

            # Calendar days
            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day == 0:
                            st.markdown(
                                "<div style='height: 38px;'></div>",
                                unsafe_allow_html=True,
                            )
                        else:
                            current_date = date(
                                st.session_state.calendar_year,
                                st.session_state.calendar_month,
                                day,
                            )
                            is_past = current_date < today
                            is_weekend = i == 0 or i == 6
                            is_selected = (
                                st.session_state.selected_date == current_date
                            )

                            if is_selected:
                                st.markdown(
                                    f"<div style='text-align:center;padding:4px 0;'><span style='display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:#111827;color:white;border-radius:50%;font-size:14px;font-weight:500;'>{day}</span></div>",
                                    unsafe_allow_html=True,
                                )
                            elif is_past or is_weekend:
                                st.markdown(
                                    f"<div style='text-align:center;color:#d1d5db;font-size:14px;padding:8px 0;'>{day}</div>",
                                    unsafe_allow_html=True,
                                )
                            else:
                                if st.button(
                                    str(day),
                                    key=f"day_{day}",
                                    use_container_width=True,
                                ):
                                    st.session_state.selected_date = current_date
                                    st.session_state.selected_time = None
                                    st.rerun()

            # Time Selection Card (only show if date selected)
            if st.session_state.selected_date:
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                selected_date_str = st.session_state.selected_date.strftime(
                    "%A, %B %d, %Y"
                )
                st.markdown(
                    "<h3 style='color: #111827; font-size: 20px; font-weight: 600; margin-bottom: 4px;'>🕐 Select a Time</h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='color: #6b7280; font-size: 14px; margin-bottom: 20px;'>{selected_date_str}</p>",
                    unsafe_allow_html=True,
                )

                # Duration selector
                st.markdown(
                    "<p style='font-size:13px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;'>Appointment Duration</p>",
                    unsafe_allow_html=True,
                )
                dur_col1, dur_col2, dur_col3 = st.columns([1, 1, 2])
                with dur_col1:
                    if st.button(
                        "30 min",
                        key="dur_30",
                        type=(
                            "primary"
                            if st.session_state.selected_duration == 30
                            else "secondary"
                        ),
                        use_container_width=True,
                    ):
                        st.session_state.selected_duration = 30
                        st.session_state.selected_time = None
                        st.rerun()
                with dur_col2:
                    if st.button(
                        "60 min",
                        key="dur_60",
                        type=(
                            "primary"
                            if st.session_state.selected_duration == 60
                            else "secondary"
                        ),
                        use_container_width=True,
                    ):
                        st.session_state.selected_duration = 60
                        st.session_state.selected_time = None
                        st.rerun()

                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

                # Get available slots
                am_slots, pm_slots = appointment_service.get_available_slots(
                    st.session_state.selected_date, st.session_state.selected_duration
                )

                # Morning slots
                st.markdown(
                    '<p class="section-label">Morning</p>', unsafe_allow_html=True
                )
                am_cols = st.columns(4)
                for idx, slot in enumerate(am_slots):
                    with am_cols[idx % 4]:
                        is_selected = st.session_state.selected_time == slot.time
                        if slot.is_available:
                            if st.button(
                                slot.display,
                                key=f"am_{slot.time}",
                                type="primary" if is_selected else "secondary",
                                use_container_width=True,
                            ):
                                st.session_state.selected_time = slot.time
                                st.rerun()
                        else:
                            st.markdown(
                                f"<div style='text-align:center;padding:8px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;color:#d1d5db;font-size:13px;text-decoration:line-through;margin-bottom:8px;'>{slot.display}</div>",
                                unsafe_allow_html=True,
                            )

                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                # Afternoon slots
                st.markdown(
                    '<p class="section-label">Afternoon</p>', unsafe_allow_html=True
                )
                pm_cols = st.columns(4)
                for idx, slot in enumerate(pm_slots):
                    with pm_cols[idx % 4]:
                        is_selected = st.session_state.selected_time == slot.time
                        if slot.is_available:
                            if st.button(
                                slot.display,
                                key=f"pm_{slot.time}",
                                type="primary" if is_selected else "secondary",
                                use_container_width=True,
                            ):
                                st.session_state.selected_time = slot.time
                                st.rerun()
                        else:
                            st.markdown(
                                f"<div style='text-align:center;padding:8px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;color:#d1d5db;font-size:13px;text-decoration:line-through;margin-bottom:8px;'>{slot.display}</div>",
                                unsafe_allow_html=True,
                            )

            # Continue button
            if st.session_state.selected_date and st.session_state.selected_time:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                if st.button(
                    "Continue to Confirm →", type="primary", use_container_width=True
                ):
                    st.session_state.show_booking_modal = True
                    st.rerun()

        # Booking Confirmation Form
        if (
            st.session_state.show_booking_modal
            and st.session_state.selected_date
            and st.session_state.selected_time
        ):
            st.markdown("---")

            # Center the form
            spacer_left, form_col, spacer_right = st.columns([1, 3, 1])

            with form_col:
                st.markdown('<div class="confirm-marker"></div>', unsafe_allow_html=True)
                st.markdown(
                    "<h3 style='color: #111827; font-size: 20px; font-weight: 600; margin-bottom: 16px;'>✓ Confirm Your Appointment</h3>",
                    unsafe_allow_html=True,
                )

                # Display selected date/time
                appt_datetime = datetime.combine(
                    st.session_state.selected_date, st.session_state.selected_time
                )
                formatted_date = appt_datetime.strftime("%A, %B %d, %Y")
                formatted_time = appt_datetime.strftime("%I:%M %p")

                st.markdown(
                    f"""
                    <div class="selected-info">
                        <div class="selected-info-row">
                            <span class="selected-info-label">Date</span>
                            <span class="selected-info-value">{formatted_date}</span>
                        </div>
                        <div class="selected-info-row">
                            <span class="selected-info-label">Time</span>
                            <span class="selected-info-value">{formatted_time}</span>
                        </div>
                        <div class="selected-info-row">
                            <span class="selected-info-label">Duration</span>
                            <span class="selected-info-value">{st.session_state.selected_duration} minutes</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Patient info
                patient_name = f"{patient.first_name} {patient.last_name}"
                st.text_input(
                    "Patient Name",
                    value=patient_name,
                    disabled=True,
                    key="confirm_name",
                )

                # Reason for visit
                reason = st.text_area(
                    "Reason for Visit *",
                    placeholder="Please describe the reason for your appointment...",
                    key="visit_reason",
                    height=100,
                )

                st.markdown(
                    "<div style='height: 16px;'></div>", unsafe_allow_html=True
                )

                # Action buttons
                btn_col1, btn_col2 = st.columns(2)

                with btn_col1:
                    if st.button("← Back", use_container_width=True):
                        st.session_state.show_booking_modal = False
                        st.rerun()

                with btn_col2:
                    if st.button(
                        "Confirm Booking", type="primary", use_container_width=True
                    ):
                        if not reason:
                            st.error("Please enter a reason for your visit.")
                        else:
                            scheduled_dt = datetime.combine(
                                st.session_state.selected_date,
                                st.session_state.selected_time,
                                tzinfo=timezone.utc,
                            )

                            try:
                                appointment_service.create_appointment(
                                    patient_id=patient.id,
                                    scheduled_datetime=scheduled_dt,
                                    duration_minutes=st.session_state.selected_duration,
                                    reason=reason,
                                    created_by_user_id=user_id,
                                )

                                st.session_state.show_booking_modal = False
                                st.session_state.selected_date = None
                                st.session_state.selected_time = None
                                st.session_state.booking_success = True
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to book appointment: {str(e)}")

finally:
    db.close()
