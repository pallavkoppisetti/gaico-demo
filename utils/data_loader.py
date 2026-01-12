"""Data loading utilities with Streamlit caching."""

import json
import streamlit as st
from typing import Dict, Any, Optional


@st.cache_data
def load_json_data(file_path: str) -> Dict[str, Any]:
    """Load JSON file with caching. Raises FileNotFoundError or JSONDecodeError on failure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON in {file_path}: {e}")
        raise


@st.cache_data
def load_text_examples() -> Dict[str, Any]:
    """Load text evaluation examples from data/text_examples.json."""
    return load_json_data("data/text_examples.json")


@st.cache_data
def load_image_examples() -> Dict[str, Any]:
    """Load image evaluation examples from data/image_examples.json."""
    return load_json_data("data/image_examples.json")


@st.cache_data
def load_audio_examples() -> Dict[str, Any]:
    """Load audio evaluation examples from data/audio_examples.json."""
    return load_json_data("data/audio_examples.json")


@st.cache_data
def load_structured_examples() -> Dict[str, Any]:
    """Load structured data examples from data/structured_examples.json."""
    return load_json_data("data/structured_examples.json")


def get_example_by_id(examples_data: Dict[str, Any], example_id: str) -> Optional[Dict[str, Any]]:
    """Get example by ID from loaded examples data. Returns None if not found."""
    for example in examples_data.get("examples", []):
        if example.get("id") == example_id:
            return example
    return None
