"""Streamlit theming utilities."""

from __future__ import annotations

import textwrap

import streamlit as st


def apply_theme() -> None:
    """Inject custom CSS for the CareLink UI."""
    css = textwrap.dedent(
        """
        :root {
            --color-primary: #005eb8;
            --color-secondary: #007f3b;
            --color-bg: #f0f4f5;
            --color-text: #212b32;
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 16px;
            --space-4: 24px;
            --space-5: 32px;
            --radius: 12px;
            --shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        }

        body {
            background: var(--color-bg);
            color: var(--color-text);
            font-family: "Helvetica Neue", Arial, sans-serif;
        }

        .carelink-card {
            background: #ffffff;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: var(--space-4);
            margin-bottom: var(--space-4);
        }

        .carelink-button {
            background: linear-gradient(90deg, var(--color-primary), #003f7d);
            color: #fff;
            border: none;
            border-radius: 10px;
            padding: var(--space-2) var(--space-3);
            font-weight: 600;
        }

        .carelink-table th {
            background: var(--color-primary);
            color: #fff;
        }

        .carelink-table tr:nth-child(even) {
            background: #eef2f7;
        }
        """
    )
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
