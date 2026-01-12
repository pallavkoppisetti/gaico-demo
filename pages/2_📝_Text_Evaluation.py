"""Text Evaluation page - LLM response comparison."""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_components import display_header, display_sidebar_links, display_footer
from utils.data_loader import load_text_examples
from utils.metric_info import get_metric_description, METRIC_INFO

st.set_page_config(page_title="GAICo Demo - Text Evaluation", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()

st.header("📝 Text Evaluation Examples")

text_data = load_text_examples()

if not text_data or "examples" not in text_data:
    st.error("Text examples not found. Check data/text_examples.json")
    st.stop()

st.markdown("""
These examples demonstrate GAICo's text evaluation capabilities using real LLM outputs 
from production use cases.
""")

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

# Show texts side by side
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Reference")
    st.caption(f"Model: {example['reference']['model']}")
    st.caption(f"Word Count: {example['reference']['word_count']}")
    with st.expander("View Text", expanded=True):
        st.text_area(
            "Reference Text",
            example['reference']['text'],
            height=300,
            label_visibility="collapsed"
        )

with col2:
    st.markdown("### Generated")
    st.caption(f"Model: {example['generated']['model']}")
    st.caption(f"Word Count: {example['generated']['word_count']}")
    with st.expander("View Text", expanded=True):
        st.text_area(
            "Generated Text",
            example['generated']['text'],
            height=300,
            label_visibility="collapsed"
        )

st.divider()

# Display metrics
st.subheader("📊 Evaluation Metrics")

metrics = example.get("metrics", {})

if metrics:
    cols = st.columns(3)
    for idx, (metric_name, score) in enumerate(metrics.items()):
        with cols[idx % 3]:
            st.metric(
                label=metric_name,
                value=f"{score:.3f}",
                help=get_metric_description(metric_name)
            )
    
    st.divider()
    
    with st.expander("📖 Metric Descriptions"):
        for metric_name in metrics.keys():
            if metric_name in METRIC_INFO:
                info = METRIC_INFO[metric_name]
                st.markdown(f"""
                **{info['name']}** ({metric_name})  
                *{info['description']}*  
                Range: {info['range']} | {info['interpretation']}
                """)
else:
    st.warning("No metrics available for this example")

display_footer()
