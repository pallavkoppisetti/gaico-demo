"""Travel Assistant page - AI Travel Assistant evaluation with consistent 2-tab structure."""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_MODALITY_QUALITY, CSV_PLAN_COHERENCE, CASE_STUDY_DIR
from utils.ui_components import display_footer
# Metric descriptions are handled inline
from utils.visualizations import display_case_study_plots

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

st.header("E2: AI Travel Assistant")

st.markdown("""
This case study demonstrates GAICo's ability to evaluate **composite AI systems**—pipelines where 
an orchestrator LLM coordinates specialist models for image and audio generation. Each pipeline 
generates a 3-day Paris itinerary including: text descriptions, structured action sequences, 
image prompts for text-to-image models, and scripts for TTS. GAICo evaluates both 
**modality quality** (how well specialist models perform) and **plan coherence** (how accurately 
the orchestrator produces structured outputs).
""")

# ============================================================================
# Pipeline Selector (Outside tabs for consistency)
# ============================================================================
st.markdown("""
| Component | Description |
|-----------|-------------|
| **📥 GAICo Inputs** | Multi-modal outputs from each pipeline: text itinerary, activity sequence, image prompt, and audio script |
| **📤 GAICo Outputs** | Cross-modality metrics comparing each pipeline's outputs against the reference |
| **🎯 What this shows** | How GAICo can evaluate complex AI systems that produce multiple output types simultaneously |

**You are selecting:** An AI pipeline configuration (combination of LLM + image generator) and a day of the itinerary.
""")

examples_dir = CASE_STUDY_DIR / "examples"

pipelines = {
    "Reference": examples_dir / "reference.json",
    "Pipeline A (GPT-5 + DALL-E 3)": examples_dir / "pipeline_A.json",
    "Pipeline B (Llama 4 + SDXL)": examples_dir / "pipeline_B.json",
    "Pipeline C (Gemini 2.5 Pro + Imagen)": examples_dir / "pipeline_C.json"
}

selected_pipeline = st.selectbox(
    "Select Pipeline",
    list(pipelines.keys()),
    help="Choose a travel assistant pipeline to evaluate"
)

json_path = pipelines[selected_pipeline]
if not json_path.exists():
    st.error(f"Pipeline data not found: {json_path}")
    st.stop()

with open(json_path, 'r') as f:
    data = json.load(f)

# Day selector
selected_day = st.radio("Select Day", [1, 2, 3], horizontal=True, help="Choose which day of the itinerary to view")
day_data = data["trip_plan"][selected_day - 1]

