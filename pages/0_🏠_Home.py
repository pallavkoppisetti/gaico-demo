"""
GAICo Streamlit Demo - Landing Page
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    APP_SUBTITLE,
    CONFERENCE, CONFERENCE_DATE, INSTITUTION,
    GITHUB_URL, PYPI_URL, DOCS_URL, CONTACT_EMAIL, STATS,
    ASSETS_DIR
)

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

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
        background: rgba(255,255,255,0.9);
        color: #667eea;
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
    
    /* Hook section */
    .hook-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 2px solid #667eea;
    }
    .hook-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    /* Acknowledgment section */
    .acknowledgment {
        background: linear-gradient(90deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 0.75rem;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid #f59e0b;
        font-size: 0.9rem;
    }
    .acknowledgment-title {
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">📊 GAICo</div>
    <div class="hero-subtitle">This app demonstrates the capabilities of GAICo:<br/>{APP_SUBTITLE}</div>
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
    👈 <strong>Use the sidebar</strong> to explore different evaluation scenarios<br/>
    <small>Each page has two tabs: <strong>Input & Visualization</strong> (see the data) and <strong>Scores & Analysis</strong> (see the results)</small>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# HOOK SECTION: Interactive Preview with DeepSeek Example
# ============================================================================
st.divider()

st.markdown("### 🔍 Try It Now: See GAICo in Action")

# Create a compelling hook with the DeepSeek example
hook_col1, hook_col2 = st.columns([3, 2])

with hook_col1:
    st.markdown("""
    <div class="hook-container">
        <div class="hook-title">Example: Comparing LLM Responses</div>
        <p style="color: #4b5563; font-size: 0.95rem; margin-bottom: 0.5rem;">
        <strong>Sample Question:</strong> <em>"How did DeepSeek train a model for $6M vs $100M for GPT-4?"</em><br/><br/>
        <strong>Inputs (what we feed to GAICo):</strong><br/>
        &bull; Two LLM responses (DeepSeek R1 and Llama 3.3) answering the same question<br/><br/>
        <strong>Outputs (what GAICo produces):</strong><br/>
        &bull; Similarity metrics comparing the responses (see radar chart →)<br/>
        &bull; Detailed scores available in the <strong>Scores & Analysis</strong> tab
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display side-by-side response snippets
    mini_col1, mini_col2 = st.columns(2)
    with mini_col1:
        st.markdown("**DeepSeek R1** (238 words)")
        st.markdown(
            '<div style="background-color: #e8f4f8; padding: 0.75rem; border-radius: 0.5rem; font-size: 0.8rem; max-height: 150px; overflow-y: auto;">'
            '<strong>Key points:</strong> Hardware optimization, simplified architecture, efficient algorithms, data efficiency, open-source utilization...'
            '</div>',
            unsafe_allow_html=True
        )
    with mini_col2:
        st.markdown("**Llama 3.3** (472 words)")
        st.markdown(
            '<div style="background-color: #e8f8e8; padding: 0.75rem; border-radius: 0.5rem; font-size: 0.8rem; max-height: 150px; overflow-y: auto;">'
            '<strong>Key points:</strong> Efficient use of existing technologies, smaller team size, innovative training methods, affordable computing resources...'
            '</div>',
            unsafe_allow_html=True
        )

with hook_col2:
    # Create a mini radar chart for the hook
    hook_metrics = {
        "BLEU": 0.42,
        "ROUGE-L": 0.58,
        "BERTScore": 0.87,
        "Jaccard": 0.35,
        "Levenshtein": 0.68
    }
    
    metrics_list = list(hook_metrics.keys())
    scores = list(hook_metrics.values())
    scores.append(scores[0])  # Close the radar
    metrics_list_closed = metrics_list + [metrics_list[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=metrics_list_closed,
        fill='toself',
        name='DeepSeek vs Llama',
        line_color='#667eea',
        line_width=3,
        fillcolor='rgba(102, 126, 234, 0.35)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1], 
                tickfont=dict(size=12, color='#4b5563'),
                gridcolor='rgba(156, 163, 175, 0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#1f2937', weight='bold'),
                gridcolor='rgba(156, 163, 175, 0.3)'
            ),
            bgcolor='rgba(248,250,252,0.5)'
        ),
        showlegend=False,
        title=dict(text="GAICo Similarity Scores", font=dict(size=18, color='#1f2937')),
        height=420,
        margin=dict(l=60, r=60, t=70, b=40),
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, width='stretch')

# Call to action
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <p style="color: #6b7280;">👆 <strong>High BERTScore (0.87)</strong> shows semantic similarity despite different styles. 
    <a href="/Text_Evaluation" target="_self" style="color: #667eea; font-weight: 600;">Explore full analysis →</a></p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Modality Cards
st.markdown("### Multi-Modal Evaluation")
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

# Stats Section
st.markdown("### GAICo by the Numbers")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("PyPI Downloads", STATS["pypi_downloads"], "Active Users")
with col2:
    st.metric("Built-in Metrics", STATS["metrics_count"], "Across 4 Modalities")
with col3:
    st.metric("Example Notebooks", STATS["notebooks_count"], "Ready to Run")

# Two column layout: Features + Quick Start
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Key Features")
    st.markdown("""
    - **15+ Built-in Metrics** — BLEU, ROUGE, BERTScore, SSIM, DTW, and more
    - **Extensible Architecture** — Easy to add custom metrics
    - **Unified API** — Same interface across all modalities
    - **Visualization Ready** — Built-in plotting functions
    - **CSV Export** — Easy result sharing and analysis
    - **Jupyter Support** — Works seamlessly in notebooks
    """)

with col2:
    st.markdown("### Quick Start")
    st.code("""from gaico import Experiment

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

# Acknowledgments
st.markdown("""
<div class="acknowledgment">
    <div class="acknowledgment-title"> Acknowledgments</div>
    This work is partially supported by <strong>NSF Awards #2454027, NAIRR250014</strong>, and <strong>Faculty Award by JP Morgan Research</strong>.
</div>
""", unsafe_allow_html=True)

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
