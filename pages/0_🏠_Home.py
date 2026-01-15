"""
GAICo Streamlit Demo - Landing Page
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    APP_SUBTITLE,
    CONFERENCE, CONFERENCE_DATE, INSTITUTION,
    GITHUB_URL, PYPI_URL, DOCS_URL, CONTACT_EMAIL, STATS,
    ASSETS_DIR
)

# Enhanced CSS for landing page
st.markdown("""
<style>
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 1rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 2rem;
        font-size: 0.95rem;
        backdrop-filter: blur(10px);
    }
    
    /* Feature cards */
    .feature-card {
        background: #f8f9fa;
        border-radius: 0.75rem;
        padding: 1.5rem;
        height: 100%;
        border-left: 4px solid #667eea;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    /* Stats section */
    .stats-container {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 1rem;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    /* CTA buttons */
    .cta-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }
    .cta-button {
        display: inline-block;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .cta-button:hover {
        transform: translateY(-2px);
    }
    .cta-primary {
        background: white;
        color: #667eea;
    }
    .cta-secondary {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid white;
    }
    
    /* Quick start code */
    .code-section {
        background: #1e1e1e;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Navigation hint */
    .nav-hint {
        background: #e0f2fe;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        margin: 2rem 0;
        border: 1px solid #7dd3fc;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">📊 GAICo</div>
    <div class="hero-subtitle">{APP_SUBTITLE}</div>
    <div class="hero-badge">🎯 {CONFERENCE} • {CONFERENCE_DATE} • {INSTITUTION}</div>
    <div class="cta-container">
        <a href="{PYPI_URL}" target="_blank" class="cta-button cta-primary">pip install gaico</a>
        <a href="{GITHUB_URL}" target="_blank" class="cta-button cta-secondary">⭐ View on GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.info("ℹ️ **Note:** This demo showcases GAICo's capabilities under fixed use cases while optimizing for response time and robustness. The library itself can be utilized for any use case.")

# Navigation hint
st.markdown("""
<div class="nav-hint">
    👈 <strong>Use the sidebar</strong> to explore different evaluation demos, or scroll down to learn more about GAICo
</div>
""", unsafe_allow_html=True)

# Modality Cards
st.markdown("### 🎨 Multi-Modal Evaluation")
st.caption("One framework for all your GenAI evaluation needs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Text</div>
        <div class="feature-desc">LLM responses, summaries, translations, Q&A</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🖼️</div>
        <div class="feature-title">Images</div>
        <div class="feature-desc">Generated images, style transfer, editing</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔊</div>
        <div class="feature-title">Audio</div>
        <div class="feature-desc">TTS synthesis, music generation, voice cloning</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Structured</div>
        <div class="feature-desc">Planning sequences, time-series, forecasts</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sample Visualization Section
st.markdown("### 📈 Sample Visualization")
st.caption("GAICo automatically generates publication-ready visualizations")

# Display the LLM FAQ radar chart as an example
radar_plot_path = ASSETS_DIR / "plots" / "llm_faq" / "radar" / "overall_radar_chart.png"
if radar_plot_path.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(radar_plot_path), caption="Multi-LLM comparison across evaluation metrics (from E1: LLM FAQ)", use_container_width=True)
else:
    st.warning("Sample visualization not found")

st.markdown("<br>", unsafe_allow_html=True)

# Stats Section
st.markdown('<div class="stats-container">', unsafe_allow_html=True)
st.markdown("### 📈 GAICo by the Numbers")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("PyPI Downloads", STATS["pypi_downloads"], "Active Users")
with col2:
    st.metric("Built-in Metrics", STATS["metrics_count"], "Across 4 Modalities")
with col3:
    st.metric("Example Notebooks", STATS["notebooks_count"], "Ready to Run")
st.markdown('</div>', unsafe_allow_html=True)

# Two column layout: Features + Quick Start
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ✨ Key Features")
    st.markdown("""
    - ✅ **15+ Built-in Metrics** — BLEU, ROUGE, BERTScore, SSIM, DTW, and more
    - ✅ **Extensible Architecture** — Easy to add custom metrics
    - ✅ **Unified API** — Same interface across all modalities
    - ✅ **Visualization Ready** — Built-in plotting functions
    - ✅ **CSV Export** — Easy result sharing and analysis
    - ✅ **Jupyter Support** — Works seamlessly in notebooks
    """)

with col2:
    st.markdown("### 🚀 Quick Start")
    st.code("""
from gaico import Experiment

exp = Experiment(
    llm_responses={
        "GPT-4": response1,
        "Claude": response2
    },
    reference_answer=ground_truth
)

results = exp.compare(plot=True)
    """, language="python")

# Footer
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>GAICo Demo</strong> • {INSTITUTION} • {CONFERENCE}</p>
        <p style='font-size: 0.85rem;'>
            <a href="{GITHUB_URL}" style="margin: 0 10px;">GitHub</a> •
            <a href="{PYPI_URL}" style="margin: 0 10px;">PyPI</a> •
            <a href="{DOCS_URL}" style="margin: 0 10px;">Documentation</a> •
            <a href="mailto:{CONTACT_EMAIL}" style="margin: 0 10px;">Contact</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
