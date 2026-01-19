"""Visualization utilities for displaying GAICo-generated plots."""

from pathlib import Path
from typing import Optional, List
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import LLM_FAQ_PLOTS_DIR, CASE_STUDY_DIR, ASSETS_DIR

# GAICo-style color palette
GAICO_COLORS = px.colors.qualitative.Set2


def display_plot(image_path: str, caption: Optional[str] = None) -> None:
    """Display a plot image if it exists, otherwise show error."""
    if Path(image_path).exists():
        st.image(image_path, caption=caption)
    else:
        st.error(f"❌ Image not found: {image_path}")


def create_metric_bar_chart(
    df: pd.DataFrame,
    metric_col: str = "metric_name",
    score_col: str = "score",
    model_col: str = "model_name",
    title: str = "Metric Comparison",
    height: int = 550
) -> go.Figure:
    """
    Create a grouped bar chart comparing metrics across models.
    Matches GAICo's plot_metric_comparison style.
    """
    fig = px.bar(
        df,
        x=model_col,
        y=score_col,
        color=metric_col,
        barmode="group",
        title=title,
        color_discrete_sequence=GAICO_COLORS,
        height=height
    )
    
    fig.update_layout(
        xaxis_title="Model",
        yaxis_title="Score",
        legend_title="Metric",
        font=dict(size=14),
        title_font=dict(size=20, color='#1f2937'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13)),
        xaxis=dict(tickfont=dict(size=13)),
        yaxis=dict(tickfont=dict(size=13)),
        plot_bgcolor='rgba(248,250,252,0.8)',
        paper_bgcolor='white'
    )
    
    fig.update_yaxes(range=[0, 1.1])
    
    return fig


def create_single_metric_bar_chart(
    df: pd.DataFrame,
    metric_name: str,
    metric_col: str = "metric_name",
    score_col: str = "score",
    model_col: str = "model_name",
    title: Optional[str] = None,
    height: int = 500
) -> go.Figure:
    """
    Create a bar chart for a single metric across models.
    Matches GAICo's plot_metric_comparison style.
    """
    filtered_df = df[df[metric_col] == metric_name]
    
    # Aggregate if multiple scores per model
    agg_df = filtered_df.groupby(model_col)[score_col].mean().reset_index()
    
    fig = px.bar(
        agg_df,
        x=model_col,
        y=score_col,
        title=title or f"{metric_name} Comparison",
        color=model_col,
        color_discrete_sequence=GAICO_COLORS,
        height=height
    )
    
    fig.update_layout(
        xaxis_title="Model",
        yaxis_title="Score",
        showlegend=False,
        font=dict(size=14),
        title_font=dict(size=20, color='#1f2937'),
        xaxis=dict(tickfont=dict(size=13)),
        yaxis=dict(tickfont=dict(size=13)),
        plot_bgcolor='rgba(248,250,252,0.8)',
        paper_bgcolor='white'
    )
    
    fig.update_yaxes(range=[0, max(1.0, agg_df[score_col].max() * 1.1)])
    
    return fig


def create_radar_chart(
    df: pd.DataFrame,
    metrics: List[str],
    model_col: str = "model_name",
    metric_col: str = "metric_name",
    score_col: str = "score",
    title: str = "Multi-Metric Radar Comparison",
    height: int = 600
) -> go.Figure:
    """
    Create a radar chart comparing multiple metrics across models.
    Matches GAICo's plot_radar_comparison style.
    """
    fig = go.Figure()
    
    models = df[model_col].unique()
    
    for idx, model in enumerate(models):
        model_df = df[df[model_col] == model]
        
        # Get scores for each metric
        scores = []
        for metric in metrics:
            metric_score = model_df[model_df[metric_col] == metric][score_col].mean()
            scores.append(metric_score if pd.notna(metric_score) else 0)
        
        # Close the radar chart
        scores.append(scores[0])
        metrics_closed = metrics + [metrics[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=metrics_closed,
            fill='toself',
            name=model,
            line_color=GAICO_COLORS[idx % len(GAICO_COLORS)],
            line_width=3,
            opacity=0.75
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1],
                tickfont=dict(size=12, color='#4b5563'),
                gridcolor='rgba(156, 163, 175, 0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#1f2937', weight='bold'),
                gridcolor='rgba(156, 163, 175, 0.3)'
            ),
            bgcolor='rgba(248,250,252,0.5)'
        ),
        showlegend=True,
        title=dict(text=title, font=dict(size=20, color='#1f2937')),
        height=height,
        font=dict(size=14),
        legend=dict(
            font=dict(size=14),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e5e7eb',
            borderwidth=1
        ),
        paper_bgcolor='white'
    )
    
    return fig


