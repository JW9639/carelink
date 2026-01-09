"""Page header component with gradient background."""

from __future__ import annotations

from html import escape

import streamlit as st


def render_page_header(title: str, subtitle: str | None = None) -> None:
    """Render a page header with a gradient background."""
    safe_title = escape(title)
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="page-hero-subtitle">{escape(subtitle)}</p>'

    st.markdown(
        f"""
        <div class="page-hero">
            <h1 class="page-hero-title">{safe_title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
