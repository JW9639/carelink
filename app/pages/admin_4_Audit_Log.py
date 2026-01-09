"""Audit Log page."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout
from app.ui.components.page_header import render_page_header


if not apply_dashboard_layout("Audit Log", ["admin"]):
    st.stop()

render_page_header("Audit Log", "Review and filter audited actions.")
st.write("Content coming soon.")
