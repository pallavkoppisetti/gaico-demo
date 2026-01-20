"""Text Evaluation page - LLM response comparison with consistent 2-tab structure."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import ASSETS_DIR
from utils.ui_components import display_footer
from utils.data_loader import load_text_examples
from utils.metric_info import get_metric_description, METRIC_INFO
from utils.visualizations import display_plot

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

st.header("Text Evaluation Examples")

text_data = load_text_examples()

if not text_data or "examples" not in text_data:
    st.error("Text examples not found. Check data/text_examples.json")
    st.stop()

st.markdown("""
These examples demonstrate GAICo's text evaluation capabilities using real LLM outputs 
from production use cases. Select an example to see the input data and corresponding visualization.
""")

# ============================================================================
# Example Selector (Outside tabs for consistency)
# ============================================================================
st.markdown("##### ⚙️ Configure Evaluation")

with st.expander("ℹ️ **What am I selecting?** (Click to expand)", expanded=False):
    st.markdown("""
    **You are selecting:** A pre-configured text comparison scenario.
    
    | Component | Description |
    |-----------|-------------|
    | **📥 GAICo Inputs** | Two text responses (a *reference* answer and a *generated* answer) from different LLMs |
    | **📤 GAICo Outputs** | Similarity scores (BLEU, ROUGE, BERTScore, etc.) measuring how closely the generated text matches the reference |
    | **🎯 What this shows** | How well one LLM's response aligns with another across multiple linguistic dimensions |
    """)

example_names = {ex["id"]: ex["name"] for ex in text_data["examples"]}
selected_id = st.selectbox(
    "Select Use Case",
    options=list(example_names.keys()),
    format_func=lambda x: example_names[x],
    help="Choose a pre-configured evaluation scenario to explore"
)

example = next((ex for ex in text_data["examples"] if ex["id"] == selected_id), None)

if not example:
    st.error("Example not found")
    st.stop()

st.info("📊 **The output of GAICo evaluation is below.** Use the tabs to switch between: (1) viewing inputs & visualization, or (2) detailed scores & analysis.")

# ============================================================================
# Two-Tab Structure: Input+Viz | Scores+Details
# ============================================================================
tab1, tab2 = st.tabs(["📥 Input & Visualization", "📤 Scores & Analysis"])

# ============================================================================
# TAB 1: Input Data + Visualization (The Hook)
# ============================================================================
with tab1:
    st.subheader(example["name"])
    st.markdown(example["description"])
    
    if "question" in example.get("metadata", {}):
        st.info(f"**Question:** {example['metadata']['question']}")
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Input Section: Reference & Generated (Side by Side)
    # -------------------------------------------------------------------------
    st.markdown("### Input Data")
    
    col1, col2 = st.columns(2)
    
    def format_text(text):
        """Format text for display - convert escape sequences to actual formatting."""
        if text:
            text = text.replace('\\n', '\n')
            text = text.replace('\\t', '\t')
        return text
    
    with col1:
        st.markdown("**Reference**")
        st.caption(f"Model: {example['reference']['model']} | Words: {example['reference']['word_count']}")
        formatted_ref = format_text(example['reference']['text'])
        st.markdown(
            f'<div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; max-height: 350px; overflow-y: auto; white-space: pre-wrap; font-size: 0.85rem;">{formatted_ref}</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("**Generated**")
        st.caption(f"Model: {example['generated']['model']} | Words: {example['generated']['word_count']}")
        formatted_gen = format_text(example['generated']['text'])
        st.markdown(
            f'<div style="background-color: #e8f8e8; padding: 1rem; border-radius: 0.5rem; max-height: 350px; overflow-y: auto; white-space: pre-wrap; font-size: 0.85rem;">{formatted_gen}</div>',
            unsafe_allow_html=True
        )
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Visualization Section (Corresponding to Selected Example)
    # -------------------------------------------------------------------------
    st.markdown("### GAICo Visualization")
    
    metrics = example.get("metrics", {})
    
    if selected_id == "deepseek_cost_analysis":
        # Generate dynamic radar chart for DeepSeek example
        st.markdown("**Multi-Metric Comparison: DeepSeek R1 vs Llama 3.3**")
        
        metrics_list = list(metrics.keys())
        scores = list(metrics.values())
        
        # Create radar chart
        scores_closed = scores + [scores[0]]
        metrics_closed = metrics_list + [metrics_list[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=metrics_closed,
            fill='toself',
            name='DeepSeek R1 vs Llama 3.3',
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            showlegend=True,
            title=dict(text="GAICo Similarity Metrics", font=dict(size=16)),
            height=800,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, width='stretch')
        
        st.caption("This radar chart shows how similar the DeepSeek R1 response is to Llama 3.3 across multiple dimensions.")
        
    elif selected_id == "election_voter_registration":
        # Display the pre-generated election visualization
        st.markdown("**Election Q&A Model Comparison**")
        
        election_plot = ASSETS_DIR / "plots" / "text" / "election_radar_plot.png"
        if election_plot.exists():
            display_plot(str(election_plot), caption="Jaccard Similarity: Multi-Model Comparison on SC Election Data")
        else:
            # Fallback: Generate dynamic visualization
            st.markdown("**Metric Scores for ChatGPT-4o vs SafeChat Reference**")
            
            scores_closed = list(metrics.values()) + [list(metrics.values())[0]]
            metrics_closed = list(metrics.keys()) + [list(metrics.keys())[0]]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores_closed,
                theta=metrics_closed,
                fill='toself',
                name='ChatGPT-4o',
                line_color='#10b981',
                fillcolor='rgba(16, 185, 129, 0.3)'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                title=dict(text="GAICo Similarity Metrics", font=dict(size=16)),
                height=800
            )
            
            st.plotly_chart(fig, width='stretch')
        
        st.caption("This visualization compares AI model responses to official SC voter information on election-related questions.")
    
    else:
        # Generic fallback for any other examples
        if metrics:
            st.markdown("**Metric Scores**")
            
            scores_closed = list(metrics.values()) + [list(metrics.values())[0]]
            metrics_closed = list(metrics.keys()) + [list(metrics.keys())[0]]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores_closed,
                theta=metrics_closed,
                fill='toself',
                name='Comparison',
                line_color='#667eea',
                fillcolor='rgba(102, 126, 234, 0.3)'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                height=800
            )
            
            st.plotly_chart(fig, width='stretch')

# ============================================================================
# TAB 2: Scores, CSV Report & Metric Explanations
# ============================================================================
with tab2:
    st.subheader(f"Detailed Analysis: {example['name']}")
    
    metrics = example.get("metrics", {})
    
    if metrics:
        # -------------------------------------------------------------------------
        # Metric Score Cards
        # -------------------------------------------------------------------------
        st.markdown("### Evaluation Scores")
        
        cols = st.columns(min(len(metrics), 4))
        for idx, (metric_name, score) in enumerate(metrics.items()):
            with cols[idx % len(cols)]:
                st.metric(
                    label=metric_name,
                    value=f"{score:.3f}",
                    help=get_metric_description(metric_name)
                )
        
        st.divider()
        
        # -------------------------------------------------------------------------
        # CSV Report Table
        # -------------------------------------------------------------------------
        st.markdown("### Evaluation Report")
        
        # Create a formatted dataframe for the report
        report_data = []
        for metric_name, score in metrics.items():
            info = METRIC_INFO.get(metric_name, {})
            report_data.append({
                "Metric": metric_name,
                "Score": f"{score:.4f}",
                "Range": info.get("range", "0.0 - 1.0"),
                "Interpretation": info.get("interpretation", "Higher is better")
            })
        
        df_report = pd.DataFrame(report_data)
        st.dataframe(df_report, width='stretch', hide_index=True)
        
        # Download button for CSV
        csv_data = df_report.to_csv(index=False)
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv_data,
            file_name=f"gaico_report_{selected_id}.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # -------------------------------------------------------------------------
        # Metric Descriptions
        # -------------------------------------------------------------------------
        st.markdown("### Metric Explanations")
        
        for metric_name in metrics.keys():
            if metric_name in METRIC_INFO:
                info = METRIC_INFO[metric_name]
                with st.expander(f"**{info['name']}** (`{metric_name}`)"):
                    st.markdown(f"""
                    **Description:** {info['description']}
                    
                    **Range:** {info['range']}
                    
                    **Interpretation:** {info['interpretation']}
                    
                    **Best For:** {info.get('best_for', 'General text comparison')}
                    """)
            else:
                with st.expander(f"**{metric_name}**"):
                    st.markdown(f"Score: {metrics[metric_name]:.4f}")
        
        st.divider()
        
        # -------------------------------------------------------------------------
        # Additional Context (Example-specific)
        # -------------------------------------------------------------------------
        with st.expander("ℹ️ About This Evaluation"):
            if selected_id == "deepseek_cost_analysis":
                st.markdown("""
                **Dataset:** AI4Society DeepSeek Evaluation
                
                **Task:** Explaining how DeepSeek achieved low development costs
                
                **Models Compared:**
                - **Reference:** Llama 3.3 (comprehensive 472-word explanation)
                - **Generated:** DeepSeek R1 (concise 238-word response)
                
                **Key Insight:** 
                High BERTScore (0.87) indicates strong semantic similarity despite different 
                response lengths and styles. Lower BLEU/Jaccard scores reflect stylistic differences.
                """)
            elif selected_id == "election_voter_registration":
                st.markdown("""
                **Dataset:** South Carolina Election Data (April 2022)
                
                **Task:** Answering voter registration questions
                
                **Models Compared:**
                - **Reference:** SafeChat (official SC voter information)
                - **Generated:** ChatGPT-4o
                
                **Key Insight:**
                Lower scores indicate ChatGPT-4o provided a simplified answer that missed 
                important nuances about failsafe voting options available to voters.
                """)
    else:
        st.warning("No metrics available for this example")

display_footer()
