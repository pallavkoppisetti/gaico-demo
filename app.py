"""
GAICo Streamlit Demo - Main Entry Point (Router)
Run with: streamlit run app.py

Uses st.Page and st.navigation with custom sidebar for full control.
"""

import streamlit as st
from config import (
    APP_TITLE, APP_ICON, APP_SUBTITLE,
    CONFERENCE, INSTITUTION,
    GITHUB_URL, PYPI_URL, DOCS_URL
)

# Set page config first
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define all pages with custom labels
home_page = st.Page(
    "pages/0_🏠_Home.py",
    title="Home",
    icon="🏠",
    default=True
)

text_page = st.Page(
    "pages/1_Text_Evaluation.py",
    title="Text Evaluation"
)

structured_page = st.Page(
    "pages/2_Structured_Data.py",
    title="Structured Data"
)

multimodal_page = st.Page(
    "pages/3_Multi_Modal.py",
    title="Multi-Modal"
)

llm_faq_page = st.Page(
    "pages/4_LLM_FAQ.py",
    title="E1: LLM FAQ"
)

travel_page = st.Page(
    "pages/5_Travel_Assistant.py",
    title="E2: Travel Assistant"
)

# Set up navigation with hidden default menu (we'll build our own)
pg = st.navigation(
    {
        "": [home_page],
        "Use Cases": [text_page, structured_page, multimodal_page, llm_faq_page, travel_page]
    },
    position="hidden"
)

# Build custom sidebar
with st.sidebar:
    # Show GAICo header ONLY on non-home pages (at the very top)
    if pg != home_page:
        st.markdown(f"### {APP_ICON} GAICo Demo")
        st.caption(APP_SUBTITLE)
        st.divider()
    
    # Custom navigation menu
    st.page_link(home_page, label="Home", icon="🏠")
    
    st.markdown("**Use Cases**")
    st.page_link(text_page, label="Text Evaluation")
    st.page_link(structured_page, label="Structured Data")
    st.page_link(multimodal_page, label="Multi-Modal")
    st.page_link(llm_faq_page, label="E1: LLM FAQ")
    st.page_link(travel_page, label="E2: Travel Assistant")
    
    st.divider()
    
    # Links section
    st.markdown("### Links")
    st.markdown(f"[GitHub]({GITHUB_URL})")
    st.markdown(f"[PyPI]({PYPI_URL})")
    st.markdown(f"[Docs]({DOCS_URL})")
    st.markdown("[Demo Paper](https://ai4society.github.io/publications/papers_local/GAICO-Demo-AAAI2026.pdf)")
    st.divider()
    st.caption(f"{CONFERENCE}")
    st.caption(f"{INSTITUTION}")

# Run the selected page
pg.run()
