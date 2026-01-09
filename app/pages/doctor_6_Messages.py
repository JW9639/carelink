"""Doctor message center."""

from __future__ import annotations

import streamlit as st

from app.ui.components.page_header import render_page_header
from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Message Center", ["doctor"]):
    st.stop()

render_page_header(
    "Message Center",
    "Messages from GP Admin.",
)
st.markdown("---")
st.info("Message center coming soon.")
