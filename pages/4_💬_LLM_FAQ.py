"""LLM FAQ page - Multi-model comparison with various visualizations."""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_components import display_header, display_sidebar_links, display_footer
from utils.visualizations import display_llm_faq_plots

st.set_page_config(page_title="GAICo Demo - LLM FAQ", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()

st.header("💬 LLM FAQ Evaluation")

st.markdown("""
Comprehensive comparison of multiple LLMs on USC FAQ dataset using 7 different metrics.
GAICo generated radar charts, bar charts, heatmaps, and line plots for detailed analysis.
""")

plot_type = st.selectbox(
    "Select Visualization Type",
    options=["radar", "bar", "heatmaps", "line"],
    format_func=lambda x: {
        "radar": "📡 Radar Charts (Multi-Metric Overview)",
        "bar": "📊 Bar Charts (Model Comparison)",
        "heatmaps": "🔥 Heatmaps (Score Matrix)",
        "line": "📈 Line Plots (Trend Analysis)"
    }[x]
)

st.divider()

display_llm_faq_plots(plot_type=plot_type)

st.divider()

with st.expander("ℹ️ Evaluation Methodology"):
    st.markdown("""
    **Dataset:** USC FAQ - Common questions about university procedures
    
    **Models Evaluated:**
    - GPT-4, Claude 3, Llama 3, Mixtral 8x7B, Phi-3
    
    **Metrics Used:**
    - BLEU, ROUGE-L, BERTScore, Jaccard, Levenshtein, JSD
    
    **Visualization Types:**
    - Radar Charts, Bar Charts, Heatmaps, Line Plots
    """)

display_footer()