st.markdown("""
<div style="text-align: center; background-color: #f8f9fa; padding: 0.75rem 1rem; border-radius: 0.5rem; margin: 1rem 0;">
    <strong>The output of GAICo evaluation is below.</strong> Use the tabs to switch between: (1) viewing inputs & visualization, or (2) detailed scores & analysis.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# Two-Tab Structure: Input+Viz | Scores+Details
# ============================================================================
tab1, tab2 = st.tabs(["📥 Input & Visualization", "📤 Scores & Analysis"])

# ============================================================================
# TAB 1: Input Data + Visualization (The Hook)
# ============================================================================
with tab1:
    st.subheader(f"{selected_pipeline} - Day {selected_day}")
    
    st.markdown("""
    Each pipeline generates a 3-day Paris itinerary with structured output including:
    day plan text, activity sequence, budget, image prompt, and audio script.
    """)

    
    # -------------------------------------------------------------------------
    # Input Section: Trip Planning Data
    # -------------------------------------------------------------------------
    st.markdown("### Input Data")
    
    # Day Plan Text
    st.markdown("**Day Plan**")
    st.markdown(
        f'<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;">{day_data["day_plan_text"]}</div>',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Activity Sequence**")
        st.markdown(
            f'<div style="background-color: #e8f4f8; padding: 0.75rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.85rem;">{day_data["day_plan_sequence"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(f"**Budget:** €{day_data['day_budget_euros']}")
    
    with col2:
        st.markdown("**Image Prompt**")
        st.markdown(
            f'<div style="background-color: #fef3c7; padding: 0.75rem; border-radius: 0.5rem; font-size: 0.85rem;">{day_data["image_prompt"]}</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("**Audio Script**")
    st.markdown(
        f'<div style="background-color: #e8f8e8; padding: 0.75rem; border-radius: 0.5rem;">{day_data["audio_script"]}</div>',
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Visualization Section
    # -------------------------------------------------------------------------
    st.markdown("### GAICo Visualization")
    
    viz_type = st.radio(
        "Visualization Type",
        ["Radar Charts", "Bar Charts"],
        horizontal=True,
        key="viz_tab1"
    )
    
    if viz_type == "Radar Charts":
        display_case_study_plots(plot_type="radar")
    else:
        display_case_study_plots(plot_type="bars")

# ============================================================================
# TAB 2: Scores, Analysis & Metric Explanations
# ============================================================================
with tab2:
    st.subheader(f"Detailed Analysis: {selected_pipeline}")
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Evaluation Results
    # -------------------------------------------------------------------------
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Modality Generation Quality")
        
        if CSV_MODALITY_QUALITY.exists():
            df_modality = pd.read_csv(CSV_MODALITY_QUALITY)
            st.dataframe(df_modality, width='stretch', hide_index=True)
            
            # Download button
            csv_data = df_modality.to_csv(index=False)
            st.download_button(
                label="📥 Download (CSV)",
                data=csv_data,
                file_name="gaico_modality_quality.csv",
                mime="text/csv",
                key="download_modality"
            )
        else:
            st.error("Modality quality CSV not found")
    
    with col2:
        st.markdown("### Plan Coherence")
        
        if CSV_PLAN_COHERENCE.exists():
            df_plan = pd.read_csv(CSV_PLAN_COHERENCE)
            st.dataframe(df_plan, width='stretch', hide_index=True)
            
            # Download button
            csv_data = df_plan.to_csv(index=False)
            st.download_button(
                label="📥 Download (CSV)",
                data=csv_data,
                file_name="gaico_plan_coherence.csv",
                mime="text/csv",
                key="download_plan"
            )
        else:
            st.error("Plan coherence CSV not found")
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Metric Explanations
    # -------------------------------------------------------------------------
    st.markdown("### Metric Explanations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Modality Quality Metrics:**")
        
        with st.expander("**ImageSSIM** (Structural Similarity)"):
            st.markdown("""
            - Measures structural similarity of generated images
            - Range: 0.0 to 1.0 (higher is better)
            - Detects changes in luminance, contrast, structure
            """)
        
        with st.expander("**AudioSNR** (Signal-to-Noise Ratio)"):
            st.markdown("""
            - Measures audio clarity and quality
            - Range: 0.0 to 1.0 (higher is better)
            - Detects noise, artifacts, distortion
            """)
    
    with col2:
        st.markdown("**Plan Coherence Metrics:**")
        
        with st.expander("**BERTScore** (Semantic Similarity)"):
            st.markdown("""
            - Measures meaning preservation in text
            - Range: 0.0 to 1.0 (higher is better)
            - Uses contextual embeddings
            """)
        
        with st.expander("**PlanningLCS** (Longest Common Subsequence)"):
            st.markdown("""
            - Measures sequence ordering correctness
            - Range: 0.0 to 1.0 (higher is better)
            - Preserves temporal dependencies
            """)
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # About This Evaluation
    # -------------------------------------------------------------------------
    with st.expander("ℹ️ Evaluation Methodology"):
        st.markdown("""
        **Pipeline Configurations:**
        - **Reference**: GPT-5 + DALL-E 3 + Kokoro TTS
        - **Pipeline A**: Same as reference (baseline)
        - **Pipeline B**: Llama 4 + Stable Diffusion XL + Google TTS
        - **Pipeline C**: Gemini 2.5 Pro + Imagen + Google TTS
        
        **Two-Tier Evaluation:**
        1. **Modality Quality**: Image (SSIM, Hash) + Audio (SNR, Spectrogram)
        2. **Plan Coherence**: Text (BERTScore, ROUGE) + Planning (LCS, Jaccard, DTW)
        
        **Key Insight:** 
        GAICo distinguishes orchestrator LLM failures from specialist model deficiencies.
        This is critical for debugging composite AI systems where multiple models interact.
        """)

display_footer()
