# GAICo Real Evaluation Results

This directory contains actual evaluation results from GAICo library runs.

## Structure

- `case_study/` - Multi-modal travel assistant case study
  - `csvs/` - results_modality_quality.csv, results_plan_coherence.csv
  - `figures/` - 4 PNG plots (bars + radars)

- `audio/` - TTS model comparisons
  - `csvs/` - tts_model_comparison.csv, tts_evaluation.csv

- `images/` - Image generation evaluations
  - `csvs/` - basketball_team, street_signs results

- `text/` - Text evaluation results
  - Election Q&A evaluation
  - LLM FAQ comparisons

## CSV Formats

### Long Format (Standard GAICo)
```csv
model_name,metric_name,score,passed_threshold,threshold_applied
Google TTS,AudioSNR,0.259,False,0.5
```

### Wide Format (Case Study)
```csv
pipeline,AudioSNR,ImageSSIM,PlanningLCS,...
pipeline_A,1.0,1.0,1.0,...
```

## Usage in Demo

These files are loaded by:
- `utils/data_loader.py` - Loads CSVs
- `app.py` - Displays plots and metrics
