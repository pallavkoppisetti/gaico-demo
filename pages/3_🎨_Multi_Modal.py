"""Multi-Modal page - Audio and Image evaluation gallery."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_TTS_COMPARISON, CSV_BASKETBALL, CSV_STREET_SIGNS, AUDIO_DIR, IMAGE_DIR
from utils.ui_components import display_footer
from utils.visualizations import create_single_metric_bar_chart, create_radar_chart, create_metric_bar_chart

st.header("🎨 Multi-Modal Evaluation Gallery")

st.markdown("""
GAICo supports evaluation of **audio** and **image** outputs using specialized perceptual metrics.
""")

tab1, tab2, tab3 = st.tabs(["🔊 Audio Evaluation", "🖼️ Image Evaluation", "📈 Visualizations"])

# ============================================================================
# TAB 1: Audio Evaluation
# ============================================================================
with tab1:
    st.subheader("🔊 TTS Model Comparison")
    
    st.markdown("""
    Comparing different Text-to-Speech models against a reference using audio quality metrics.
    GAICo evaluates **AudioSNR** (signal-to-noise ratio) and **AudioSpectrogramDistance**.
    """)
    
    st.divider()
    
    # Input Section
    st.markdown("### 📥 Input Data - Audio Samples")
    
    st.markdown("**Reference Audio:** Microsoft Edge TTS (Aria)")
    ref_audio = AUDIO_DIR / "samples" / "edge_tts_aria.mp3"
    if ref_audio.exists():
        st.audio(str(ref_audio))
    
    st.markdown("**Generated Audio Samples:**")
    
    audio_samples = {
        "Google TTS (Free)": AUDIO_DIR / "samples" / "gtts_output.mp3",
        "Microsoft Edge TTS (Guy)": AUDIO_DIR / "samples" / "edge_tts_guy.mp3",
        "Synthetic Poor TTS": AUDIO_DIR / "samples" / "synthetic_poor_tts.wav"
    }
    
    cols = st.columns(3)
    for idx, (name, path) in enumerate(audio_samples.items()):
        with cols[idx]:
            st.markdown(f"**{name}**")
            if path.exists():
                st.audio(str(path))
            else:
                st.warning("Not found")
    
    st.divider()
    
    # Evaluation Results
    st.markdown("### 📊 GAICo Evaluation Results")
    
    if CSV_TTS_COMPARISON.exists():
        df_audio = pd.read_csv(CSV_TTS_COMPARISON)
        
        # Format the dataframe for display
        df_display = df_audio[['model_name', 'metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
        df_display['score'] = df_display['score'].round(4)
        df_display['passed_threshold'] = df_display['passed_threshold'].apply(
            lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
        )
        df_display.columns = ['Model', 'Metric', 'Score', 'Result', 'Threshold']
        
        st.dataframe(df_display, width='stretch', hide_index=True)
        
        st.divider()
        
        # Metric explanations
        with st.expander("📖 Metric Descriptions"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **AudioSNR** (Signal-to-Noise Ratio)  
                - Range: 0.0 to 1.0 (normalized)
                - Higher values indicate clearer audio
                - Detects artifacts, noise, distortion
                - Threshold: 0.5 (50% quality)
                """)
            
            with col2:
                st.markdown("""
                **AudioSpectrogramDistance**  
                - Range: 0.0 to 1.0
                - Higher values indicate more similar spectrograms
                - Compares timbre, pitch, frequency content
                - Threshold: 0.5 (50% similarity)
                """)
    else:
        st.error("Audio comparison CSV not found")

