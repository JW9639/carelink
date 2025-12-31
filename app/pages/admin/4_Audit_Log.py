"""Audit Log page."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Audit Log", ["admin"]):
    st.stop()

st.markdown("### Audit Log")
st.write("Content coming soon.")
