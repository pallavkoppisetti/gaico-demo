"""LLM FAQ page - Multi-model comparison with consistent 2-tab structure."""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATA_DIR
from utils.ui_components import display_footer
from utils.visualizations import display_llm_faq_plots

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2

st.header("E1: LLM FAQ Evaluation")

st.markdown("""
Comprehensive comparison of **DeepSeek R1** vs **Llama 3.3** on a FAQ dataset using multiple metrics.
GAICo evaluates text similarity and generates visualizations for detailed analysis.
""")

# ============================================================================
# Load Data
# ============================================================================
csv_path = DATA_DIR / "llm_responses_processed.csv"

if not csv_path.exists():
    st.error("LLM responses CSV not found")
    st.stop()

df = pd.read_csv(csv_path)

# ============================================================================
# Question Selector (Outside tabs for consistency)
# ============================================================================
st.markdown("""
| Component | Description |
|-----------|-------------|
| **📥 GAICo Inputs** | Two LLM responses (DeepSeek R1 and Llama 3.3) answering the same question |
| **📤 GAICo Outputs** | Multi-metric comparison: BLEU, ROUGE, BERTScore, Jaccard, Levenshtein, and more |
| **🎯 What this shows** | How similarly (or differently) two state-of-the-art LLMs respond to the same prompt |

**You are selecting:** A FAQ question to see how two different LLMs answered it.
""")

questions = df['question'].tolist()
selected_q_idx = st.selectbox(
    "Select Question",
    range(len(questions)),
    format_func=lambda x: questions[x][:80] + "..." if len(questions[x]) > 80 else questions[x],
    help="Choose a question to compare LLM responses"
)

selected_row = df.iloc[selected_q_idx]

