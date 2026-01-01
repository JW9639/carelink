"""Application header component."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


def render_app_header(
    show_subtitle: bool = False, show_menu_toggle: bool = True
) -> None:
    """Render the CareLink application header.

    Args:
        show_subtitle: If True, shows "Secure Healthcare Portal" subtitle (login page only)
        show_menu_toggle: If True, shows the hamburger menu toggle button (default True)
    """
    menu_btn_html = ""

    if show_menu_toggle:
        menu_btn_html = '<div id="sidebar-toggle-btn" role="button" tabindex="0"><span class="bar"></span><span class="bar"></span><span class="bar"></span></div>'

    subtitle_html = ""
    if show_subtitle:
        subtitle_html = '<p class="header-subtitle">Secure Healthcare Portal</p>'

    # Build and render the header HTML
    header_html = f'<div class="app-header"><div class="header-brand">{menu_btn_html}<div class="header-logo">CL</div><h1 class="header-title">CARELINK</h1></div>{subtitle_html}</div>'

    st.markdown(header_html, unsafe_allow_html=True)

    # Inject JavaScript separately using components.html for proper execution
    if show_menu_toggle:
        js_code = """
        <script>
        (function() {
            function toggleSidebar() {
                var sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
                var btn = parent.document.getElementById('sidebar-toggle-btn');
                if (!sidebar) return;
                
                var expanded = sidebar.getAttribute('aria-expanded') === 'true';
                
                if (expanded) {
                    sidebar.setAttribute('aria-expanded', 'false');
                    if (btn) btn.classList.remove('open');
                } else {
                    sidebar.setAttribute('aria-expanded', 'true');
                    if (btn) btn.classList.add('open');
                }
            }
            
            function initSidebar() {
                var btn = parent.document.getElementById('sidebar-toggle-btn');
                var sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
                
                if (btn && !btn._listenerAttached) {
                    btn.addEventListener('click', toggleSidebar);
                    btn._listenerAttached = true;
                }
                
                if (sidebar && btn) {
                    var isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                    btn.classList.toggle('open', isExpanded);
                }
            }
            
            // Run init after a short delay to ensure DOM is ready
            setTimeout(initSidebar, 100);
            setTimeout(initSidebar, 500);
        })();
        </script>
        """
        components.html(js_code, height=0)
