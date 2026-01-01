"""Application header component."""

from __future__ import annotations

import streamlit as st


def render_app_header(show_subtitle: bool = False, show_menu_toggle: bool = True) -> None:
    """Render the CareLink application header.
    
    Args:
        show_subtitle: If True, shows "Secure Healthcare Portal" subtitle (login page only)
        show_menu_toggle: If True, shows the hamburger menu toggle button (default True)
    """
    menu_btn_html = ""
    js_html = ""
    
    if show_menu_toggle:
        menu_btn_html = '<div id="sidebar-toggle-btn" onclick="toggleSidebar()" role="button" tabindex="0"><span class="bar"></span><span class="bar"></span><span class="bar"></span></div>'
        js_html = """<script>
function toggleSidebar(){var b=document.getElementById('sidebar-toggle-btn');var c=document.querySelector('[data-testid="collapsedControl"] button')||document.querySelector('[data-testid="stSidebarCollapseButton"] button')||document.querySelector('button[kind="header"]');if(b)b.classList.toggle('open');if(c)c.click();}
var obs=new MutationObserver(function(m){var s=document.querySelector('[data-testid="stSidebar"]');var b=document.getElementById('sidebar-toggle-btn');if(s&&b){b.classList.toggle('open',s.getAttribute('aria-expanded')==='true');}});
setTimeout(function(){var s=document.querySelector('[data-testid="stSidebar"]');if(s){obs.observe(s,{attributes:true,attributeFilter:['aria-expanded']});var b=document.getElementById('sidebar-toggle-btn');if(b&&s.getAttribute('aria-expanded')==='true')b.classList.add('open');}},300);
</script>"""
    
    subtitle_html = ""
    if show_subtitle:
        subtitle_html = '<p class="header-subtitle">Secure Healthcare Portal</p>'
    
    # Build and render the complete header HTML in one call
    header_html = f'<div class="app-header"><div class="header-brand">{menu_btn_html}<div class="header-logo">CL</div><h1 class="header-title">CARELINK</h1></div>{subtitle_html}</div>{js_html}'
    
    st.markdown(header_html, unsafe_allow_html=True)
