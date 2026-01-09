"""Patient Appointments page - Book and view appointments with tabbed interface."""

from __future__ import annotations

import calendar
import math
from datetime import datetime, date, timezone
from html import escape

import streamlit as st

from app.db.session import SessionLocal
from app.services.appointment_service import AppointmentService
from app.services.patient_service import PatientService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.ui.components.page_header import render_page_header
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

    render_page_header(
        "Appointments",
        "View your appointments or book a new visit.",
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
                doctor_info = escape(doctor_info)
                reason_text = escape(appt.reason) if appt.reason else ""

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
                            <div style="color: #64748b; font-size: 14px; margin-top: 4px;">{appt_time} - {appt.duration_minutes} min - {doctor_info}</div>
                            {f'<div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Reason: {reason_text}</div>' if reason_text else ''}
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
                        "Previous",
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
                        "Next",
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
                doctor_info = escape(doctor_info)
                reason_text = escape(appt.reason) if appt.reason else ""
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
                            <div style="color: #64748b; font-size: 14px; margin-top: 4px;">{appt_time} - {appt.duration_minutes} min - {doctor_info}</div>
                            {f'<div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Reason: {reason_text}</div>' if reason_text else ''}
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
                        "Previous",
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
                        "Next",
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
                max-width: 400px !important;
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
            /* Thicker black tab slider/highlight */
            [data-baseweb="tab-highlight"] {
                background-color: #111827 !important;
                height: 4px !important;
            }
            /* Month title styling */
            .month-title {
                text-align: center !important;
                font-weight: 700 !important;
                font-size: 28px !important;
                color: #111827 !important;
                margin: 0 !important;
                line-height: 42px !important;
            }
            /* Section divider line */
            [data-testid="stColumn"]:has(.calendar-marker) hr {
                border: none !important;
                height: 3px !important;
                background-color: #111827 !important;
                margin: 0 !important;
            }
            /* Section headers with underline */
            .section-header {
                color: #111827 !important;
                font-size: 20px !important;
                font-weight: 600 !important;
                margin-bottom: 16px !important;
                text-decoration: underline !important;
                text-underline-offset: 6px !important;
            }
            /* Override ALL buttons in calendar section - reset blue gradient */
            [data-testid="stColumn"]:has(.calendar-marker) [data-testid="stButton"] button,
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="primary"],
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="secondary"] {
                background: none !important;
                background-color: white !important;
                background-image: none !important;
                box-shadow: none !important;
                border: 1px solid #d1d5db !important;
                color: #374151 !important;
                padding: 8px 16px !important;
                border-radius: 8px !important;
                transform: none !important;
            }
            /* Primary (selected) button - teal */
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="primary"] {
                background: #0d9488 !important;
                background-color: #0d9488 !important;
                border-color: #0d9488 !important;
                color: white !important;
            }
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="primary"] p {
                color: white !important;
            }
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="primary"]:hover {
                background: #0f766e !important;
                background-color: #0f766e !important;
                border-color: #0f766e !important;
            }
            /* Secondary (unselected) button - gray outline */
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="secondary"] {
                background: white !important;
                background-color: white !important;
                border: 1px solid #d1d5db !important;
                color: #374151 !important;
            }
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="secondary"] p {
                color: #374151 !important;
            }
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="secondary"]:hover {
                border-color: #0d9488 !important;
                color: #0d9488 !important;
                background: #f0fdfa !important;
                background-color: #f0fdfa !important;
            }
            [data-testid="stColumn"]:has(.calendar-marker) button[kind="secondary"]:hover p {
                color: #0d9488 !important;
            }
            /* Input and textarea styling for confirm form */
            [data-testid="stColumn"]:has(.confirm-marker) input,
            [data-testid="stColumn"]:has(.confirm-marker) textarea,
            [data-testid="stColumn"]:has(.confirm-marker) input[type="text"],
            [data-testid="stColumn"]:has(.confirm-marker) [data-testid="stTextInput"] input {
                background-color: white !important;
                color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
                border: 1px solid #d1d5db !important;
                border-radius: 8px !important;
                padding: 12px !important;
                opacity: 1 !important;
            }
            /* Disabled inputs should still show dark text */
            [data-testid="stColumn"]:has(.confirm-marker) input:disabled,
            [data-testid="stColumn"]:has(.confirm-marker) input[disabled] {
                color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
                opacity: 1 !important;
            }
            [data-testid="stColumn"]:has(.confirm-marker) input::placeholder,
            [data-testid="stColumn"]:has(.confirm-marker) textarea::placeholder {
                color: #9ca3af !important;
            }
            /* Input wrapper/container styling */
            [data-testid="stColumn"]:has(.confirm-marker) [data-baseweb="input"],
            [data-testid="stColumn"]:has(.confirm-marker) [data-baseweb="textarea"] {
                background-color: white !important;
            }
            /* Labels and text in confirm form - make dark */
            [data-testid="stColumn"]:has(.confirm-marker) label,
            [data-testid="stColumn"]:has(.confirm-marker) label p,
            [data-testid="stColumn"]:has(.confirm-marker) [data-testid="stMarkdownContainer"]:not([data-testid="stButton"] *) p,
            [data-testid="stColumn"]:has(.confirm-marker) [data-testid="stTextInput"] label p,
            [data-testid="stColumn"]:has(.confirm-marker) [data-testid="stTextArea"] label p {
                color: #111827 !important;
            }
            /* Required field asterisk - make red */
            [data-testid="stColumn"]:has(.confirm-marker) label span[data-testid="stMarkdownContainer"] span,
            [data-testid="stColumn"]:has(.confirm-marker) label [data-testid="stMarkdownContainer"] p span {
                color: #ef4444 !important;
            }
            /* Keep button text white in confirm form */
            [data-testid="stColumn"]:has(.confirm-marker) [data-testid="stButton"] button p,
            [data-testid="stColumn"]:has(.confirm-marker) button p {
                color: #ffffff !important;
            }
            /* ========== MODAL DIALOG STYLING ========== */
            /* Modal dialog container - white background */
            div[role="dialog"] {
                background: white !important;
                border-radius: 16px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
                max-width: 800px !important;
            }
            /* Modal header */
            div[role="dialog"] > div:first-child {
                background: white !important;
                border-bottom: 1px solid #e5e7eb !important;
                padding-bottom: 16px !important;
            }
            /* Modal title */
            div[role="dialog"] > div:first-child p {
                color: #111827 !important;
                font-weight: 600 !important;
            }
            /* Modal body/content area */
            div[role="dialog"] > div:nth-child(2) {
                background: white !important;
                color: #111827 !important;
            }
            /* All text in modal */
            div[role="dialog"] p,
            div[role="dialog"] span,
            div[role="dialog"] label {
                color: #111827 !important;
            }
            /* Input fields in modal */
            div[role="dialog"] input,
            div[role="dialog"] textarea {
                background-color: #f9fafb !important;
                color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
                border: 1px solid #d1d5db !important;
                border-radius: 8px !important;
            }
            div[role="dialog"] input:disabled {
                background-color: #f3f4f6 !important;
                color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
                opacity: 1 !important;
            }
            div[role="dialog"] input::placeholder,
            div[role="dialog"] textarea::placeholder {
                color: #9ca3af !important;
                -webkit-text-fill-color: #9ca3af !important;
            }
            /* Input wrapper styling */
            div[role="dialog"] [data-baseweb="input"],
            div[role="dialog"] [data-baseweb="textarea"],
            div[role="dialog"] [data-baseweb="base-input"] {
                background-color: #f9fafb !important;
                border-color: #d1d5db !important;
            }
            /* Primary button in modal - Blue gradient */
            div[role="dialog"] button[kind="primary"] {
                background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25) !important;
            }
            div[role="dialog"] button[kind="primary"] p {
                color: white !important;
            }
            div[role="dialog"] button[kind="primary"]:hover {
                background: linear-gradient(135deg, #0052a3 0%, #003d7a 100%) !important;
                transform: translateY(-1px) !important;
            }
            /* Secondary button in modal - Gray outline */
            div[role="dialog"] button[kind="secondary"] {
                background: white !important;
                color: #374151 !important;
                border: 1px solid #d1d5db !important;
                border-radius: 10px !important;
                font-weight: 500 !important;
            }
            div[role="dialog"] button[kind="secondary"] p {
                color: #374151 !important;
            }
            div[role="dialog"] button[kind="secondary"]:hover {
                background: #f3f4f6 !important;
                border-color: #9ca3af !important;
            }
            /* Close button styling */
            div[role="dialog"] button[aria-label="Close"] {
                background: transparent !important;
                border: none !important;
                color: #6b7280 !important;
                box-shadow: none !important;
            }
            div[role="dialog"] button[aria-label="Close"]:hover {
                color: #111827 !important;
                background: #f3f4f6 !important;
            }
            div[role="dialog"] button[aria-label="Close"] svg {
                stroke: #6b7280 !important;
            }
            /* Label styling in modal */
            div[role="dialog"] label p {
                color: #374151 !important;
                font-weight: 500 !important;
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
                "<h3 class='section-header'>Select a Date</h3>",
                unsafe_allow_html=True,
            )

            # Calendar navigation
            nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

            with nav_col1:
                if st.button("Prev", key="prev_month", use_container_width=True):
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
                    f"<p class='month-title'>{month_name} {st.session_state.calendar_year}</p>",
                    unsafe_allow_html=True,
                )

            with nav_col3:
                if st.button("Next", key="next_month", use_container_width=True):
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
                            is_selected = st.session_state.selected_date == current_date

                            if is_selected:
                                st.markdown(
                                    f"<div style='text-align:center;padding:2px;'><div style='display:flex;align-items:center;justify-content:center;background:#10b981;color:white;border-radius:8px;font-size:14px;font-weight:600;padding:8px 4px;box-shadow:0 2px 4px rgba(16,185,129,0.3);'>* {day}</div></div>",
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
                    "<h3 class='section-header' style='margin-bottom: 4px !important;'>Select a Time</h3>",
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
                    is_30_selected = st.session_state.selected_duration == 30
                    if st.button(
                        "* 30 min" if is_30_selected else "30 min",
                        key="dur_30",
                        type="primary" if is_30_selected else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.selected_duration = 30
                        st.session_state.selected_time = None
                        st.rerun()
                with dur_col2:
                    is_60_selected = st.session_state.selected_duration == 60
                    if st.button(
                        "* 60 min" if is_60_selected else "60 min",
                        key="dur_60",
                        type="primary" if is_60_selected else "secondary",
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
                            btn_type = "primary" if is_selected else "secondary"
                            if st.button(
                                f"* {slot.display}" if is_selected else slot.display,
                                key=f"am_{slot.time}",
                                type=btn_type,
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
                            btn_type = "primary" if is_selected else "secondary"
                            if st.button(
                                f"* {slot.display}" if is_selected else slot.display,
                                key=f"pm_{slot.time}",
                                type=btn_type,
                                use_container_width=True,
                            ):
                                st.session_state.selected_time = slot.time
                                st.rerun()
                        else:
                            st.markdown(
                                f"<div style='text-align:center;padding:8px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;color:#d1d5db;font-size:13px;text-decoration:line-through;margin-bottom:8px;'>{slot.display}</div>",
                                unsafe_allow_html=True,
                            )

        # Continue button - outside the calendar column so it gets default blue styling
        if st.session_state.selected_date and st.session_state.selected_time:
            spacer_l2, btn_col, spacer_r2 = st.columns([1, 4, 1])
            with btn_col:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                if st.button(
                    "Continue to Confirm", type="primary", use_container_width=True
                ):
                    st.session_state.show_booking_modal = True
                    st.rerun()

        # Booking Confirmation Modal
        if (
            st.session_state.show_booking_modal
            and st.session_state.selected_date
            and st.session_state.selected_time
        ):
            # Modal using st.dialog (Streamlit 1.33+)
            @st.dialog("Confirm Your Appointment", width="large")
            def show_confirmation_modal():
                st.markdown(
                    '<div class="confirm-marker"></div>', unsafe_allow_html=True
                )

                # Display selected date/time
                appt_datetime = datetime.combine(
                    st.session_state.selected_date, st.session_state.selected_time
                )
                formatted_date = appt_datetime.strftime("%A, %B %d, %Y")
                formatted_time = appt_datetime.strftime("%I:%M %p")

                st.markdown(
                    f"""
                    <div style="background: #f9fafb; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e5e7eb;">
                            <span style="color: #6b7280; font-size: 14px;">Date</span>
                            <span style="color: #111827; font-weight: 500;">{formatted_date}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e5e7eb;">
                            <span style="color: #6b7280; font-size: 14px;">Time</span>
                            <span style="color: #111827; font-weight: 500;">{formatted_time}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                            <span style="color: #6b7280; font-size: 14px;">Duration</span>
                            <span style="color: #111827; font-weight: 500;">{st.session_state.selected_duration} minutes</span>
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
                    key="modal_confirm_name",
                )

                # Reason for visit
                st.markdown(
                    '<p style="font-size: 14px; margin-bottom: 4px; color: #111827;">Reason for Visit <span style="color: #ef4444;">*</span></p>',
                    unsafe_allow_html=True,
                )
                reason = st.text_area(
                    "Reason for Visit",
                    placeholder="Please describe the reason for your appointment...",
                    key="modal_visit_reason",
                    height=100,
                    label_visibility="collapsed",
                )

                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

                # Action buttons
                btn_col1, btn_col2 = st.columns(2)

                with btn_col1:
                    if st.button("Back", use_container_width=True, key="modal_back"):
                        st.session_state.show_booking_modal = False
                        st.rerun()

                with btn_col2:
                    if st.button(
                        "Confirm Booking",
                        type="primary",
                        use_container_width=True,
                        key="modal_confirm",
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

            # Call the modal function to display it
            show_confirmation_modal()

finally:
    db.close()
