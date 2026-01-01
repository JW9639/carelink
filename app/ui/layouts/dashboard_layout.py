"""Dashboard layout helpers."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.security.session_manager import (
    check_session_timeout,
    clear_session,
    init_session_state,
    update_last_activity,
)
from app.ui.components.header import render_app_header
from app.ui.components.sidebar import render_sidebar


def load_css(filename: str) -> None:
    """Load a CSS file from the styles directory."""
    possible_paths = [
        Path(__file__).resolve().parent.parent.parent / "styles" / filename,
        Path("/app/app/styles") / filename,
    ]

    for css_path in possible_paths:
        if css_path.exists():
            try:
                css_content = css_path.read_text()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
                return
            except Exception:
                continue


def apply_dashboard_layout(page_title: str, allowed_roles: list[str]) -> bool:
    """
    Apply dashboard layout with auth checks.

    Args:
        page_title: Title displayed on the page.
        allowed_roles: Roles allowed to access the page.

    Returns:
        True if authorized; otherwise False.
    """
    st.set_page_config(
        page_title=f"CareLink - {page_title}",
        page_icon="C",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_css("main.css")
    load_css("dashboard.css")
    load_css("sidebar.css")

    init_session_state()

    # Render header with menu toggle button (enabled by default)
    render_app_header(show_subtitle=False)

    if not st.session_state.get("is_authenticated", False):
        st.warning("Please log in to access this page.")
        st.switch_page("pages/Home.py")
        return False

    if not check_session_timeout():
        st.warning("Your session has expired. Please log in again.")
        clear_session()
        st.switch_page("pages/Home.py")
        return False

    user_role = st.session_state.get("role", "")
    role_value = user_role.value if hasattr(user_role, "value") else user_role
    # Case-insensitive role comparison
    role_lower = role_value.lower() if isinstance(role_value, str) else ""
    allowed_lower = [r.lower() for r in allowed_roles]
    if role_lower not in allowed_lower:
        st.error("You do not have permission to access this page.")
        st.stop()
        return False

    update_last_activity()
    render_sidebar(str(role_value))

    return True
