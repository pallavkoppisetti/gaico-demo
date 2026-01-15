"""Travel Assistant page - AI Travel Assistant evaluation."""

import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_MODALITY_QUALITY, CSV_PLAN_COHERENCE, CASE_STUDY_DIR
from utils.ui_components import display_footer
from utils.metric_info import get_metric_description, METRIC_INFO
from utils.visualizations import display_case_study_plots

st.header("✈️ E2: AI Travel Assistant")

st.markdown("""
This case study demonstrates GAICo's ability to evaluate **composite AI systems** that 
combine multiple specialist models. We evaluate 3 different travel assistant pipelines 
that generate itineraries, images, and audio descriptions.
""")

tab1, tab2, tab3 = st.tabs(["📥 Input Data", "📊 GAICo Evaluation Results", "📈 Visualizations"])

# ============================================================================
# TAB 1: Input Data
# ============================================================================
with tab1:
    st.subheader("📥 Trip Planning Data")
    
    st.markdown("""
    Each pipeline generates a 3-day Paris itinerary with structured output including:
    - **Day plan text**: Natural language description
    - **Day plan sequence**: Structured activity sequence
    - **Budget**: Daily budget in euros
    - **Image prompt**: Prompt for image generation
    - **Audio script**: Script for TTS narration
    """)
    
    # Load the JSON files
    examples_dir = CASE_STUDY_DIR / "examples"
    
    pipelines = {
        "Reference": examples_dir / "reference.json",
        "Pipeline A (GPT-5 + DALL-E 3)": examples_dir / "pipeline_A.json",
        "Pipeline B (Llama 4 + SDXL)": examples_dir / "pipeline_B.json",
        "Pipeline C (Gemini 2.5 Pro + Imagen)": examples_dir / "pipeline_C.json"
    }
    
    selected_pipeline = st.selectbox("Select Pipeline", list(pipelines.keys()))
    
    json_path = pipelines[selected_pipeline]
    if json_path.exists():
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        selected_day = st.radio("Select Day", [1, 2, 3], horizontal=True)
        
        day_data = data["trip_plan"][selected_day - 1]
        
        st.divider()
        
        # Display day plan
        st.markdown(f"### Day {selected_day}")
        
        st.markdown("**📝 Day Plan**")
        st.markdown(
            f'<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;">{day_data["day_plan_text"]}</div>',
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Activity Sequence**")
            st.code(day_data["day_plan_sequence"], language=None)
            
            st.markdown(f"**💰 Budget:** €{day_data['day_budget_euros']}")
        
        with col2:
            st.markdown("**🎨 Image Prompt**")
            st.markdown(
                f'<div style="background-color: #e8f4f8; padding: 0.75rem; border-radius: 0.5rem; font-size: 0.85rem;">{day_data["image_prompt"]}</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("**🔊 Audio Script**")
        st.markdown(
            f'<div style="background-color: #e8f8e8; padding: 0.75rem; border-radius: 0.5rem;">{day_data["audio_script"]}</div>',
            unsafe_allow_html=True
        )
        
    else:
        st.error(f"Pipeline data not found: {json_path}")

# ============================================================================
# TAB 2: GAICo Evaluation Results
# ============================================================================
with tab2:
    st.subheader("📊 GAICo Evaluation Results")
    
    st.markdown("""
    GAICo evaluates both **modality generation quality** (images, audio) and **plan coherence** (text, structure).
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Modality Generation Quality")
        if CSV_MODALITY_QUALITY.exists():
            df_modality = pd.read_csv(CSV_MODALITY_QUALITY)
            st.dataframe(df_modality, width='stretch', hide_index=True)
            
            with st.expander("📖 Metric Descriptions"):
                for metric in df_modality.columns[1:]:
                    if metric in METRIC_INFO:
                        st.markdown(f"- **{metric}**: {get_metric_description(metric)}")
        else:
            st.error("Modality quality CSV not found")
    
    with col2:
        st.markdown("### 📋 Plan Coherence")
        if CSV_PLAN_COHERENCE.exists():
            df_plan = pd.read_csv(CSV_PLAN_COHERENCE)
            st.dataframe(df_plan, width='stretch', hide_index=True)
            
            with st.expander("📖 Metric Descriptions"):
                for metric in df_plan.columns[1:]:
                    if metric in METRIC_INFO:
                        st.markdown(f"- **{metric}**: {get_metric_description(metric)}")
        else:
            st.error("Plan coherence CSV not found")
    
    st.divider()
    
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
        
        **Key Insight:** GAICo distinguishes orchestrator LLM failures from specialist model deficiencies.
        """)

# ============================================================================
# TAB 3: Visualizations
# ============================================================================
with tab3:
    st.subheader("📈 GAICo-Generated Visualizations")
    
    st.markdown("**Radar Charts** - Multi-Metric Overview")
    display_case_study_plots(plot_type="radar")
    
    st.divider()
    
    st.markdown("**Bar Charts** - Detailed Breakdown")
    display_case_study_plots(plot_type="bars")

display_footer()
