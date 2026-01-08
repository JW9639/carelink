"""Bloodwork page."""

from __future__ import annotations

from html import escape
import math
import re

import streamlit as st

from app.db.session import SessionLocal
from app.services.bloodwork_service import BloodworkService
from app.services.patient_service import PatientService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Bloodwork", ["patient"]):
    st.stop()

st.markdown(
    """
    <style>
    .bloodwork-panels-anchor {
        height: 0;
        margin: 0;
    }
    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .bloodwork-panels-anchor) {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 0 auto 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        max-width: 1100px;
        width: 100%;
    }
    [data-testid="stHorizontalBlock"]:has(.bloodwork-card-marker) {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 0 auto 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        max-width: 900px;
        width: 100%;
    }
    .bloodwork-card-marker { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

STATUS_STYLES = {
    "normal": ("Normal", "#10b981", "rgba(16, 185, 129, 0.12)"),
    "low": ("Low", "#f59e0b", "rgba(245, 158, 11, 0.12)"),
    "high": ("High", "#f97316", "rgba(249, 115, 22, 0.12)"),
    "critical": ("Critical", "#ef4444", "rgba(239, 68, 68, 0.12)"),
    "unknown": ("Unknown", "#6b7280", "rgba(107, 114, 128, 0.12)"),
}

_TAG_PATTERN = re.compile(r"<[^>]*>")


def _range_positions(
    reference: dict,
) -> tuple[float | None, float | None, float | None, float | None]:
    low = reference.get("low")
    high = reference.get("high")
    if low is None or high is None:
        return None, None, None, None
    try:
        low = float(low)
        high = float(high)
    except (TypeError, ValueError):
        return None, None, None, None
    if high == low:
        return None, None, None, None

    span = high - low
    scale_min = low - span
    scale_max = high + span
    total = scale_max - scale_min
    low_pct = (low - scale_min) / total * 100
    high_pct = (high - scale_min) / total * 100
    return low_pct, high_pct, scale_min, scale_max


def _value_position(value: float | None, scale_min: float, scale_max: float) -> float | None:
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if scale_max == scale_min:
        return None
    value = max(min(value, scale_max), scale_min)
    return (value - scale_min) / (scale_max - scale_min) * 100


def _has_value(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, str) and not _TAG_PATTERN.sub("", value).strip():
        return False
    return True


def _sanitize_text(value: str) -> str:
    return _TAG_PATTERN.sub("", value).strip()


# Session state for view switching
if "bloodwork_view" not in st.session_state:
    st.session_state.bloodwork_view = "panels"
if "selected_bloodwork_id" not in st.session_state:
    st.session_state.selected_bloodwork_id = None
if "selected_category_index" not in st.session_state:
    st.session_state.selected_category_index = None
if "bloodwork_panel_page" not in st.session_state:
    st.session_state.bloodwork_panel_page = 1
if st.session_state.bloodwork_view not in {"panels", "markers"}:
    st.session_state.bloodwork_view = "panels"

user_id = st.session_state.get("user_id")

db = SessionLocal()
try:
    patient_service = PatientService(db)
    bloodwork_service = BloodworkService(db)

    patient = patient_service.get_patient_by_user_id(user_id) if user_id else None
    if not patient:
        st.error("Patient profile not found.")
        st.stop()

    bloodwork_results = bloodwork_service.get_published_results(patient.id)
    normalized = {
        bw.id: bloodwork_service.normalize_bloodwork(bw) for bw in bloodwork_results
    }
finally:
    db.close()

st.markdown(
    "<h2 style='color: #1e293b; margin-bottom: 4px;'>Bloodwork Results</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #0f172a; font-size: 16px; margin-top: 0;'>Review your published lab results and explore individual markers in detail.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

if not bloodwork_results:
    st.info("No bloodwork results have been shared yet.")
    st.stop()

panel_cards = []
for bw in bloodwork_results:
    data = normalized.get(bw.id, {})
    categories = data.get("categories", [])
    for idx, category in enumerate(categories):
        panel_cards.append(
            {
                "bloodwork": bw,
                "category_index": idx,
                "category": category,
                "test_name": data.get("test_name") or bw.test_type,
            }
        )

if not panel_cards:
    st.info("No bloodwork panels are available yet.")
    st.stop()

if st.session_state.bloodwork_view == "panels":
    with st.container():
        st.markdown('<div class="bloodwork-panels-anchor"></div>', unsafe_allow_html=True)
        panels_per_page = 6
        total_panels = len(panel_cards)
        total_pages = max(1, math.ceil(total_panels / panels_per_page))
        current_page = min(
            max(st.session_state.bloodwork_panel_page, 1), total_pages
        )
        st.session_state.bloodwork_panel_page = current_page

        if total_pages > 1:
            col_prev, col_page, col_next = st.columns([1, 2, 1], gap="small")
            with col_prev:
                if st.button("Previous", use_container_width=True, disabled=current_page == 1):
                    st.session_state.bloodwork_panel_page = current_page - 1
                    st.rerun()
            with col_page:
                start_idx = (current_page - 1) * panels_per_page + 1
                end_idx = min(current_page * panels_per_page, total_panels)
                st.markdown(
                    f"<div style='text-align: center; color: #0f172a; font-size: 16px;'>"
                    f"Showing {start_idx}–{end_idx} of {total_panels} panels</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: center; color: #64748b; font-size: 14px;'>"
                    f"Page {current_page} of {total_pages}</div>",
                    unsafe_allow_html=True,
                )
            with col_next:
                if st.button("Next", use_container_width=True, disabled=current_page == total_pages):
                    st.session_state.bloodwork_panel_page = current_page + 1
                    st.rerun()

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        start = (current_page - 1) * panels_per_page
        end = start + panels_per_page
        for panel in panel_cards[start:end]:
            bw = panel["bloodwork"]
            category = panel["category"]
            cat_summary = bloodwork_service.summarize_category(category)
            doctor = bw.approved_by_doctor
            doctor_name = (
                f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Assigned Clinician"
            )
            panel_name = escape(category.get("name") or panel["test_name"] or "Panel")
            status_text = (
                "All within range"
                if cat_summary.out_of_range == 0
                else f"{cat_summary.out_of_range} outside range"
            )
            col_left, col_right = st.columns([5, 1])
            with col_left:
                panel_html = "\n".join(
                    [
                        '<div class="bloodwork-card-marker"></div>',
                        f'<div style="font-size: 18px; font-weight: 700; color: #1e293b;">{panel_name}</div>',
                        '<div style="font-size: 16px; color: #0f172a; margin-top: 4px;">',
                        f'{bw.test_date.strftime("%B %d, %Y")} - {escape(doctor_name)}',
                        "</div>",
                        '<div style="margin-top: 12px; font-size: 16px; color: #0f172a;">',
                        f"{cat_summary.total} markers - {status_text}",
                        "</div>",
                    ]
                )
                st.markdown(panel_html, unsafe_allow_html=True)
            with col_right:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                if st.button(
                    "View",
                    key=f"view_panel_{bw.id}_{panel['category_index']}",
                    use_container_width=True,
                ):
                    st.session_state.bloodwork_view = "markers"
                    st.session_state.selected_bloodwork_id = bw.id
                    st.session_state.selected_category_index = panel["category_index"]
                    st.rerun()

elif st.session_state.bloodwork_view == "markers":
    selected_id = st.session_state.selected_bloodwork_id
    selected_bw = next((bw for bw in bloodwork_results if bw.id == selected_id), None)
    if not selected_bw:
        st.session_state.bloodwork_view = "panels"
        st.rerun()

    data = normalized.get(selected_bw.id, {})
    categories = data.get("categories", [])
    category_index = st.session_state.selected_category_index or 0
    if category_index >= len(categories):
        st.session_state.bloodwork_view = "panels"
        st.rerun()

    category = categories[category_index]
    category_name = escape(category.get("name", "Category"))

    if st.button("Back to Panels"):
        st.session_state.bloodwork_view = "panels"
        st.rerun()

    st.markdown(f"<h3 style='color: #000000; margin-bottom: 8px;'>{category_name}</h3>", unsafe_allow_html=True)

    markers = [
        marker for marker in category.get("markers", []) if _has_value(marker.get("value"))
    ]
    if not markers:
        st.info("No results were reported for this panel.")
        st.stop()

    for marker in markers:
        marker_name = escape(marker.get("name", "Marker"))
        abbreviation = escape(marker.get("abbreviation", ""))
        unit = escape(marker.get("unit", ""))
        value = marker.get("value")
        status = bloodwork_service.get_marker_status(marker)
        status_label, status_color, status_bg = STATUS_STYLES.get(
            status, STATUS_STYLES["unknown"]
        )
        reference = marker.get("reference_range") or {}
        low_pct, high_pct, scale_min, scale_max = _range_positions(reference)
        value_pct = (
            _value_position(value, scale_min, scale_max)
            if scale_min is not None and scale_max is not None
            else None
        )
        reference_text = ""
        if reference.get("low") is not None and reference.get("high") is not None:
            reference_text = f"{reference.get('low')} - {reference.get('high')}"
        reference_note = marker.get("reference_note") or ""

        if isinstance(value, str):
            marker_value = escape(_sanitize_text(value))
        else:
            marker_value = "N/A" if value is None else f"{value}"
        if unit:
            marker_value = f"{marker_value} {unit}"
        interpretation = marker.get("interpretation")
        interpretation_html = ""
        if interpretation:
            interpretation_html = (
                "<div style=\"font-size: 16px; color: #0f172a; margin-top: 10px;\">"
                f"Interpretation: {escape(str(interpretation))}</div>"
            )
        range_background = "#e5e7eb"
        if low_pct is not None and high_pct is not None:
            range_background = (
                "linear-gradient(to right, "
                f"#ef4444 0%, #ef4444 {low_pct}%, "
                f"#10b981 {low_pct}%, #10b981 {high_pct}%, "
                f"#ef4444 {high_pct}%, #ef4444 100%)"
            )
        boundary_html = ""
        if low_pct is not None and high_pct is not None:
            boundary_html = (
                "<div style=\"position:absolute; left:{0}%; top:-4px; width:2px; "
                "height:18px; background:#94a3b8; transform: translateX(-50%);\"></div>"
                "<div style=\"position:absolute; left:{1}%; top:-4px; width:2px; "
                "height:18px; background:#94a3b8; transform: translateX(-50%);\"></div>"
            ).format(low_pct, high_pct)
        value_html = ""
        if value_pct is not None:
            value_pct = max(0.0, min(100.0, value_pct))
            value_html = (
                "<div style=\"position:absolute; left:{0}%; top:-8px; width:0; height:0; "
                "border-left:7px solid transparent; border-right:7px solid transparent; "
                "border-top:12px solid #0f172a; transform: translateX(-50%);\"></div>"
            ).format(value_pct)

        reference_display = (
            escape(reference_text)
            if reference_text
            else escape(reference_note)
            if reference_note
            else "Not available"
        )
        card_html = "\n".join(
            [
                '<div style="background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid #e2e8f0;">',
                '<div style="display: flex; justify-content: space-between; align-items: flex-start;">',
                "<div>",
                f'<div style="font-size: 18px; font-weight: 700; color: #0f172a;">{marker_name} <span style="color: #64748b;">{abbreviation}</span></div>',
                f'<div style="font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 6px;">{marker_value}</div>',
                "</div>",
                f'<div style="background: {status_bg}; color: {status_color}; padding: 6px 14px; border-radius: 999px; font-size: 14px; font-weight: 700;">{status_label}</div>',
                "</div>",
                '<div style="margin-top: 16px;">',
                f'<div style="position: relative; height: 10px; border-radius: 999px; background: {range_background};">',
                boundary_html,
                value_html,
                "</div>",
                f'<div style="font-size: 16px; color: #0f172a; margin-top: 8px;">Reference range: {reference_display}</div>',
                interpretation_html,
                "</div>",
                "</div>",
            ]
        )
        st.markdown(card_html, unsafe_allow_html=True)
