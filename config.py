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
# CUSTOM CSS - Modify styling here
# =============================================================================
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
"""
