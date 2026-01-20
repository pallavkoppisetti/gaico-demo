"""
Central configuration for GAICo Demo App.
Edit this file to update paths, constants, and styling.
"""

from pathlib import Path

# =============================================================================
# APP METADATA - Update for conferences/presentations
# =============================================================================
APP_TITLE = "GAICo Demo - AAAI-26"
APP_ICON = "📊"
APP_SUBTITLE = "Generative AI Comparator - Multi-Modal Evaluation Framework"
CONFERENCE = "AAAI-26 Demo Track"
CONFERENCE_DATE = "January 23, 2026"
INSTITUTION = "USC AI Institute"

# =============================================================================
# PATHS - All data paths relative to project root
# =============================================================================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# GAICo Results
GAICO_RESULTS_DIR = DATA_DIR / "gaico_results"
CASE_STUDY_DIR = GAICO_RESULTS_DIR / "case_study"
AUDIO_DIR = GAICO_RESULTS_DIR / "audio"
IMAGE_DIR = GAICO_RESULTS_DIR / "images"
TEXT_DIR = GAICO_RESULTS_DIR / "text"
STRUCTURED_DIR = GAICO_RESULTS_DIR / "structured"

# CSV Paths
CSV_MODALITY_QUALITY = CASE_STUDY_DIR / "csvs" / "results_modality_quality.csv"
CSV_PLAN_COHERENCE = CASE_STUDY_DIR / "csvs" / "results_plan_coherence.csv"
CSV_TTS_COMPARISON = AUDIO_DIR / "csvs" / "tts_model_comparison.csv"
CSV_BASKETBALL = IMAGE_DIR / "csvs" / "basketball_team_image_evaluation_results.csv"
CSV_STREET_SIGNS = IMAGE_DIR / "csvs" / "street_signs_image_evaluation_results.csv"
CSV_PLANNING_METRICS = STRUCTURED_DIR / "planning_metrics_report.csv"
CSV_TIMESERIES_METRICS = STRUCTURED_DIR / "timeseries_metrics_report.csv"

# Plot Paths
LLM_FAQ_PLOTS_DIR = ASSETS_DIR / "plots" / "llm_faq"

# =============================================================================
# EXTERNAL LINKS
# =============================================================================
GITHUB_URL = "https://github.com/ai4society/GenAIResultsComparator"
PYPI_URL = "https://pypi.org/project/gaico/"
DOCS_URL = "https://ai4society.github.io/projects/GenAIResultsComparator/"
CONTACT_EMAIL = "ai4societyteam@gmail.com"

# =============================================================================
# STATISTICS - Update as needed
# =============================================================================
STATS = {
    "pypi_downloads": "16,000+",
    "metrics_count": "15+",
    "notebooks_count": "17",
}

# =============================================================================
# CUSTOM CSS - Consistent color coding for the application
# =============================================================================
# Color Guide:
# - Reference/Input: Blue tones (#e8f4f8, #3b82f6)
# - Generated/Output: Green tones (#e8f8e8, #10b981)
# - Configuration: Purple tones (#667eea)
# - Highlights/Results: Amber tones (#fef3c7, #f59e0b)

CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Consistent Input/Output color coding */
    .input-section {
        background-color: #e8f4f8;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .output-section {
        background-color: #e8f8e8;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .reference-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #93c5fd;
    }
    .generated-box {
        background-color: #e8f8e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #86efac;
    }
    
    /* Configuration section styling */
    .config-section {
        background-color: #f3f4f6;
        border-left: 4px solid #667eea;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Results highlight */
    .results-highlight {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
"""
