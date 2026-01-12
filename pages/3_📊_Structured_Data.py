"""Structured Data page - Planning and time-series evaluation."""

import streamlit as st
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CASE_STUDY_DIR
from utils.ui_components import display_header, display_sidebar_links, display_footer

st.set_page_config(page_title="GAICo Demo - Structured Data", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()

st.header("📊 Structured Data Evaluation")

st.markdown("""
GAICo evaluates structured outputs like planning sequences and time-series forecasts using 
specialized metrics that preserve temporal ordering and sequential dependencies.

**Below are REAL examples from the Travel Assistant Case Study.**
""")

tab1, tab2, tab3 = st.tabs([
    "📋 Actual Examples", 
    "🗺️ Planning Metrics", 
    "📈 Time-Series Metrics"
])

with tab1:
    st.subheader("Real Travel Plans Evaluated by GAICo")
    
    reference_path = CASE_STUDY_DIR / "examples" / "reference.json"
    pipeline_b_path = CASE_STUDY_DIR / "examples" / "pipeline_B.json"
    
    if not reference_path.exists():
        st.warning("JSON examples not found in data/gaico_results/case_study/examples/")
        st.stop()
    
    with open(reference_path) as f:
        reference_data = json.load(f)
    
    with open(pipeline_b_path) as f:
        pipeline_b_data = json.load(f)
    
    st.markdown("""
    These are the **actual travel plans** that GAICo evaluated. 
    Compare the reference plan (left) vs Pipeline B's generated plan (right).
    """)
    
    day_num = st.selectbox("Select Day", [1, 2, 3], format_func=lambda x: f"Day {x}")
    
    ref_day = reference_data["trip_plan"][day_num - 1]
    gen_day = pipeline_b_data["trip_plan"][day_num - 1]
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📘 Reference (Pipeline A)")
        st.markdown(f"**Day {day_num} Plan:**")
        st.write(ref_day["day_plan_text"])
        
        st.markdown("**Activity Sequence:**")
        st.code(ref_day["day_plan_sequence"], language="text")
        
        st.markdown(f"**Budget:** €{ref_day['day_budget_euros']}")
    
    with col2:
        st.markdown("### 📗 Generated (Pipeline B)")
        st.markdown(f"**Day {day_num} Plan:**")
        st.write(gen_day["day_plan_text"])
        
        st.markdown("**Activity Sequence:**")
        st.code(gen_day["day_plan_sequence"], language="text")
        
        st.markdown(f"**Budget:** €{gen_day['day_budget_euros']}")
    
    st.divider()
    
    st.markdown("### 🔍 Key Differences")
    
    ref_activities = ref_day["day_plan_sequence"].split("), ")
    gen_activities = gen_day["day_plan_sequence"].split("), ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Reference Activities", len(ref_activities))
    with col2:
        st.metric("Generated Activities", len(gen_activities))
    with col3:
        budget_diff = gen_day["day_budget_euros"] - ref_day["day_budget_euros"]
        st.metric("Budget Difference", f"€{budget_diff:+d}")
    
    st.info("""
    💡 **What GAICo Measures:**
    - **PlanningLCS**: How well the sequence order matches
    - **PlanningJaccard**: How many activities overlap (regardless of order)
    - **TimeSeriesDTW**: How similar the 3-day budget forecast is
    """)

with tab2:
    st.subheader("Travel Planning Sequence Evaluation")
    st.markdown("""
    Comparing LLM-generated travel plans using sequence alignment metrics that 
    preserve the order of activities.
    """)
    
    st.markdown("### 📖 Planning Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **PlanningLCS** (Longest Common Subsequence)  
        - Measures similarity while preserving temporal ordering
        - Higher is better (1.0 = identical sequences)
        - Use case: Evaluating if key activities are in correct order
        
        **Example:**  
        Reference: [Eiffel Tower → Louvre → Notre Dame]  
        Generated: [Louvre → Eiffel Tower → Arc de Triomphe]  
        LCS finds: [Louvre → Eiffel Tower] (2/3 = 0.67)
        """)
    
    with col2:
        st.markdown("""
        **PlanningJaccard** (Set-based Similarity)  
        - Measures overlap of activities regardless of order
        - Higher is better (1.0 = identical sets)
        - Use case: Evaluating activity completeness
        
        **Example:**  
        Reference: {Eiffel Tower, Louvre, Notre Dame}  
        Generated: {Louvre, Eiffel Tower, Arc de Triomphe}  
        Overlap: 2 activities, Union: 4 activities → 0.50
        """)
    
    st.divider()
    st.info("💡 **Key Insight**: PlanningLCS is stricter (order matters), while PlanningJaccard is more forgiving (only completeness matters)")

with tab3:
    st.subheader("Daily Budget Forecast Evaluation")
    st.markdown("""
    Comparing predicted vs actual daily spending using time-series alignment metrics.
    """)
    
    st.markdown("### 📖 Time-Series Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **TimeSeriesDTW** (Dynamic Time Warping)  
        - Allows for temporal shifts and stretching
        - Lower is better (0.0 = perfect alignment)
        - Use case: Patterns that may be shifted in time
        
        **Example:**  
        Reference: [100, 150, 200, 180, 120]  
        Generated: [90, 160, 210, 170, 115]  
        DTW aligns shifted patterns gracefully
        """)
    
    with col2:
        st.markdown("""
        **TimeSeriesElementDiff** (Point-by-Point)  
        - Strict comparison of values at each time point
        - Lower is better (0.0 = exact match)
        - Use case: When timing must be precise
        
        **Example:**  
        Reference: [100, 150, 200]  
        Generated: [95, 145, 205]  
        Avg difference: (5+5+5)/3 = 5.0
        """)
    
    st.divider()
    st.info("💡 **Key Insight**: DTW is robust to phase shifts, while ElementDiff requires exact timing")

display_footer()