def create_timeseries_line_chart(
    series_data: dict,
    title: str = "Time Series Comparison",
    height: int = 400
) -> go.Figure:
    """
    Create a line chart comparing time series data.
    
    Args:
        series_data: Dict mapping series names to lists of values
        title: Chart title
        height: Chart height
    """
    fig = go.Figure()
    
    for idx, (name, values) in enumerate(series_data.items()):
        fig.add_trace(go.Scatter(
            x=list(range(len(values))),
            y=values,
            mode='lines+markers',
            name=name,
            line_color=GAICO_COLORS[idx % len(GAICO_COLORS)]
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='#1f2937')),
        xaxis_title="Time Step",
        yaxis_title="Value",
        height=550,
        font=dict(size=14),
        xaxis=dict(tickfont=dict(size=13), gridcolor='rgba(156, 163, 175, 0.3)'),
        yaxis=dict(tickfont=dict(size=13), gridcolor='rgba(156, 163, 175, 0.3)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13)),
        plot_bgcolor='rgba(248,250,252,0.8)',
        paper_bgcolor='white'
    )
    
    return fig


def display_case_study_plots(plot_type: str = "radar") -> None:
    """Display case study radar or bar plots (modality quality and plan coherence)."""
    if plot_type not in ["radar", "bars"]:
        st.error("Plot type must be 'radar' or 'bars'")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Modality Generation Quality")
        st.caption("Evaluates image and audio quality generated by specialist models")
        display_plot(str(CASE_STUDY_DIR / "figures" / f"modality_quality_{plot_type}.png"))
    
    with col2:
        st.markdown("### Plan Coherence")
        st.caption("Evaluates text planning and structured data accuracy")
        display_plot(str(CASE_STUDY_DIR / "figures" / f"plan_coherence_{plot_type}.png"))


def display_llm_faq_plots(plot_type: str = "radar", metric: Optional[str] = None) -> None:
    """Display LLM FAQ comparison plots (radar, bar, heatmaps, or line)."""
    valid_types = ["radar", "bar", "heatmaps", "line"]
    if plot_type not in valid_types:
        st.error(f"Plot type must be one of: {', '.join(valid_types)}")
        return
    
    plot_dir = LLM_FAQ_PLOTS_DIR / plot_type
    
    if not plot_dir.exists():
        st.warning(f"No plots found in {plot_dir}")
        return
    
    available_plots = sorted(plot_dir.glob("*.png"))
    
    if not available_plots:
        st.warning(f"No PNG files found in {plot_dir}")
        return
    
    # Handle specific metric request
    if metric:
        suffix = "_radar_chart" if plot_type == "radar" else f"_{plot_type}"
        metric_plot = plot_dir / f"{metric}{suffix}.png"
        if metric_plot.exists():
            display_plot(str(metric_plot), caption=f"{metric} - {plot_type.title()}")
        else:
            st.error(f"Plot not found: {metric_plot.name}")
        return
    
    # Display all plots based on type
    if plot_type == "radar":
        overall = plot_dir / "overall_radar_chart.png"
        if overall.exists():
            display_plot(str(overall), caption="Overall Multi-Metric Comparison")
            st.divider()
        
        st.markdown("#### Individual Metric Radars")
        cols = st.columns(3)
        for idx, p in enumerate([x for x in available_plots if "overall" not in x.name]):
            with cols[idx % 3]:
                display_plot(str(p), caption=p.stem.replace("_radar_chart", ""))
    
    elif plot_type == "bar":
        for p in available_plots:
            display_plot(str(p), caption=p.stem.replace("_", " ").title())
    
    else:  # heatmaps or line
        cols = st.columns(2)
        suffix = "_heatmap" if plot_type == "heatmaps" else "_line_plot"
        for idx, p in enumerate(available_plots):
            with cols[idx % 2]:
                display_plot(str(p), caption=p.stem.replace(suffix, ""))
