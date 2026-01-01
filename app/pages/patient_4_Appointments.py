"""Patient Appointments page - Book and view appointments with tabbed interface."""

from __future__ import annotations

import calendar
import math
from datetime import datetime, date, time, timedelta, timezone

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
    st.markdown("""
    <h2 style="color: #1e293b; margin-bottom: 8px;">📅 Appointments</h2>
    <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">View your appointments or book a new visit.</p>
    """, unsafe_allow_html=True)
    
    # Show success message if just booked
    if st.session_state.booking_success:
        st.success("✅ Your appointment has been booked successfully! It is now pending review by our staff who will assign a doctor.")
        st.session_state.booking_success = False
    
    # Show hint if directed to book
    if default_tab_index == 1:
        st.info("👆 Click the **'➕ Book Appointment'** tab above to schedule a new appointment.")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 My Appointments", "➕ Book Appointment"])
    
    # ========== TAB 1: MY APPOINTMENTS (History & Upcoming) ==========
    with tab1:
        # Upcoming Appointments Section
        st.markdown("<h4 style='color: #1e293b; font-weight: 600; margin-top: 16px; margin-bottom: 16px;'>Upcoming Appointments</h4>", unsafe_allow_html=True)
        
        upcoming_appointments = appointment_service.get_patient_upcoming_appointments(patient.id)
        
        if upcoming_appointments:
            # Show max 2 upcoming
            for appt in upcoming_appointments[:2]:
                status_color = "#f59e0b" if appt.status == AppointmentStatus.PENDING else "#10b981"
                status_text = "Pending Review" if appt.status == AppointmentStatus.PENDING else "Confirmed"
                doctor_info = f"Dr. {appt.doctor.last_name}" if appt.doctor else "Doctor TBD"
                
                appt_date = appt.scheduled_datetime.strftime("%A, %B %d, %Y")
                appt_time = appt.scheduled_datetime.strftime("%I:%M %p")
                
                st.markdown(f"""
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
                """, unsafe_allow_html=True)
            
            if len(upcoming_appointments) > 2:
                st.info(f"📌 You have {len(upcoming_appointments) - 2} more upcoming appointment(s).")
        else:
            st.markdown("""
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
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Past Appointments (History) Section
        st.markdown("<h4 style='color: #1e293b; font-weight: 600; margin-top: 16px; margin-bottom: 16px;'>Appointment History</h4>", unsafe_allow_html=True)
        
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
            patient.id, 
            limit=ITEMS_PER_PAGE, 
            offset=offset
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
                
                st.markdown(f"""
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
                """, unsafe_allow_html=True)
            
            # Pagination controls
            if total_pages > 1:
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("◀ Previous", disabled=st.session_state.history_page == 0, key="prev_history"):
                        st.session_state.history_page -= 1
                        st.rerun()
                
                with col2:
                    st.markdown(f"<p style='text-align: center; color: #64748b; margin: 8px 0;'>Page {st.session_state.history_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Next ▶", disabled=st.session_state.history_page >= total_pages - 1, key="next_history"):
                        st.session_state.history_page += 1
                        st.rerun()
        else:
            st.markdown("""
            <div style="
                background: #f8fafc;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                border: 1px dashed #e2e8f0;
            ">
                <p style="color: #64748b; font-size: 15px; margin: 0;">No appointment history yet</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== TAB 2: BOOK APPOINTMENT ==========
    with tab2:
        st.markdown("<h4 style='color: #1e293b; font-weight: 600; margin-top: 16px; margin-bottom: 16px;'>Select a Date</h4>", unsafe_allow_html=True)
        
        # Calendar Navigation
        col_prev, col_title, col_next = st.columns([1, 3, 1])
        
        with col_prev:
            if st.button("◀ Prev", key="prev_month"):
                if st.session_state.calendar_month == 1:
                    st.session_state.calendar_month = 12
                    st.session_state.calendar_year -= 1
                else:
                    st.session_state.calendar_month -= 1
                st.session_state.selected_date = None
                st.session_state.selected_time = None
                st.rerun()
        
        with col_title:
            month_name = calendar.month_name[st.session_state.calendar_month]
            st.markdown(f"<h4 style='text-align: center; margin: 0; color: #1e293b; font-weight: 600;'>{month_name} {st.session_state.calendar_year}</h4>", unsafe_allow_html=True)
        
        with col_next:
            if st.button("Next ▶", key="next_month"):
                if st.session_state.calendar_month == 12:
                    st.session_state.calendar_month = 1
                    st.session_state.calendar_year += 1
                else:
                    st.session_state.calendar_month += 1
                st.session_state.selected_date = None
                st.session_state.selected_time = None
                st.rerun()
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # Calendar Grid
        cal = calendar.Calendar(firstweekday=6)  # Sunday first
        month_days = cal.monthdayscalendar(st.session_state.calendar_year, st.session_state.calendar_month)
        
        # Day headers
        day_headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        header_cols = st.columns(7)
        for i, day in enumerate(day_headers):
            with header_cols[i]:
                st.markdown(f"<div style='text-align: center; font-weight: 600; color: #64748b; font-size: 12px; padding: 8px;'>{day}</div>", unsafe_allow_html=True)
        
        # Calendar days
        today = date.today()
        for week in month_days:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                    else:
                        current_date = date(st.session_state.calendar_year, st.session_state.calendar_month, day)
                        is_past = current_date < today
                        is_weekend = i == 0 or i == 6  # Sunday or Saturday
                        is_selected = st.session_state.selected_date == current_date
                        is_today = current_date == today
                        
                        # Styling
                        if is_selected:
                            bg_color = "#0066cc"
                            text_color = "white"
                        elif is_past or is_weekend:
                            bg_color = "#f1f5f9"
                            text_color = "#94a3b8"
                        elif is_today:
                            bg_color = "#dbeafe"
                            text_color = "#0066cc"
                        else:
                            bg_color = "white"
                            text_color = "#1e293b"
                        
                        # Only allow clicking on valid days
                        if not is_past and not is_weekend:
                            if st.button(str(day), key=f"day_{day}", use_container_width=True):
                                st.session_state.selected_date = current_date
                                st.session_state.selected_time = None
                                st.rerun()
                        else:
                            st.markdown(f"""
                            <div style="
                                text-align: center;
                                padding: 8px;
                                background: {bg_color};
                                border-radius: 8px;
                                color: {text_color};
                                font-size: 14px;
                            ">{day}</div>
                            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Time Slots Section (only show if date selected)
        if st.session_state.selected_date:
            st.markdown("---")
            selected_date_str = st.session_state.selected_date.strftime("%A, %B %d, %Y")
            st.markdown(f"<h4 style='color: #1e293b; font-weight: 600; margin-bottom: 16px;'>Select a Time for {selected_date_str}</h4>", unsafe_allow_html=True)
            
            # Duration selector
            duration_col1, duration_col2 = st.columns([2, 3])
            with duration_col1:
                duration = st.selectbox(
                    "Appointment Duration",
                    options=[30, 60],
                    format_func=lambda x: f"{x} minutes",
                    key="duration_select"
                )
                st.session_state.selected_duration = duration
            
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            # Get available slots
            am_slots, pm_slots = appointment_service.get_available_slots(
                st.session_state.selected_date, 
                st.session_state.selected_duration
            )
            
            # Time slots in AM/PM columns
            am_col, pm_col = st.columns(2)
            
            with am_col:
                st.markdown("<div style='font-weight: 600; color: #1e293b; margin-bottom: 12px; font-size: 15px;'>Morning</div>", unsafe_allow_html=True)
                for slot in am_slots:
                    is_selected = st.session_state.selected_time == slot.time
                    if slot.is_available:
                        btn_type = "primary" if is_selected else "secondary"
                        if st.button(slot.display, key=f"am_{slot.time}", use_container_width=True, type=btn_type):
                            st.session_state.selected_time = slot.time
                            st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="
                            text-align: center;
                            padding: 8px 16px;
                            background: #f1f5f9;
                            border-radius: 6px;
                            color: #94a3b8;
                            font-size: 14px;
                            margin-bottom: 8px;
                            text-decoration: line-through;
                        ">{slot.display}</div>
                        """, unsafe_allow_html=True)
            
            with pm_col:
                st.markdown("<div style='font-weight: 600; color: #1e293b; margin-bottom: 12px; font-size: 15px;'>Afternoon</div>", unsafe_allow_html=True)
                for slot in pm_slots:
                    is_selected = st.session_state.selected_time == slot.time
                    if slot.is_available:
                        btn_type = "primary" if is_selected else "secondary"
                        if st.button(slot.display, key=f"pm_{slot.time}", use_container_width=True, type=btn_type):
                            st.session_state.selected_time = slot.time
                            st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="
                            text-align: center;
                            padding: 8px 16px;
                            background: #f1f5f9;
                            border-radius: 6px;
                            color: #94a3b8;
                            font-size: 14px;
                            margin-bottom: 8px;
                            text-decoration: line-through;
                        ">{slot.display}</div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
            
            # Continue button (only if time selected)
            if st.session_state.selected_time:
                if st.button("Continue to Book →", type="primary", use_container_width=True):
                    st.session_state.show_booking_modal = True
                    st.rerun()
        
        # Booking Modal
        if st.session_state.show_booking_modal and st.session_state.selected_date and st.session_state.selected_time:
            # Dark overlay
            st.markdown("""
            <style>
            .booking-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 9998;
            }
            </style>
            <div class="booking-overlay"></div>
            """, unsafe_allow_html=True)
            
            # Modal content using Streamlit container
            with st.container():
                st.markdown("""
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    border-radius: 16px;
                    padding: 32px;
                    width: 500px;
                    max-width: 90vw;
                    z-index: 9999;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                ">
                """, unsafe_allow_html=True)
                
                st.markdown("<h4 style='color: #1e293b; font-weight: 600; margin-bottom: 16px;'>Confirm Your Appointment</h4>", unsafe_allow_html=True)
                
                # Display selected date/time
                appt_datetime = datetime.combine(st.session_state.selected_date, st.session_state.selected_time)
                formatted_date = appt_datetime.strftime("%A, %B %d, %Y")
                formatted_time = appt_datetime.strftime("%I:%M %p")
                
                st.markdown(f"""
                <div style="
                    background: #f0f9ff;
                    border-radius: 8px;
                    padding: 16px;
                    margin-bottom: 20px;
                    border: 1px solid #bae6fd;
                ">
                    <div style="font-weight: 600; color: #0369a1;">📅 {formatted_date}</div>
                    <div style="color: #0369a1; margin-top: 4px;">🕐 {formatted_time} • {st.session_state.selected_duration} minutes</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Patient info (pre-filled)
                patient_name = f"{patient.first_name} {patient.last_name}"
                patient_address = f"{patient.address_line_1}, {patient.city}" if patient.address_line_1 else "Not on file"
                
                st.markdown("**Patient Details**")
                st.text_input("Name", value=patient_name, disabled=True, key="confirm_name")
                st.text_input("Address", value=patient_address, disabled=True, key="confirm_address")
                
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                # Reason for visit
                reason = st.text_area(
                    "Reason for Visit *",
                    placeholder="Please describe the reason for your appointment...",
                    key="visit_reason",
                    height=100
                )
                
                st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                
                # Action buttons
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.show_booking_modal = False
                        st.rerun()
                
                with btn_col2:
                    if st.button("Confirm Booking", type="primary", use_container_width=True):
                        if not reason:
                            st.error("Please enter a reason for your visit.")
                        else:
                            # Create the appointment
                            scheduled_dt = datetime.combine(
                                st.session_state.selected_date,
                                st.session_state.selected_time,
                                tzinfo=timezone.utc
                            )
                            
                            try:
                                appointment_service.create_appointment(
                                    patient_id=patient.id,
                                    scheduled_datetime=scheduled_dt,
                                    duration_minutes=st.session_state.selected_duration,
                                    reason=reason,
                                    created_by_user_id=user_id,
                                )
                                
                                # Reset state and show success
                                st.session_state.show_booking_modal = False
                                st.session_state.selected_date = None
                                st.session_state.selected_time = None
                                st.session_state.booking_success = True
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to book appointment: {str(e)}")
                
                st.markdown("</div>", unsafe_allow_html=True)

finally:
    db.close()
