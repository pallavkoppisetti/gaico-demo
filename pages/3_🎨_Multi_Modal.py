"""Multi-Modal page - Audio and Image evaluation with consistent 2-tab structure."""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_TTS_COMPARISON, CSV_BASKETBALL, CSV_STREET_SIGNS, AUDIO_DIR, IMAGE_DIR
from utils.ui_components import display_footer
from utils.visualizations import create_radar_chart

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

st.header("🎨 Multi-Modal Evaluation Gallery")

st.markdown("""
GAICo supports evaluation of **audio** and **image** outputs using specialized perceptual metrics.
Select a modality and example to explore input data with corresponding visualizations.
""")

# ============================================================================
# Modality Selector (Outside tabs for consistency)
# ============================================================================
modality = st.radio(
    "Select Modality",
    ["🔊 Audio (TTS)", "🖼️ Images"],
    horizontal=True
)

st.divider()

# ============================================================================
# AUDIO EVALUATION
# ============================================================================
if modality == "🔊 Audio (TTS)":
    
    st.subheader("🔊 TTS Model Comparison")
    
    st.markdown("""
    Comparing different Text-to-Speech models against a reference using audio quality metrics.
    GAICo evaluates **AudioSNR** (signal-to-noise ratio) and **AudioSpectrogramDistance**.
    """)
    
    # Two-tab structure
    tab1, tab2 = st.tabs(["🎯 Input & Visualization", "📊 Scores & Analysis"])
    
    # =========================================================================
    # TAB 1: Input + Visualization
    # =========================================================================
    with tab1:
        st.markdown("### 📥 Input Data - Audio Samples")
        
        # Reference Audio
        st.markdown("**Reference Audio:** Microsoft Edge TTS (Aria)")
        ref_audio = AUDIO_DIR / "samples" / "edge_tts_aria.mp3"
        if ref_audio.exists():
            st.audio(str(ref_audio))
        else:
            st.warning("Reference audio not found")
        
        st.divider()
        
        # Generated Audio Samples
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
        
        # Visualization
        st.markdown("### 📈 GAICo Visualization")
        
        if CSV_TTS_COMPARISON.exists():
            df = pd.read_csv(CSV_TTS_COMPARISON)
            metrics = df['metric_name'].unique().tolist()
            
            # Radar chart - use larger height for better visibility
            fig_radar = create_radar_chart(
                df,
                metrics=metrics,
                title="TTS Audio Quality - Model Comparison",
                height=800
            )
            
            st.plotly_chart(fig_radar, width='stretch')
            
            st.caption("Radar chart comparing TTS models across audio quality metrics.")
        else:
            st.warning("Audio comparison data not found")
    
    # =========================================================================
    # TAB 2: Scores & Analysis
    # =========================================================================
    with tab2:
        st.markdown("### 🎯 Evaluation Scores")
        
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
            
            # Download button
            csv_data = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv_data,
                file_name="gaico_audio_evaluation.csv",
                mime="text/csv"
            )
            
            st.divider()
            
            # Metric explanations
            st.markdown("### 📖 Metric Explanations")
            
            with st.expander("**AudioSNR** (Signal-to-Noise Ratio)"):
                st.markdown("""
                - Range: 0.0 to 1.0 (normalized)
                - Higher values indicate clearer audio
                - Detects artifacts, noise, distortion
                - Threshold: 0.5 (50% quality)
                """)
            
            with st.expander("**AudioSpectrogramDistance**"):
                st.markdown("""
                - Range: 0.0 to 1.0
                - Higher values indicate more similar spectrograms
                - Compares timbre, pitch, frequency content
                - Threshold: 0.5 (50% similarity)
                """)
        else:
            st.error("Audio comparison CSV not found")

# ============================================================================
# IMAGE EVALUATION
# ============================================================================
else:
    
    st.subheader("🖼️ Image Generation Evaluation")
    
    # Image example selector
    image_example = st.selectbox(
        "Select Example",
        ["Street Signs", "Basketball Team"],
        key="image_example"
    )
    
    st.markdown("""
    Comparing AI-generated images against reference images using perceptual quality metrics.
    """)
    
    # Set csv_path and title based on selected example (must be outside tabs)
    if image_example == "Street Signs":
        csv_path = CSV_STREET_SIGNS
        title = "Street Signs Image Quality"
    else:
        csv_path = CSV_BASKETBALL
        title = "Basketball Team Image Quality"
    
    # Two-tab structure
    tab1, tab2 = st.tabs(["🎯 Input & Visualization", "📊 Scores & Analysis"])
    
    # =========================================================================
    # TAB 1: Input + Visualization
    # =========================================================================
    with tab1:
        
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
        
        # Visualization
        st.markdown("### 📈 GAICo Visualization")
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            metrics = df['metric_name'].unique().tolist()
            
            # Radar chart - use larger height for better visibility
            fig_radar = create_radar_chart(
                df,
                metrics=metrics,
                title=f"{title} - Model Comparison",
                height=800
            )
            
            st.plotly_chart(fig_radar, width='stretch')
            
            st.caption(f"Radar chart comparing models on {title.lower()} metrics.")
        else:
            st.warning("Image evaluation data not found")
    
    # =========================================================================
    # TAB 2: Scores & Analysis
    # =========================================================================
    with tab2:
        st.markdown("### 🎯 Evaluation Scores")
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            
            df_display = df[['model_name', 'metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
            df_display['score'] = df_display['score'].round(4)
            df_display['passed_threshold'] = df_display['passed_threshold'].apply(
                lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
            )
            df_display.columns = ['Model', 'Metric', 'Score', 'Result', 'Threshold']
            
            st.dataframe(df_display, width='stretch', hide_index=True)
            
            # Download button
            csv_data = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv_data,
                file_name=f"gaico_image_{image_example.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
            
            st.divider()
            
            # Metric explanations
            st.markdown("### 📖 Metric Explanations")
            
            with st.expander("**ImageSSIM** (Structural Similarity)"):
                st.markdown("""
                - Range: 0.0 to 1.0
                - Higher is better
                - Measures structural similarity
                - Sensitive to luminance, contrast, structure
                """)
            
            with st.expander("**ImageAverageHash** (Perceptual Hash)"):
                st.markdown("""
                - Range: 0.0 to 1.0
                - Higher is better
                - Compares image fingerprints
                - Robust to minor changes
                """)
            
            with st.expander("**ImageHistogramMatch**"):
                st.markdown("""
                - Range: 0.0 to 1.0
                - Higher is better
                - Compares color distributions
                - Detects color/tone differences
                """)
        else:
            st.warning("CSV not found")

display_footer()
