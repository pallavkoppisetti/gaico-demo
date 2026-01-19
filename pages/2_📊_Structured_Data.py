"""Structured Data page - Planning and time-series evaluation with consistent 2-tab structure."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_PLANNING_METRICS, CSV_TIMESERIES_METRICS
from utils.ui_components import display_footer

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

st.header("📊 Structured Data Evaluation")

st.markdown("""
GAICo evaluates structured outputs like **planning sequences** and **time-series forecasts** 
using specialized metrics that preserve temporal ordering and sequential dependencies.
""")

# ============================================================================
# Data Type Selector (Outside tabs for consistency)
# ============================================================================
data_type = st.radio(
    "Select Data Type",
    ["🗺️ Planning Sequences", "📈 Time-Series Forecasts"],
    horizontal=True
)

st.divider()

# ============================================================================
# PLANNING SEQUENCES
# ============================================================================
if data_type == "🗺️ Planning Sequences":
    
    if not CSV_PLANNING_METRICS.exists():
        st.error("Planning metrics CSV not found")
        st.stop()
    
    df_planning = pd.read_csv(CSV_PLANNING_METRICS)
    models = df_planning['model_name'].unique().tolist()
    
    # Model selector
    selected_model = st.selectbox("Select Model", models, key="planning_model")
    model_data = df_planning[df_planning['model_name'] == selected_model]
    
    # Two-tab structure
    tab1, tab2 = st.tabs(["🎯 Input & Visualization", "📊 Scores & Analysis"])
    
    # =========================================================================
    # TAB 1: Input + Visualization
    # =========================================================================
    with tab1:
        st.subheader(f"Planning Evaluation: {selected_model}")
        
        st.markdown("""
        Evaluating AI-generated action sequences against reference plans. 
        Critical for **robotics**, **workflow automation**, and **task planning**.
        """)
        
        st.divider()
        
        # Input Section
        st.markdown("### 📥 Input Data")
        
        ref_text = model_data['reference_text'].iloc[0]
        gen_text = model_data['generated_text'].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Reference Sequence**")
            st.markdown(
                f'<div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.9rem;">{ref_text}</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("**Generated Sequence**")
            st.markdown(
                f'<div style="background-color: #e8f8e8; padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.9rem;">{gen_text}</div>',
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Visualization Section
        st.markdown("### 📈 GAICo Visualization")
        
        metrics = model_data['metric_name'].unique().tolist()
        
        # Create radar chart for this model
        scores = []
        for metric in metrics:
            score = model_data[model_data['metric_name'] == metric]['score'].values[0]
            scores.append(score)
        
        scores_closed = scores + [scores[0]]
        metrics_closed = metrics + [metrics[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=metrics_closed,
            fill='toself',
            name=selected_model,
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=dict(text=f"Planning Metrics: {selected_model}", font=dict(size=16)),
            height=800
        )
        
        st.plotly_chart(fig, width='stretch')
        
        st.caption("Radar chart showing performance across planning evaluation metrics.")
    
    # =========================================================================
    # TAB 2: Scores & Analysis
    # =========================================================================
    with tab2:
        st.subheader(f"📊 Detailed Analysis: {selected_model}")
        
        # Metric Score Cards
        st.markdown("### 🎯 Evaluation Scores")
        
        cols = st.columns(4)
        for idx, (_, row) in enumerate(model_data.iterrows()):
            with cols[idx % 4]:
                score = row['score']
                passed = row['passed_threshold']
                icon = "✅" if passed == True else ("❌" if passed == False else "—")
                st.metric(
                    label=row['metric_name'],
                    value=f"{score:.4f}",
                    delta=icon
                )
        
        st.divider()
        
        # CSV Report Table
        st.markdown("### 📋 Evaluation Report")
        
        metrics_df = model_data[['metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
        metrics_df['score'] = metrics_df['score'].round(4)
        metrics_df['passed_threshold'] = metrics_df['passed_threshold'].apply(
            lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
        )
        metrics_df.columns = ['Metric', 'Score', 'Result', 'Threshold']
        
        st.dataframe(metrics_df, width='stretch', hide_index=True)
        
        # Download button
        csv_data = metrics_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv_data,
            file_name=f"gaico_planning_{selected_model}.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # Metric Descriptions
        st.markdown("### 📖 Metric Explanations")
        
        with st.expander("**PlanningLCS** (Longest Common Subsequence)"):
            st.markdown("""
            - Measures similarity while **preserving temporal ordering**
            - Higher is better (1.0 = identical sequences)
            - Best for: Evaluating if key actions are in correct order
            """)
        
        with st.expander("**PlanningJaccard** (Set-based Similarity)"):
            st.markdown("""
            - Measures overlap of actions **regardless of order**
            - Higher is better (1.0 = identical sets)
            - Best for: Evaluating action completeness
            """)
        
        with st.expander("**Jaccard** (Token-level)"):
            st.markdown("""
            - Character/token-level set similarity
            - Higher is better (1.0 = identical)
            """)
        
        with st.expander("**Levenshtein** (Edit Distance)"):
            st.markdown("""
            - Normalized edit distance between strings
            - Higher is better (1.0 = identical)
            """)

# ============================================================================
# TIME-SERIES FORECASTS
# ============================================================================
else:
    
    if not CSV_TIMESERIES_METRICS.exists():
        st.error("Time-series metrics CSV not found")
        st.stop()
    
    df_timeseries = pd.read_csv(CSV_TIMESERIES_METRICS)
    models = df_timeseries['model_name'].unique().tolist()
    
    # Model selector
    selected_model = st.selectbox("Select Model", models, key="timeseries_model")
    model_data = df_timeseries[df_timeseries['model_name'] == selected_model]
    
    # Two-tab structure
    tab1, tab2 = st.tabs(["🎯 Input & Visualization", "📊 Scores & Analysis"])
    
    # =========================================================================
    # TAB 1: Input + Visualization
    # =========================================================================
    with tab1:
        st.subheader(f"Time-Series Evaluation: {selected_model}")
        
        st.markdown("""
        Evaluating AI-generated time-series predictions against ground truth.
        Critical for **financial forecasting**, **demand prediction**, and **sensor data**.
        """)
        
        st.divider()
        
        # Input Section
        st.markdown("### 📥 Input Data")
        
        ref_text = model_data['reference_text'].iloc[0]
        gen_text = model_data['generated_text'].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Reference Time-Series**")
            st.markdown(
                f'<div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.9rem;">{ref_text}</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("**Generated Time-Series**")
            st.markdown(
                f'<div style="background-color: #e8f8e8; padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.9rem;">{gen_text}</div>',
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Visualization Section
        st.markdown("### 📈 GAICo Visualization")
        
        metrics = model_data['metric_name'].unique().tolist()
        
        # Create radar chart for this model
        scores = []
        for metric in metrics:
            score = model_data[model_data['metric_name'] == metric]['score'].values[0]
            scores.append(score)
        
        scores_closed = scores + [scores[0]]
        metrics_closed = metrics + [metrics[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=metrics_closed,
            fill='toself',
            name=selected_model,
            line_color='#10b981',
            fillcolor='rgba(16, 185, 129, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=dict(text=f"Time-Series Metrics: {selected_model}", font=dict(size=16)),
            height=800
        )
        
        st.plotly_chart(fig, width='stretch')
        
        st.caption("Radar chart showing performance across time-series evaluation metrics.")
    
    # =========================================================================
    # TAB 2: Scores & Analysis
    # =========================================================================
    with tab2:
        st.subheader(f"📊 Detailed Analysis: {selected_model}")
        
        # Metric Score Cards
        st.markdown("### 🎯 Evaluation Scores")
        
        cols = st.columns(4)
        for idx, (_, row) in enumerate(model_data.iterrows()):
            with cols[idx % 4]:
                score = row['score']
                passed = row['passed_threshold']
                icon = "✅" if passed == True else ("❌" if passed == False else "—")
                st.metric(
                    label=row['metric_name'],
                    value=f"{score:.4f}",
                    delta=icon
                )
        
        st.divider()
        
        # CSV Report Table
        st.markdown("### 📋 Evaluation Report")
        
        metrics_df = model_data[['metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
        metrics_df['score'] = metrics_df['score'].round(4)
        metrics_df['passed_threshold'] = metrics_df['passed_threshold'].apply(
            lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
        )
        metrics_df.columns = ['Metric', 'Score', 'Result', 'Threshold']
        
        st.dataframe(metrics_df, width='stretch', hide_index=True)
        
        # Download button
        csv_data = metrics_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv_data,
            file_name=f"gaico_timeseries_{selected_model}.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # Metric Descriptions
        st.markdown("### 📖 Metric Explanations")
        
        with st.expander("**TimeSeriesElementDiff** (Point-by-Point)"):
            st.markdown("""
            - Strict comparison of values at each time point
            - Higher is better (1.0 = exact match, normalized)
            - Best for: When timing must be precise
            """)
        
        with st.expander("**TimeSeriesDTW** (Dynamic Time Warping)"):
            st.markdown("""
            - Allows for temporal shifts and stretching
            - Higher is better (normalized, 1.0 = perfect alignment)
            - Best for: Patterns that may be shifted in time
            """)
        
        with st.expander("**Jaccard** (Token-level)"):
            st.markdown("""
            - Character/token-level set similarity
            - Higher is better (1.0 = identical)
            """)

display_footer()
