"""Results Review page."""

from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from app.db.repositories.doctor_repository import DoctorRepository
from app.db.repositories.patient_repository import PatientRepository
from app.db.session import SessionLocal
from app.services.bloodwork_service import BloodworkService
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Results Review", ["doctor"]):
    st.stop()

st.markdown(
    """
<style>
.results-hero {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.12), rgba(0, 168, 150, 0.12));
  border: 1px solid #dbe7f3;
  border-radius: 16px;
  padding: 20px 24px;
  margin-bottom: 32px;
}
.results-hero h2 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
  font-weight: 700;
}
.results-hero p {
  margin: 6px 0 0 0;
  color: #475569;
  font-size: 16px;
}
.results-section {
  margin: 16px 0 8px;
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}
.results-summary {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 12px;
}
.results-summary strong {
  color: #0f172a;
}
.results-summary span {
  color: #475569;
}
.entry-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 14px;
}
.entry-card-anchor {
  height: 0;
  margin: 0;
}
div[data-testid="stForm"]:has(.entry-card-anchor) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 20px;
}
.entry-actions-anchor {
  height: 0;
}
.entry-actions-anchor + div[data-testid="stHorizontalBlock"] {
  align-items: center;
}
.entry-actions-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
  display: flex;
  justify-content: flex-end;
}
.entry-card h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
  font-weight: 700;
}
.entry-card p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 16px;
}
.entry-head {
  margin: 4px 0;
}
.entry-head span {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: #64748b;
}
.entry-summary {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 16px;
  font-size: 16px;
  line-height: 1.6;
}
.entry-summary strong {
  color: #0f172a;
}
.entry-summary span {
  color: #475569;
}
.entry-list-anchor {
  height: 0;
  margin: 2px 0 0;
}
.entry-list-anchor ~ div[data-testid="stHorizontalBlock"] {
  background: #ffffff;
  padding: 6px 4px;
  margin: 0;
  gap: 6px;
  column-gap: 6px;
  border-bottom: 1px solid #e5e7eb;
}
.entry-list-anchor ~ div[data-testid="stHorizontalBlock"]:last-child {
  border-bottom: none;
}
.entry-marker {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}
.entry-meta {
  font-size: 16px;
  color: #64748b;
  margin-top: 4px;
}

/* Select card */
div[data-testid="stForm"] {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  margin: 0 auto 20px;
}
div[data-testid="stForm"]:has(.results-card-title) {
  max-width: 920px;
}
div[data-testid="stForm"] .results-card-title {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 12px;
}
div[data-testid="stForm"] [data-testid="stSelectbox"],
div[data-testid="stForm"] [data-testid="stDateInput"] {
  max-width: 540px;
  width: 100%;
}
div[data-testid="stForm"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stForm"] [data-testid="stDateInput"] input {
  background: #ffffff !important;
  color: #0f172a !important;
}
div[data-testid="stForm"] [data-testid="stSelectbox"] span,
div[data-testid="stForm"] [data-testid="stDateInput"] input::placeholder {
  color: #0f172a !important;
}

/* Input fields: white background, dark text */
.stApp .main [data-testid="stTextInput"] input,
.stApp .main [data-testid="stTextArea"] textarea,
.stApp .main [data-testid="stDateInput"] input,
.stApp .main [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: #ffffff !important;
  color: #0f172a !important;
  border: 1px solid #e2e8f0 !important;
}
.stApp .main [data-testid="stSelectbox"] div[data-baseweb="select"] span {
  color: #0f172a !important;
}
.stApp .main [data-testid="stSelectbox"] svg {
  color: #0f172a !important;
}
.stApp .main input::placeholder,
.stApp .main textarea::placeholder {
  color: #94a3b8 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

if st.session_state.get("bloodwork_reset_pending"):
    for key in list(st.session_state.keys()):
        if key.startswith("bloodwork_value_"):
            st.session_state.pop(key, None)
    st.session_state.pop("bloodwork_signature", None)
    st.session_state.pop("bloodwork_notes", None)
    st.session_state.bloodwork_step = "select"
    st.session_state.bloodwork_patient_id = None
    st.session_state.bloodwork_panel_key = None
    st.session_state.bloodwork_test_date = date.today()
    st.session_state.bloodwork_draft_id = None
    st.session_state.bloodwork_reset_pending = False

if "bloodwork_step" not in st.session_state:
    st.session_state.bloodwork_step = "select"
if "bloodwork_patient_id" not in st.session_state:
    st.session_state.bloodwork_patient_id = None
if "bloodwork_panel_key" not in st.session_state:
    st.session_state.bloodwork_panel_key = None
if "bloodwork_test_date" not in st.session_state:
    st.session_state.bloodwork_test_date = date.today()
if "bloodwork_draft_id" not in st.session_state:
    st.session_state.bloodwork_draft_id = None
if "bloodwork_signature" not in st.session_state:
    st.session_state.bloodwork_signature = ""
if "bloodwork_notes" not in st.session_state:
    st.session_state.bloodwork_notes = ""


def _reset_flow() -> None:
    st.session_state.bloodwork_reset_pending = True


db = SessionLocal()
try:
    doctor_repo = DoctorRepository(db)
    patient_repo = PatientRepository(db)
    bloodwork_service = BloodworkService(db)

    user_id = st.session_state.get("user_id")
    doctor = doctor_repo.get_by_user_id(user_id) if user_id else None
    if not doctor:
        st.error("Doctor profile not found.")
        st.stop()

    patients = patient_repo.get_by_doctor_id(doctor.id)
    panels = bloodwork_service.get_panel_templates()

    hero_html = "\n".join(
        [
            '<div class="results-hero">',
            "<h2>Results Review</h2>",
            "<p>Capture lab values, confirm ranges, and publish results to the patient portal.</p>",
            "</div>",
        ]
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    if not patients:
        st.info("No patients are assigned to your care yet.")
        st.stop()

    if not panels:
        st.info("No bloodwork panels are configured.")
        st.stop()

    if st.session_state.bloodwork_step == "select":
        patient_ids = [patient.id for patient in patients]

        def patient_label(patient_id: int) -> str:
            patient = next(
                (item for item in patients if item.id == patient_id), None
            )
            if not patient:
                return str(patient_id)
            return f"{patient.id} - {patient.first_name} {patient.last_name}"

        panel_names = [panel["name"] for panel in panels]

        with st.form("results_select_form"):
            st.markdown(
                '<div class="results-card-title">Select patient and panel</div>',
                unsafe_allow_html=True,
            )
            selected_patient_id = st.selectbox(
                "Patient", patient_ids, format_func=patient_label
            )
            selected_panel_name = st.selectbox("Panel", panel_names)
            selected_date = st.date_input(
                "Test date",
                value=st.session_state.bloodwork_test_date,
                max_value=date.today(),
            )
            submitted = st.form_submit_button("Next")

        selected_panel_key = next(
            panel["key"] for panel in panels if panel["name"] == selected_panel_name
        )

        if submitted:
            if st.session_state.bloodwork_panel_key != selected_panel_key:
                for panel in panels:
                    for marker in panel.get("markers", []):
                        marker_key = marker.get("key", marker.get("name"))
                        state_key = f"bloodwork_value_{marker_key}"
                        if state_key in st.session_state:
                            st.session_state.pop(state_key)
            st.session_state.bloodwork_patient_id = selected_patient_id
            st.session_state.bloodwork_panel_key = selected_panel_key
            st.session_state.bloodwork_test_date = selected_date
            st.session_state.bloodwork_step = "enter"
            st.rerun()

    elif st.session_state.bloodwork_step == "enter":
        panel = bloodwork_service.get_panel_template(
            st.session_state.bloodwork_panel_key
        )
        patient = next(
            (item for item in patients if item.id == st.session_state.bloodwork_patient_id),
            None,
        )
        if not patient:
            st.error("Patient selection is invalid.")
            _reset_flow()
            st.rerun()

        with st.form("entry_form", enter_to_submit=False):
            st.markdown('<div class="entry-card-anchor"></div>', unsafe_allow_html=True)
            entry_summary = "\n".join(
                [
                    '<div class="entry-summary">',
                    f"<strong>Patient:</strong> <span>{escape(patient.first_name)} {escape(patient.last_name)}</span><br/>",
                    f"<strong>Panel:</strong> <span>{escape(panel.get('name', 'Panel'))}</span><br/>",
                    f"<strong>Test date:</strong> <span>{st.session_state.bloodwork_test_date.strftime('%B %d, %Y')}</span>",
                    "</div>",
                ]
            )
            st.markdown(entry_summary, unsafe_allow_html=True)
            entry_intro = "\n".join(
                [
                    '<div class="entry-card">',
                    "<h3>Enter marker values</h3>",
                    "<p>Leave a field blank if that marker was not measured in this panel.</p>",
                    "</div>",
                ]
            )
            st.markdown(entry_intro, unsafe_allow_html=True)

            head_left, head_mid, head_right = st.columns([2.1, 2.4, 1.1], gap="small")
            with head_left:
                st.markdown(
                    '<div class="entry-head"><span>Marker</span></div>',
                    unsafe_allow_html=True,
                )
            with head_mid:
                st.markdown(
                    '<div class="entry-head"><span>Reference range</span></div>',
                    unsafe_allow_html=True,
                )
            with head_right:
                st.markdown(
                    '<div class="entry-head"><span>Result</span></div>',
                    unsafe_allow_html=True,
                )

            marker_inputs: list[tuple[dict, str, str]] = []
            with st.container():
                st.markdown('<div class="entry-list-anchor"></div>', unsafe_allow_html=True)
                for marker in panel.get("markers", []):
                    marker_key = marker.get("key", marker.get("name"))
                    input_key = f"bloodwork_value_{marker_key}"
                    value_type = marker.get("value_type", "number")
                    marker_inputs.append((marker, input_key, value_type))

                    reference = marker.get("reference_range", {})
                    ref_text = ""
                    if reference.get("low") is not None and reference.get("high") is not None:
                        ref_text = f"{reference.get('low')} - {reference.get('high')}"
                    reference_note = marker.get("reference_note", "")
                    display_reference = ref_text or reference_note or "Not provided"
                    unit = marker.get("unit", "")
                    unit_text = f" ({unit})" if unit else ""

                    col_left, col_mid, col_right = st.columns([2.1, 2.4, 1.1], gap="small")
                    with col_left:
                        st.markdown(
                            f'<div class="entry-marker">{escape(marker.get("name", "Marker"))}'
                            f"{escape(unit_text)}</div>",
                            unsafe_allow_html=True,
                        )
                        if reference_note and ref_text:
                            st.caption(reference_note)
                    with col_mid:
                        st.markdown(
                            f'<div class="entry-meta">{escape(display_reference)}</div>',
                            unsafe_allow_html=True,
                        )
                    with col_right:
                        placeholder = "Enter value" if value_type == "text" else "Enter number"
                        st.text_input(
                            "Result",
                            key=input_key,
                            label_visibility="collapsed",
                            placeholder=placeholder,
                        )

            st.markdown('<div class="entry-actions-anchor"></div>', unsafe_allow_html=True)
            col_back, col_spacer, col_save = st.columns([1, 4, 1], gap="small")
            with col_back:
                back_clicked = st.form_submit_button("Back")
            with col_spacer:
                st.markdown("", unsafe_allow_html=True)
            with col_save:
                save_clicked = st.form_submit_button("Save for Review")

        if back_clicked:
            st.session_state.bloodwork_step = "select"
            st.rerun()
        if save_clicked:
            values: dict[str, float | str] = {}
            errors = []
            for marker, input_key, value_type in marker_inputs:
                marker_key = marker.get("key", marker.get("name"))
                raw_value = st.session_state.get(input_key, "").strip()
                if not raw_value:
                    continue
                if value_type == "text":
                    values[marker_key] = raw_value
                else:
                    try:
                        values[marker_key] = float(raw_value)
                    except ValueError:
                        errors.append(
                            f"Value for {marker.get('name')} must be a number."
                        )
            if errors:
                st.error("\n".join(errors))
            elif not values:
                st.error("Enter at least one value before saving for review.")
            else:
                draft = bloodwork_service.create_draft_result(
                    patient_id=patient.id,
                    panel_key=panel["key"],
                    test_date=st.session_state.bloodwork_test_date,
                    values=values,
                )
                st.session_state.bloodwork_draft_id = draft.id
                st.session_state.bloodwork_step = "review"
                st.rerun()

    elif st.session_state.bloodwork_step == "review":
        if not st.session_state.bloodwork_draft_id:
            st.error("No draft result to review.")
            _reset_flow()
            st.rerun()

        bloodwork = bloodwork_service.bloodwork_repo.get_by_id(
            st.session_state.bloodwork_draft_id
        )
        if not bloodwork:
            st.error("Draft result not found.")
            _reset_flow()
            st.rerun()

        normalized = bloodwork_service.normalize_bloodwork(bloodwork)
        categories = normalized.get("categories", [])
        category = categories[0] if categories else {"markers": []}

        review_summary = "\n".join(
            [
                '<div class="results-summary">',
                f"<strong>Panel:</strong> <span>{escape(normalized.get('test_name', bloodwork.test_type))}</span><br/>",
                f"<strong>Test date:</strong> <span>{bloodwork.test_date.strftime('%B %d, %Y')}</span>",
                "</div>",
            ]
        )
        st.markdown(review_summary, unsafe_allow_html=True)
        st.markdown('<div class="results-section">Review captured values</div>', unsafe_allow_html=True)

        for marker in category.get("markers", []):
            marker_name = escape(marker.get("name", "Marker"))
            unit = marker.get("unit", "")
            unit_text = f" {escape(unit)}" if unit else ""
            value = marker.get("value")
            if not bloodwork_service._has_value(value):
                continue
            reference = marker.get("reference_range") or {}
            ref_text = ""
            if reference.get("low") is not None and reference.get("high") is not None:
                ref_text = f"{reference.get('low')} - {reference.get('high')}"
            reference_note = marker.get("reference_note") or ""
            if not ref_text and reference_note:
                ref_text = reference_note
            st.markdown(
                f"- {marker_name}: {value}{unit_text} (Ref {ref_text or 'N/A'})"
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.text_input(
            "Doctor signature",
            key="bloodwork_signature",
            placeholder="Type your name",
        )
        st.text_area(
            "Notes (optional)",
            key="bloodwork_notes",
            placeholder="Add any clinical notes for the patient",
        )

        col_back, col_publish = st.columns([1, 2])
        with col_back:
            if st.button("Back to Edit"):
                st.session_state.bloodwork_step = "enter"
                st.rerun()
        with col_publish:
            if st.button("Publish Results"):
                signature = st.session_state.bloodwork_signature.strip()
                if not signature:
                    st.error("Signature is required to publish.")
                else:
                    bloodwork_service.publish_result(
                        bloodwork_id=bloodwork.id,
                        doctor_id=doctor.id,
                        signature=signature,
                        notes=st.session_state.bloodwork_notes.strip() or None,
                    )
                    st.success("Results published successfully.")
                    _reset_flow()
                    st.rerun()
finally:
    db.close()
