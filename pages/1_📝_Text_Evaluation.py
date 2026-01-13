"""Text Evaluation page - LLM response comparison."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TEXT_DIR, ASSETS_DIR
from utils.ui_components import display_footer
from utils.data_loader import load_text_examples
from utils.metric_info import get_metric_description, METRIC_INFO
from utils.visualizations import display_plot, create_single_metric_bar_chart

st.header("📝 Text Evaluation Examples")

text_data = load_text_examples()

if not text_data or "examples" not in text_data:
    st.error("Text examples not found. Check data/text_examples.json")
    st.stop()

st.markdown("""
These examples demonstrate GAICo's text evaluation capabilities using real LLM outputs 
from production use cases.
""")

tab1, tab2 = st.tabs(["📊 Example Comparison", "📈 Visualizations"])

# ============================================================================
# TAB 1: Example Comparison
# ============================================================================
with tab1:
    # Example selector
    example_names = {ex["id"]: ex["name"] for ex in text_data["examples"]}
    selected_id = st.selectbox(
        "Select Example",
        options=list(example_names.keys()),
        format_func=lambda x: example_names[x]
    )
    
    example = next((ex for ex in text_data["examples"] if ex["id"] == selected_id), None)
    
    if not example:
        st.error("Example not found")
        st.stop()
    
    st.divider()
    
    # Display example details
    st.subheader(example["name"])
    st.markdown(example["description"])
    
    if "question" in example.get("metadata", {}):
        st.info(f"**Question:** {example['metadata']['question']}")
    
    st.divider()
    
    # ============================================================================
    # Input Section: Reference & Generated
    # ============================================================================
    st.markdown("### 📥 Input Data")
    
    col1, col2 = st.columns(2)
    
    def format_text(text):
        """Format text for display - convert escape sequences to actual formatting."""
        if text:
            # Convert literal \n to actual newlines
            text = text.replace('\\n', '\n')
            # Convert literal \t to actual tabs
            text = text.replace('\\t', '\t')
        return text
    
    with col1:
        st.markdown("**Reference**")
        st.caption(f"📌 Model: {example['reference']['model']} | Words: {example['reference']['word_count']}")
        formatted_ref = format_text(example['reference']['text'])
        st.markdown(
            f'<div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; max-height: 400px; overflow-y: auto; white-space: pre-wrap; font-size: 0.9rem;">{formatted_ref}</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("**Generated**")
        st.caption(f"📌 Model: {example['generated']['model']} | Words: {example['generated']['word_count']}")
        formatted_gen = format_text(example['generated']['text'])
        st.markdown(
            f'<div style="background-color: #e8f8e8; padding: 1rem; border-radius: 0.5rem; max-height: 400px; overflow-y: auto; white-space: pre-wrap; font-size: 0.9rem;">{formatted_gen}</div>',
            unsafe_allow_html=True
        )
    
    st.divider()
    
    # ============================================================================
    # Evaluation Results Section
    # ============================================================================
    st.markdown("### 📊 GAICo Evaluation Results")
    
    metrics = example.get("metrics", {})
    
    if metrics:
        # Display as metric cards
        cols = st.columns(min(len(metrics), 4))
        for idx, (metric_name, score) in enumerate(metrics.items()):
            with cols[idx % len(cols)]:
                st.metric(
                    label=metric_name,
                    value=f"{score:.3f}",
                    help=get_metric_description(metric_name)
                )
        
        st.divider()
        
        # Metric descriptions
        with st.expander("📖 Metric Descriptions"):
            for metric_name in metrics.keys():
                if metric_name in METRIC_INFO:
                    info = METRIC_INFO[metric_name]
                    st.markdown(f"""
                    **{info['name']}** (`{metric_name}`)  
                    *{info['description']}*  
                    Range: {info['range']} | {info['interpretation']}
                    """)
                else:
                    st.markdown(f"**{metric_name}**: Score = {metrics[metric_name]:.3f}")
    else:
        st.warning("No metrics available for this example")

# ============================================================================
# TAB 2: Visualizations
# ============================================================================
with tab2:
    st.subheader("📈 GAICo-Generated Visualizations")
    
    st.markdown("""
    This visualization shows the Jaccard similarity scores for election Q&A responses 
    from multiple AI models evaluated against ground truth answers.
    """)
    
    # Display the static plot from GAICo
    election_plot = ASSETS_DIR / "plots" / "text" / "election_radar_plot.png"
    if election_plot.exists():
        display_plot(str(election_plot), caption="Jaccard Similarity: Election QA Model Comparison")
    else:
        st.warning("Election comparison plot not found")
    
    st.divider()
    
    # Also load and display the evaluation table if available
    election_csv = TEXT_DIR / "election_evaluation_table.csv"
    if election_csv.exists():
        st.markdown("### 📊 Detailed Evaluation Table")
        df = pd.read_csv(election_csv)
        st.dataframe(df, width='stretch', hide_index=True)
    
    with st.expander("ℹ️ About This Evaluation"):
        st.markdown("""
        **Dataset:** South Carolina Election Data (April 2022)
        
        **Models Compared:**
        - ChatGPT-4o
        - Gemini 2.5 Flash
        - SafeChat (baseline)
        
        **Metric Used:**
        - **Jaccard Similarity**: Measures token-level overlap between model responses and ground truth
        
        **How It Works:**
        1. Each model answers election-related questions
        2. GAICo computes Jaccard similarity against reference answers
        3. Results are aggregated and visualized for comparison
        """)

display_footer()
