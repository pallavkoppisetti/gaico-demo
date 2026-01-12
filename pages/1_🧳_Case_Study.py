"""Case Study page - AI Travel Assistant evaluation."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_MODALITY_QUALITY, CSV_PLAN_COHERENCE
from utils.ui_components import display_header, display_sidebar_links, display_footer
from utils.metric_info import get_metric_description, METRIC_INFO
from utils.visualizations import display_case_study_plots

st.set_page_config(page_title="GAICo Demo - Case Study", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()

st.header("🧳 AI Travel Assistant Case Study")

st.markdown("""
This case study demonstrates GAICo's ability to evaluate **composite AI systems** that 
combine multiple specialist models. We evaluate 3 different travel assistant pipelines 
that generate itineraries, images, and audio descriptions.
""")

tab1, tab2, tab3 = st.tabs(["📊 Visualizations", "📈 Metric Scores", "ℹ️ Methodology"])

with tab1:
    st.subheader("Radar Charts - Multi-Metric Overview")
    display_case_study_plots(plot_type="radar")
    
    st.divider()
    
    st.subheader("Bar Charts - Detailed Breakdown")
    display_case_study_plots(plot_type="bars")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Modality Generation Quality")
        if CSV_MODALITY_QUALITY.exists():
            df_modality = pd.read_csv(CSV_MODALITY_QUALITY)
            st.dataframe(df_modality, use_container_width=True, hide_index=True)
            
            st.caption("**Metrics Used:**")
            for metric in df_modality.columns[1:]:
                if metric in METRIC_INFO:
                    st.markdown(f"- **{metric}**: {get_metric_description(metric)}")
        else:
            st.error("Modality quality CSV not found")
    
    with col2:
        st.subheader("📋 Plan Coherence")
        if CSV_PLAN_COHERENCE.exists():
            df_plan = pd.read_csv(CSV_PLAN_COHERENCE)
            st.dataframe(df_plan, use_container_width=True, hide_index=True)
            
            st.caption("**Metrics Used:**")
            for metric in df_plan.columns[1:]:
                if metric in METRIC_INFO:
                    st.markdown(f"- **{metric}**: {get_metric_description(metric)}")
        else:
            st.error("Plan coherence CSV not found")

with tab3:
    st.markdown("""
    ### Evaluation Methodology
    
    **System Under Test:**  
    Three AI Travel Assistant pipelines that generate 3-day Paris itineraries with:
    - Text planning (day-by-day activities)
    - Image generation (location visualizations)
    - Audio narration (TTS descriptions)
    
    **Pipeline Configurations:**
    - **Pipeline A**: GPT-5 + DALL-E 3 + Kokoro TTS (reference)
    - **Pipeline B**: Llama 4 + Stable Diffusion XL + Google TTS
    - **Pipeline C**: Gemini 2.5 Pro + Imagen + Google TTS
    
    **Evaluation Categories:**
    
    1. **Modality Generation Quality**  
       Evaluates fidelity of specialist models (images, audio) against reference outputs
       - *Image Metrics*: SSIM, AverageHash, HistogramMatch
       - *Audio Metrics*: AudioSNR, AudioSpectrogramDistance
    
    2. **Plan Coherence**  
       Evaluates text planning and structured output quality
       - *Text Metrics*: BERTScore F1, ROUGE-L
       - *Planning Metrics*: PlanningLCS, PlanningJaccard
       - *Time-Series*: TimeSeriesDTW (budget forecasts)
    
    **Key Insight:**  
    GAICo enables **two-tier evaluation** - distinguishing orchestrator LLM failures 
    from specialist model deficiencies, critical for debugging composite AI systems.
    """)

display_footer()
