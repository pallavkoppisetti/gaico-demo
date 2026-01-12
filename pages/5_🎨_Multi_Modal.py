"""Multi-Modal page - Audio and Image evaluation gallery."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_TTS_COMPARISON, CSV_BASKETBALL, CSV_STREET_SIGNS, AUDIO_DIR, IMAGE_DIR
from utils.ui_components import display_header, display_sidebar_links, display_footer

st.set_page_config(page_title="GAICo Demo - Multi-Modal", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()

st.header("🎨 Multi-Modal Evaluation Gallery")

tab1, tab2 = st.tabs(["🔊 Audio Evaluation", "🖼️ Image Evaluation"])

with tab1:
    st.subheader("TTS Model Comparison")
    
    st.markdown("""
    Comparing different Text-to-Speech models using audio quality metrics.
    GAICo evaluates **AudioSNR** (signal-to-noise ratio) and **AudioSpectrogramDistance**.
    """)
    
    st.markdown("### 🎵 Listen to TTS Samples")
    
    audio_samples = {
        "Edge TTS (Aria)": AUDIO_DIR / "samples" / "edge_tts_aria.mp3",
        "Edge TTS (Guy)": AUDIO_DIR / "samples" / "edge_tts_guy.mp3",
        "Google TTS": AUDIO_DIR / "samples" / "gtts_output.mp3",
        "Synthetic (Poor)": AUDIO_DIR / "samples" / "synthetic_poor_tts.wav"
    }
    
    cols = st.columns(2)
    for idx, (name, path) in enumerate(audio_samples.items()):
        with cols[idx % 2]:
            st.markdown(f"**{name}**")
            if path.exists():
                st.audio(str(path))
            else:
                st.warning("Audio file not found")
    
    st.divider()
    
    st.markdown("### 📊 Evaluation Results")
    
    if CSV_TTS_COMPARISON.exists():
        df_audio = pd.read_csv(CSV_TTS_COMPARISON)
        st.dataframe(df_audio, width="stretch", hide_index=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **AudioSNR** (Signal-to-Noise Ratio)  
            - Range: 0.0 to 1.0 (normalized)
            - Higher values indicate clearer audio
            - Detects artifacts, noise, distortion
            """)
        
        with col2:
            st.markdown("""
            **AudioSpectrogramDistance**  
            - Range: 0.0 to 1.0
            - Lower values indicate more similar spectrograms
            - Compares timbre, pitch, frequency content
            """)
    else:
        st.error("Audio comparison CSV not found")

with tab2:
    st.subheader("Image Generation Evaluation")
    
    st.markdown("""
    Comparing generated images against reference images using perceptual quality metrics.
    """)
    
    # Street Signs
    st.markdown("### 🚦 Street Signs Comparison")
    
    street_images = {
        "Reference": IMAGE_DIR / "samples" / "street-sign" / "street-sign.png",
        "Gemini": IMAGE_DIR / "samples" / "street-sign" / "street-sign_gemini.png",
        "GPT": IMAGE_DIR / "samples" / "street-sign" / "street-sign_gpt.png"
    }
    
    cols = st.columns(3)
    for idx, (name, path) in enumerate(street_images.items()):
        with cols[idx]:
            st.markdown(f"**{name}**")
            if path.exists():
                st.image(str(path))
            else:
                st.warning("Not found")
    
    st.divider()
    
    # Basketball Team
    st.markdown("### 🏀 Basketball Team Comparison")
    
    team_images = {
        "Reference": IMAGE_DIR / "samples" / "team" / "team.png",
        "Gemini": IMAGE_DIR / "samples" / "team" / "team_gemini.png",
        "GPT": IMAGE_DIR / "samples" / "team" / "team_gpt.png"
    }
    
    cols = st.columns(3)
    for idx, (name, path) in enumerate(team_images.items()):
        with cols[idx]:
            st.markdown(f"**{name}**")
            if path.exists():
                st.image(str(path))
            else:
                st.warning("Not found")
    
    st.divider()
    
    st.markdown("### 📊 Evaluation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏀 Basketball Team")
        if CSV_BASKETBALL.exists():
            df = pd.read_csv(CSV_BASKETBALL)
            st.dataframe(df, width="stretch", hide_index=True)
        else:
            st.warning("CSV not found")
    
    with col2:
        st.markdown("#### 🚦 Street Signs")
        if CSV_STREET_SIGNS.exists():
            df = pd.read_csv(CSV_STREET_SIGNS)
            st.dataframe(df, width="stretch", hide_index=True)
        else:
            st.warning("CSV not found")

display_footer()
