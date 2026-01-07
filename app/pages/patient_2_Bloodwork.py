"""Bloodwork page."""

from __future__ import annotations

from html import escape

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
    [data-testid="stHorizontalBlock"]:has(.bloodwork-card-marker) {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
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


def _range_gradient(reference: dict) -> tuple[str, float] | tuple[None, None]:
    low = reference.get("low")
    high = reference.get("high")
    optimal_low = reference.get("optimal_low", low)
    optimal_high = reference.get("optimal_high", high)
    if low is None or high is None or high == low:
        return None, None
    try:
        low = float(low)
        high = float(high)
        optimal_low = float(optimal_low)
        optimal_high = float(optimal_high)
    except (TypeError, ValueError):
        return None, None

    total = high - low
    optimal_low_pct = max(0.0, min(100.0, (optimal_low - low) / total * 100))
    optimal_high_pct = max(0.0, min(100.0, (optimal_high - low) / total * 100))

    gradient = (
        "linear-gradient(to right, "
        f"#ef4444 0%, "
        f"#f59e0b {optimal_low_pct}%, "
        f"#10b981 {optimal_low_pct}%, "
        f"#10b981 {optimal_high_pct}%, "
        f"#f59e0b {optimal_high_pct}%, "
        "#ef4444 100%)"
    )
    return gradient, total


def _marker_position(value: float | None, reference: dict) -> float | None:
    if value is None:
        return None
    low = reference.get("low")
    high = reference.get("high")
    if low is None or high is None:
        return None
    try:
        low = float(low)
        high = float(high)
        value = float(value)
    except (TypeError, ValueError):
        return None
    if high == low:
        return None
    value = max(min(value, high), low)
    return (value - low) / (high - low) * 100


# Session state for view switching
if "bloodwork_view" not in st.session_state:
    st.session_state.bloodwork_view = "list"
if "selected_bloodwork_id" not in st.session_state:
    st.session_state.selected_bloodwork_id = None
if "selected_category_index" not in st.session_state:
    st.session_state.selected_category_index = None

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
    "<p style='color: #475569; font-size: 16px; margin-top: 0;'>Review your published lab results and explore individual markers in detail.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

if not bloodwork_results:
    st.info("No bloodwork results have been shared yet.")
    st.stop()

if st.session_state.bloodwork_view == "list":
    for bw in bloodwork_results:
        data = normalized.get(bw.id, {})
        categories = data.get("categories", [])
        summary = bloodwork_service.summarize_categories(categories)
        doctor = bw.approved_by_doctor
        doctor_name = (
            f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Assigned Clinician"
        )
        test_name = escape(data.get("test_name") or bw.test_type)
        col_left, col_right = st.columns([5, 1])
        with col_left:
            st.markdown(
                f"""
                <div class="bloodwork-card-marker"></div>
                <div style="font-size: 18px; font-weight: 700; color: #1e293b;">{test_name}</div>
                <div style="font-size: 16px; color: #64748b; margin-top: 4px;">
                    {bw.test_date.strftime("%B %d, %Y")} - {escape(doctor_name)}
                </div>
                <div style="margin-top: 12px; font-size: 16px; color: #475569;">
                    {summary.total} markers - {summary.out_of_range} outside range
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_right:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            if st.button("View", key=f"view_bloodwork_{bw.id}", use_container_width=True):
                st.session_state.bloodwork_view = "categories"
                st.session_state.selected_bloodwork_id = bw.id
                st.session_state.selected_category_index = None
                st.rerun()

elif st.session_state.bloodwork_view == "categories":
    selected_id = st.session_state.selected_bloodwork_id
    selected_bw = next((bw for bw in bloodwork_results if bw.id == selected_id), None)
    if not selected_bw:
        st.session_state.bloodwork_view = "list"
        st.rerun()

    data = normalized.get(selected_bw.id, {})
    categories = data.get("categories", [])
    summary = bloodwork_service.summarize_categories(categories)
    test_name = escape(data.get("test_name") or selected_bw.test_type)

    if st.button("Back to Results"):
        st.session_state.bloodwork_view = "list"
        st.session_state.selected_bloodwork_id = None
        st.rerun()

    st.markdown(
        f"### {test_name} ({selected_bw.test_date.strftime('%B %d, %Y')})"
    )
    st.markdown(
        f"{summary.total} markers total - {summary.out_of_range} outside range"
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    for idx, category in enumerate(categories):
        name = escape(category.get("name", "Category"))
        cat_summary = bloodwork_service.summarize_category(category)
        status_text = (
            "All within range"
            if cat_summary.out_of_range == 0
            else f"{cat_summary.out_of_range} outside range"
        )
        st.markdown(
            f"""
            <div style="
                background: white;
                border-radius: 14px;
                padding: 18px;
                margin-bottom: 12px;
                border: 1px solid #e2e8f0;
            ">
                <div style="font-size: 17px; font-weight: 700; color: #1e293b;">{name}</div>
                <div style="font-size: 16px; color: #64748b; margin-top: 4px;">
                    {cat_summary.total} markers - {status_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "View Markers",
            key=f"view_category_{selected_bw.id}_{idx}",
            use_container_width=True,
        ):
            st.session_state.bloodwork_view = "markers"
            st.session_state.selected_category_index = idx
            st.rerun()

elif st.session_state.bloodwork_view == "markers":
    selected_id = st.session_state.selected_bloodwork_id
    selected_bw = next((bw for bw in bloodwork_results if bw.id == selected_id), None)
    if not selected_bw:
        st.session_state.bloodwork_view = "list"
        st.rerun()

    data = normalized.get(selected_bw.id, {})
    categories = data.get("categories", [])
    category_index = st.session_state.selected_category_index or 0
    if category_index >= len(categories):
        st.session_state.bloodwork_view = "categories"
        st.rerun()

    category = categories[category_index]
    category_name = escape(category.get("name", "Category"))

    if st.button("Back to Categories"):
        st.session_state.bloodwork_view = "categories"
        st.rerun()

    st.markdown(f"### {category_name}")
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    for marker in category.get("markers", []):
        marker_name = escape(marker.get("name", "Marker"))
        abbreviation = escape(marker.get("abbreviation", ""))
        unit = escape(marker.get("unit", ""))
        value = marker.get("value")
        status = bloodwork_service.get_marker_status(marker)
        status_label, status_color, status_bg = STATUS_STYLES.get(
            status, STATUS_STYLES["unknown"]
        )
        reference = marker.get("reference_range") or {}
        gradient, _ = _range_gradient(reference)
        value_pct = _marker_position(value, reference)
        reference_text = ""
        if reference.get("low") is not None and reference.get("high") is not None:
            reference_text = f"{reference.get('low')} - {reference.get('high')}"

        marker_value = "N/A" if value is None else f"{value}"
        if unit:
            marker_value = f"{marker_value} {unit}"
        interpretation = marker.get("interpretation")
        interpretation_html = ""
        if interpretation:
            interpretation_html = (
                "<div style=\"font-size: 16px; color: #64748b; margin-top: 10px;\">"
                f"Interpretation: {escape(str(interpretation))}</div>"
            )
        arrow_html = ""
        if value_pct is not None and gradient:
            arrow_html = (
                "<div style=\"position:absolute; left:{0}%; top:-6px; "
                "transform: translateX(-50%); width: 0; height: 0; "
                "border-left: 6px solid transparent; border-right: 6px solid transparent; "
                "border-top: 10px solid {1};\"></div>"
            ).format(value_pct, status_color)

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
                            {marker_name} <span style="color: #64748b;">{abbreviation}</span>
                        </div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 6px;">
                            {marker_value}
                        </div>
                    </div>
                    <div style="
                        background: {status_bg};
                        color: {status_color};
                        padding: 6px 14px;
                        border-radius: 999px;
                        font-size: 14px;
                        font-weight: 700;
                    ">{status_label}</div>
                </div>
                <div style="margin-top: 16px;">
                    <div style="
                        position: relative;
                        height: 10px;
                        border-radius: 999px;
                        background: {gradient if gradient else '#e5e7eb'};
                    ">
                        {arrow_html}
                    </div>
                    <div style="font-size: 16px; color: #64748b; margin-top: 8px;">
                        Reference range: {reference_text or 'Not available'}
                    </div>
                    {interpretation_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
