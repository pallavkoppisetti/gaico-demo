"""Shared UI components for consistent styling across pages."""

import streamlit as st
from config import (
    APP_TITLE, APP_ICON, APP_SUBTITLE, CUSTOM_CSS,
    CONFERENCE, CONFERENCE_DATE, INSTITUTION,
    GITHUB_URL, PYPI_URL, DOCS_URL
)


def setup_page(title: str = None):
    """Configure page settings. Call at the top of each page."""
    st.set_page_config(
        page_title=title or APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def display_header():
    """Display the main app header."""
    st.markdown(f'<div class="main-header">{APP_ICON} GAICo Demo</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"📊 **{CONFERENCE}** | {CONFERENCE_DATE} | {INSTITUTION}")


def display_sidebar_links():
    """Display common sidebar header and links for non-home pages."""
    # GAICo header in sidebar
    st.markdown(f"### {APP_ICON} GAICo Demo")
    st.caption(APP_SUBTITLE)
    st.divider()
    
    st.markdown("### 🔗 Links")
    st.markdown(f"[📦 GitHub]({GITHUB_URL})")
    st.markdown(f"[🐍 PyPI]({PYPI_URL})")
    st.markdown(f"[📚 Docs]({DOCS_URL})")
    st.divider()
    st.caption(f"📅 {CONFERENCE}")
    st.caption(f"🏛️ {INSTITUTION}")


def display_footer():
    """Display the page footer."""
    st.divider()
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>GAICo Demo</strong> | {INSTITUTION} | {CONFERENCE}</p>
    </div>
    """, unsafe_allow_html=True)
