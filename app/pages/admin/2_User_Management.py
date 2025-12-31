"""User Management page."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("User Management", ["admin"]):
    st.stop()

st.markdown("### User Management")
st.write("Content coming soon.")