# ============================================================================
# TAB 2: Image Evaluation
# ============================================================================
with tab2:
    st.subheader("🖼️ Image Generation Evaluation")
    
    st.markdown("""
    Comparing AI-generated images against reference images using perceptual quality metrics.
    """)
    
    image_example = st.selectbox(
        "Select Example",
        ["Street Signs", "Basketball Team"],
        key="image_example"
    )
    
    st.divider()
    
    if image_example == "Street Signs":
        st.markdown("### 📥 Input Data - Street Signs")
        
        street_images = {
            "Reference": IMAGE_DIR / "samples" / "street-sign" / "street-sign.png",
            "GPT-4 Vision": IMAGE_DIR / "samples" / "street-sign" / "street-sign_gpt.png",
            "Gemini Vision": IMAGE_DIR / "samples" / "street-sign" / "street-sign_gemini.png"
        }
        
        cols = st.columns(3)
        for idx, (name, path) in enumerate(street_images.items()):
            with cols[idx]:
                st.markdown(f"**{name}**")
                if path.exists():
                    st.image(str(path), width='stretch')
                else:
                    st.warning("Not found")
        
        st.divider()
        
        st.markdown("### 📊 GAICo Evaluation Results")
        
        if CSV_STREET_SIGNS.exists():
            df = pd.read_csv(CSV_STREET_SIGNS)
            df_display = df[['model_name', 'metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
            df_display['score'] = df_display['score'].round(4)
            df_display['passed_threshold'] = df_display['passed_threshold'].apply(
                lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
            )
            df_display.columns = ['Model', 'Metric', 'Score', 'Result', 'Threshold']
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.warning("CSV not found")
    
    else:  # Basketball Team
        st.markdown("### 📥 Input Data - Basketball Team")
        
        team_images = {
            "Reference": IMAGE_DIR / "samples" / "team" / "team.png",
            "GPT-4 Vision": IMAGE_DIR / "samples" / "team" / "team_gpt.png",
            "Gemini Vision": IMAGE_DIR / "samples" / "team" / "team_gemini.png"
        }
        
        cols = st.columns(3)
        for idx, (name, path) in enumerate(team_images.items()):
            with cols[idx]:
                st.markdown(f"**{name}**")
                if path.exists():
                    st.image(str(path), width='stretch')
                else:
                    st.warning("Not found")
        
        st.divider()
        
        st.markdown("### 📊 GAICo Evaluation Results")
        
        if CSV_BASKETBALL.exists():
            df = pd.read_csv(CSV_BASKETBALL)
            df_display = df[['model_name', 'metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
            df_display['score'] = df_display['score'].round(4)
            df_display['passed_threshold'] = df_display['passed_threshold'].apply(
                lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
            )
            df_display.columns = ['Model', 'Metric', 'Score', 'Result', 'Threshold']
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.warning("CSV not found")
    
    st.divider()
    
    # Metric explanations
    with st.expander("📖 Image Metric Descriptions"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **ImageSSIM** (Structural Similarity)  
            - Range: 0.0 to 1.0
            - Higher is better
            - Measures structural similarity
            - Sensitive to luminance, contrast, structure
            """)
        
        with col2:
            st.markdown("""
            **ImageAverageHash** (Perceptual Hash)  
            - Range: 0.0 to 1.0
            - Higher is better
            - Compares image fingerprints
            - Robust to minor changes
            """)
        
        with col3:
            st.markdown("""
            **ImageHistogramMatch**  
            - Range: 0.0 to 1.0
            - Higher is better
            - Compares color distributions
            - Detects color/tone differences
            """)

# ============================================================================
# TAB 3: Visualizations
# ============================================================================
with tab3:
    st.subheader("📈 GAICo-Generated Visualizations")
    
    st.markdown("""
    These visualizations compare model performance across multi-modal evaluation metrics.
    """)
    
    viz_type = st.radio(
        "Select Modality",
        ["Audio (TTS)", "Images (Street Signs)", "Images (Basketball Team)"],
        horizontal=True
    )
    
    st.divider()
    
    if viz_type == "Audio (TTS)" and CSV_TTS_COMPARISON.exists():
        df = pd.read_csv(CSV_TTS_COMPARISON)
        metrics = df['metric_name'].unique().tolist()
        
        # Radar chart
        st.markdown("### 📡 Multi-Metric Radar Comparison")
        fig_radar = create_radar_chart(
            df,
            metrics=metrics,
            title="TTS Audio Quality - Model Comparison"
        )
        st.plotly_chart(fig_radar, width='stretch')
        
        st.divider()
        
        # Individual bar charts
        st.markdown("### 📊 Individual Metric Comparisons")
        cols = st.columns(2)
        for idx, metric in enumerate(metrics):
            with cols[idx % 2]:
                fig = create_single_metric_bar_chart(
                    df, 
                    metric_name=metric,
                    title=f"{metric} Comparison"
                )
                st.plotly_chart(fig, width='stretch')
    
    elif viz_type == "Images (Street Signs)" and CSV_STREET_SIGNS.exists():
        df = pd.read_csv(CSV_STREET_SIGNS)
        metrics = df['metric_name'].unique().tolist()
        
        # Radar chart
        st.markdown("### 📡 Multi-Metric Radar Comparison")
        fig_radar = create_radar_chart(
            df,
            metrics=metrics,
            title="Street Signs Image Quality - Model Comparison"
        )
        st.plotly_chart(fig_radar, width='stretch')
        
        st.divider()
        
        # Individual bar charts
        st.markdown("### 📊 Individual Metric Comparisons")
        cols = st.columns(3)
        for idx, metric in enumerate(metrics):
            with cols[idx % 3]:
                fig = create_single_metric_bar_chart(
                    df, 
                    metric_name=metric,
                    title=f"{metric}"
                )
                st.plotly_chart(fig, width='stretch')
    
    elif viz_type == "Images (Basketball Team)" and CSV_BASKETBALL.exists():
        df = pd.read_csv(CSV_BASKETBALL)
        metrics = df['metric_name'].unique().tolist()
        
        # Radar chart
        st.markdown("### 📡 Multi-Metric Radar Comparison")
        fig_radar = create_radar_chart(
            df,
            metrics=metrics,
            title="Basketball Team Image Quality - Model Comparison"
        )
        st.plotly_chart(fig_radar, width='stretch')
        
        st.divider()
        
        # Individual bar charts
        st.markdown("### 📊 Individual Metric Comparisons")
        cols = st.columns(3)
        for idx, metric in enumerate(metrics):
            with cols[idx % 3]:
                fig = create_single_metric_bar_chart(
                    df, 
                    metric_name=metric,
                    title=f"{metric}"
                )
                st.plotly_chart(fig, width='stretch')
    
    else:
        st.warning("Data not available for visualization")

display_footer()
