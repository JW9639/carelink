"""Results Review page."""

from __future__ import annotations

import streamlit as st

from app.ui.layouts.dashboard_layout import apply_dashboard_layout


if not apply_dashboard_layout("Results Review", ["doctor"]):
    st.stop()

st.markdown("### Results Review")
st.write("Content coming soon.")
