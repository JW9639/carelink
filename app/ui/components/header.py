"""Application header component."""

from __future__ import annotations

import streamlit as st


def render_app_header(show_subtitle: bool = False) -> None:
    """Render the CareLink application header.
    
    Args:
        show_subtitle: If True, shows "Secure Healthcare Portal" subtitle (login page only)
    """
    if show_subtitle:
        st.markdown(
            """
            <div class="app-header">
                <div class="header-brand">
                    <div class="header-logo">CL</div>
                    <h1 class="header-title">CARELINK</h1>
                </div>
                <p class="header-subtitle">Secure Healthcare Portal</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="app-header">
                <div class="header-brand">
                    <div class="header-logo">CL</div>
                    <h1 class="header-title">CARELINK</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
