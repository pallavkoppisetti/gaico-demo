"""Structured Data page - Planning and time-series evaluation."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CSV_PLANNING_METRICS, CSV_TIMESERIES_METRICS
from utils.ui_components import display_footer
from utils.visualizations import create_single_metric_bar_chart, create_radar_chart

st.header("📊 Structured Data Evaluation")

st.markdown("""
GAICo evaluates structured outputs like **planning sequences** and **time-series forecasts** 
using specialized metrics that preserve temporal ordering and sequential dependencies.
""")

tab1, tab2, tab3 = st.tabs([
    "🗺️ Planning Sequences", 
    "📈 Time-Series Forecasts",
    "📊 Visualizations"
])

# ============================================================================
# TAB 1: Planning Sequences
# ============================================================================
with tab1:
    st.subheader("🗺️ Planning Sequence Evaluation")
    
    st.markdown("""
    Evaluating AI-generated action sequences against reference plans. 
    This is critical for **robotics**, **workflow automation**, and **task planning** applications.
    """)
    
    # Load planning data
    if CSV_PLANNING_METRICS.exists():
        df_planning = pd.read_csv(CSV_PLANNING_METRICS)
        
        # Get unique models
        models = df_planning['model_name'].unique().tolist()
        selected_model = st.selectbox("Select Model", models, key="planning_model")
        
        model_data = df_planning[df_planning['model_name'] == selected_model]
        
        st.divider()
        
        # Input Section
        st.markdown("### 📥 Input Data")
        
        ref_text = model_data['reference_text'].iloc[0]
        gen_text = model_data['generated_text'].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Reference Sequence**")
            st.info(ref_text)
        with col2:
            st.markdown("**Generated Sequence**")
            st.success(gen_text)
        
        st.divider()
        
        # Evaluation Results
        st.markdown("### 📊 GAICo Evaluation Results")
        
        # Display metrics as cards
        metrics_df = model_data[['metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
        metrics_df['score'] = metrics_df['score'].round(4)
        metrics_df['passed_threshold'] = metrics_df['passed_threshold'].apply(
            lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
        )
        metrics_df.columns = ['Metric', 'Score', 'Result', 'Threshold']
        
        st.dataframe(metrics_df, width='stretch', hide_index=True)
        
        # Metric cards
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
        
        # Metric explanations
        with st.expander("📖 Metric Descriptions"):
            st.markdown("""
            **PlanningLCS** (Longest Common Subsequence)
            - Measures similarity while **preserving temporal ordering**
            - Higher is better (1.0 = identical sequences)
            - Best for: Evaluating if key actions are in correct order
            
            **PlanningJaccard** (Set-based Similarity)
            - Measures overlap of actions **regardless of order**
            - Higher is better (1.0 = identical sets)
            - Best for: Evaluating action completeness
            
            **Jaccard** (Token-level)
            - Character/token-level set similarity
            - Higher is better (1.0 = identical)
            
            **Levenshtein** (Edit Distance)
            - Normalized edit distance between strings
            - Higher is better (1.0 = identical)
            """)
    else:
        st.error("Planning metrics CSV not found")

# ============================================================================
# TAB 2: Time-Series Forecasts
# ============================================================================
with tab2:
    st.subheader("📈 Time-Series Forecast Evaluation")
    
    st.markdown("""
    Evaluating AI-generated time-series predictions against ground truth.
    Critical for **financial forecasting**, **demand prediction**, and **sensor data** applications.
    """)
    
    # Load timeseries data
    if CSV_TIMESERIES_METRICS.exists():
        df_timeseries = pd.read_csv(CSV_TIMESERIES_METRICS)
        
        # Get unique models
        models = df_timeseries['model_name'].unique().tolist()
        selected_model = st.selectbox("Select Model", models, key="timeseries_model")
        
        model_data = df_timeseries[df_timeseries['model_name'] == selected_model]
        
        st.divider()
        
        # Input Section
        st.markdown("### 📥 Input Data")
        
        ref_text = model_data['reference_text'].iloc[0]
        gen_text = model_data['generated_text'].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Reference Time-Series**")
            st.info(ref_text)
        with col2:
            st.markdown("**Generated Time-Series**")
            st.success(gen_text)
        
        st.divider()
        
        # Evaluation Results
        st.markdown("### 📊 GAICo Evaluation Results")
        
        # Display metrics table
        metrics_df = model_data[['metric_name', 'score', 'passed_threshold', 'threshold_applied']].copy()
        metrics_df['score'] = metrics_df['score'].round(4)
        metrics_df['passed_threshold'] = metrics_df['passed_threshold'].apply(
            lambda x: "✅ Pass" if x == True else ("❌ Fail" if x == False else "—")
        )
        metrics_df.columns = ['Metric', 'Score', 'Result', 'Threshold']
        
        st.dataframe(metrics_df, width='stretch', hide_index=True)
        
        # Metric cards
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
        
        # Metric explanations
        with st.expander("📖 Metric Descriptions"):
            st.markdown("""
            **TimeSeriesElementDiff** (Point-by-Point)
            - Strict comparison of values at each time point
            - Higher is better (1.0 = exact match, normalized)
            - Best for: When timing must be precise
            
            **TimeSeriesDTW** (Dynamic Time Warping)
            - Allows for temporal shifts and stretching
            - Higher is better (normalized, 1.0 = perfect alignment)
            - Best for: Patterns that may be shifted in time
            
            **Jaccard** (Token-level)
            - Character/token-level set similarity
            - Higher is better (1.0 = identical)
            
            **Levenshtein** (Edit Distance)
            - Normalized edit distance between strings
            - Higher is better (1.0 = identical)
            """)
    else:
        st.error("Time-series metrics CSV not found")

# ============================================================================
# TAB 3: Visualizations
# ============================================================================
with tab3:
    st.subheader("📈 GAICo-Generated Visualizations")
    
    st.markdown("""
    These visualizations compare model performance across structured data evaluation metrics.
    """)
    
    viz_type = st.radio(
        "Select Data Type",
        ["Planning Sequences", "Time-Series Forecasts"],
        horizontal=True
    )
    
    st.divider()
    
    if viz_type == "Planning Sequences" and CSV_PLANNING_METRICS.exists():
        df = pd.read_csv(CSV_PLANNING_METRICS)
        metrics = df['metric_name'].unique().tolist()
        
        # Radar chart
        st.markdown("### 📡 Multi-Metric Radar Comparison")
        fig_radar = create_radar_chart(
            df,
            metrics=metrics,
            title="Planning Metrics - Model Comparison"
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
    
    elif viz_type == "Time-Series Forecasts" and CSV_TIMESERIES_METRICS.exists():
        df = pd.read_csv(CSV_TIMESERIES_METRICS)
        metrics = df['metric_name'].unique().tolist()
        
        # Radar chart
        st.markdown("### 📡 Multi-Metric Radar Comparison")
        fig_radar = create_radar_chart(
            df,
            metrics=metrics,
            title="Time-Series Metrics - Model Comparison"
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
    
    else:
        st.warning("Data not available for visualization")

display_footer()
