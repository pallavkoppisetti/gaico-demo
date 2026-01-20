"""Metric descriptions and metadata for all GAICo evaluation metrics."""

from typing import Dict

# Metric definitions: {name: {description, range, interpretation, ...}}
METRIC_INFO: Dict[str, Dict[str, str]] = {
    # Text Metrics
    "BLEU": {
        "name": "BLEU Score",
        "category": "Text",
        "description": "N-gram overlap between generated and reference text",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "ROUGE-L": {
        "name": "ROUGE-L",
        "category": "Text",
        "description": "Longest common subsequence similarity",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "BERTScore-F1": {
        "name": "BERTScore F1",
        "category": "Text",
        "description": "Semantic similarity using BERT embeddings",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "Jaccard": {
        "name": "Jaccard Similarity",
        "category": "Text",
        "description": "Word set overlap (intersection over union)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "JSD": {
        "name": "Jensen-Shannon Similarity",
        "category": "Text",
        "description": "Word distribution similarity (1 - divergence)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "Levenshtein": {
        "name": "Levenshtein Similarity",
        "category": "Text",
        "description": "Normalized edit similarity (1 - normalized distance)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "CosineSimilarity": {
        "name": "Cosine Similarity",
        "category": "Text",
        "description": "Angle between text embedding vectors",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    
    # Image Metrics
    "SSIM": {
        "name": "Structural Similarity",
        "category": "Image",
        "description": "Compares luminance, contrast, and structure",
        "range": "-1.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "PSNR": {
        "name": "Peak SNR",
        "category": "Image",
        "description": "Signal-to-noise ratio in dB",
        "range": "0 to ∞ (typically 20-50 dB)",
        "interpretation": "Higher is better"
    },
    "AverageHash": {
        "name": "Average Hash",
        "category": "Image",
        "description": "Perceptual hash similarity",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "HistogramMatch": {
        "name": "Histogram Match",
        "category": "Image",
        "description": "Color distribution similarity",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    
    # Audio Metrics
    "AudioSNR": {
        "name": "Audio SNR",
        "category": "Audio",
        "description": "Signal-to-noise ratio (normalized)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "AudioSpectrogramDistance": {
        "name": "Spectrogram Similarity",
        "category": "Audio",
        "description": "Frequency representation similarity (converted from distance)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    
    # Planning Metrics
    "PlanningLCS": {
        "name": "Planning LCS",
        "category": "Planning",
        "description": "Longest common subsequence (order-preserving)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    "PlanningJaccard": {
        "name": "Planning Jaccard",
        "category": "Planning",
        "description": "Action set overlap (order-independent)",
        "range": "0.0 to 1.0",
        "interpretation": "Higher is better"
    },
    
    # Time Series Metrics
    "TimeSeriesDTW": {
        "name": "Dynamic Time Warping",
        "category": "Time Series",
        "description": "Similarity with temporal alignment",
        "range": "0.0 to 1.0",
        "interpretation": "Lower is better"
    },
    "TimeSeriesElementDiff": {
        "name": "Element-wise Difference",
        "category": "Time Series",
        "description": "Average point-by-point difference",
        "range": "0.0 to 1.0",
        "interpretation": "Lower is better"
    },
}


def get_metric_description(metric_name: str) -> str:
    """Get short description for a metric. Returns metric name if not found."""
    if metric_name in METRIC_INFO:
        return METRIC_INFO[metric_name]["description"]
    return f"Metric: {metric_name}"


def get_metric_interpretation(metric_name: str) -> str:
    """Get interpretation guidance (higher/lower is better)."""
    if metric_name in METRIC_INFO:
        return METRIC_INFO[metric_name]["interpretation"]
    return "Higher is typically better"
