"""
Utils package for GAICo Demo App.

Modules:
- data_loader: JSON data loading with caching
- metric_info: Metric descriptions and metadata
- visualizations: Plot display functions
- ui_components: Shared Streamlit UI elements
"""

from .data_loader import load_text_examples, load_image_examples, load_audio_examples
from .metric_info import get_metric_description, METRIC_INFO
from .visualizations import display_case_study_plots, display_llm_faq_plots
from .ui_components import setup_page, display_header, display_sidebar_links, display_footer