st.markdown("""
<div style="text-align: center; background-color: #f8f9fa; padding: 0.75rem 1rem; border-radius: 0.5rem; margin: 1rem 0;">
    <strong>The output of GAICo evaluation is below.</strong> Use the tabs to switch between: (1) viewing inputs & visualization, or (2) detailed scores & analysis.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# Two-Tab Structure: Input+Viz | Scores+Details
# ============================================================================
tab1, tab2 = st.tabs(["📥 Input & Visualization", "📤 Scores & Analysis"])

# ============================================================================
# TAB 1: Input Data + Visualization (The Hook)
# ============================================================================
with tab1:
    st.subheader("LLM Response Comparison")
    
    st.markdown(f"**Question:** {selected_row['question']}")
    

    
    # -------------------------------------------------------------------------
    # Input Section: Side by Side Responses
    # -------------------------------------------------------------------------
    st.markdown("### Input Data")
    
    col1, col2 = st.columns(2)
    
    def format_text(text):
        """Format text for display."""
        if pd.isna(text):
            return "No response"
        text = str(text)
        text = text.replace('\\n', '\n')
        text = text.replace('\\t', '\t')
        return text
    
    with col1:
        st.markdown("**DeepSeek R1 Response**")
        r1_text = format_text(selected_row.get('r1', ''))
        st.markdown(
            f'<div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; max-height: 350px; overflow-y: auto; white-space: pre-wrap; font-size: 0.85rem;">{r1_text}</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("**Llama 3.3 Response**")
        llama_text = format_text(selected_row.get('llama3.3', ''))
        st.markdown(
            f'<div style="background-color: #e8f8e8; padding: 1rem; border-radius: 0.5rem; max-height: 350px; overflow-y: auto; white-space: pre-wrap; font-size: 0.85rem;">{llama_text}</div>',
            unsafe_allow_html=True
        )
    

    
    # -------------------------------------------------------------------------
    # Visualization Section
    # -------------------------------------------------------------------------
    st.markdown("### GAICo Visualization")
    
    # Display aggregate visualization from pre-generated plots
    plot_type = st.selectbox(
        "Select Visualization Type",
        options=["radar", "bar", "heatmaps", "line"],
        format_func=lambda x: {
            "radar": "Radar Charts (Multi-Metric Overview)",
            "bar": "Bar Charts (Model Comparison)",
            "heatmaps": "Heatmaps (Score Matrix)",
            "line": "Line Plots (Trend Analysis)"
        }[x],
        key="viz_type_tab1"
    )
    
    display_llm_faq_plots(plot_type=plot_type)

# ============================================================================
# TAB 2: Scores, Analysis & Metric Explanations
# ============================================================================
with tab2:
    st.subheader("Detailed Analysis")
    
    st.markdown(f"**Question:** {selected_row['question'][:100]}...")
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Aggregate Metrics Information
    # -------------------------------------------------------------------------
    st.markdown("### Evaluation Methodology")
    
    st.info("""
    GAICo computes the following metrics to compare DeepSeek R1 and Llama 3.3 responses:
    - **BLEU** - N-gram precision based metric
    - **ROUGE-L** - Longest common subsequence based
    - **BERTScore** - Semantic similarity using BERT embeddings
    - **Jaccard** - Token-level set overlap
    - **Levenshtein** - Edit distance normalized
    - **JSD** - Jensen-Shannon Divergence (distribution difference)
    """)
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # CSV Report (All Questions)
    # -------------------------------------------------------------------------
    st.markdown("### Full Dataset Overview")
    
    # Create a summary table
    summary_data = []
    for idx, row in df.iterrows():
        summary_data.append({
            "Question": row['question'][:60] + "..." if len(row['question']) > 60 else row['question'],
            "DeepSeek R1 (chars)": len(str(row.get('r1', ''))) if pd.notna(row.get('r1')) else 0,
            "Llama 3.3 (chars)": len(str(row.get('llama3.3', ''))) if pd.notna(row.get('llama3.3')) else 0
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, width='stretch', hide_index=True)
    
    # Download button
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=csv_data,
        file_name="gaico_llm_faq_responses.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Metric Descriptions
    # -------------------------------------------------------------------------
    st.markdown("### Metric Explanations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("**BLEU** (Bilingual Evaluation Understudy)"):
            st.markdown("""
            - N-gram precision based metric
            - Range: 0.0 to 1.0 (higher is better)
            - Best for: Translation, summarization
            - Measures exact word/phrase overlap
            """)
        
        with st.expander("**ROUGE-L** (Recall-Oriented Understudy)"):
            st.markdown("""
            - Longest common subsequence based
            - Range: 0.0 to 1.0 (higher is better)
            - Best for: Summarization quality
            - Captures sentence-level structure
            """)
        
        with st.expander("**BERTScore**"):
            st.markdown("""
            - Semantic similarity using BERT embeddings
            - Range: 0.0 to 1.0 (higher is better)
            - Best for: Meaning preservation
            - Captures semantic equivalence beyond exact wording
            """)
    
    with col2:
        with st.expander("**Jaccard Similarity**"):
            st.markdown("""
            - Token-level set overlap
            - Range: 0.0 to 1.0 (higher is better)
            - Best for: Vocabulary coverage
            - Measures proportion of shared words
            """)
        
        with st.expander("**Levenshtein Distance**"):
            st.markdown("""
            - Edit distance normalized
            - Range: 0.0 to 1.0 (higher is better)
            - Best for: String similarity
            - Counts insertions, deletions, substitutions
            """)
        
        with st.expander("**JSD** (Jensen-Shannon Similarity)"):
            st.markdown("""
            - Distribution similarity
            - Range: 0.0 to 1.0 (**higher is better**)
            - Best for: Probability distribution comparison
            - Measures similarity between word distributions
            """)
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # About This Evaluation
    # -------------------------------------------------------------------------
    with st.expander("ℹ️ About This Evaluation"):
        st.markdown("""
        **Dataset:** AI4Society LLM FAQ Dataset
        
        **Models Compared:**
        - **DeepSeek R1**: Chinese AI model with strong reasoning capabilities
        - **Llama 3.3**: Meta's open-source LLM
        
        **Question Categories:**
        - General knowledge (capital cities)
        - Technical explanations (AI development costs)
        - Politically sensitive topics (Taiwan, Tiananmen)
        - Practical advice (credit cards, health, scams)
        
        **Key Insights:**
        - DeepSeek R1 shows distinct response patterns on politically sensitive topics
        - Both models provide similar quality on factual questions
        - Response length varies significantly between models
        """)

display_footer()
