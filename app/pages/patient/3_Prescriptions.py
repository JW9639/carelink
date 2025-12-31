"""Prescriptions page."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Prescriptions", ["patient"]):
    st.stop()

st.markdown("### Prescriptions")
st.write("Content coming soon.")
