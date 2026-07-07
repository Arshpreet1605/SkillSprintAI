"""
app/ui/components/radar_chart.py
---------------------------------
Reusable Plotly radar (spider) chart component for skill visualisation.

Renders a dark-themed, filled radar chart that visually maps multi-dimensional
skill scores using the app's colour palette.

Usage:
    from app.ui.components.radar_chart import render_radar_chart

    render_radar_chart(
        labels=["Technical", "Communication", "Problem Solving", "Confidence", "Role Match"],
        scores=[8, 6, 7, 5, 9],
        title="Skill Breakdown",
    )
"""

import plotly.graph_objects as go
import streamlit as st


# ── Design tokens (mirror styles.py CSS variables) ────────────────────────────
_PRIMARY      = "#1565C0"
_ACCENT       = "#29B6F6"
_BG_CARD      = "rgba(255,255,255,0.04)"
_TEXT_PRIMARY = "#F0F4FF"
_GRID_COLOUR  = "rgba(255,255,255,0.08)"


def render_radar_chart(
    labels: list[str],
    scores: list[float],
    title: str = "Skill Breakdown",
    max_score: float = 10,
    height: int = 400,
) -> None:
    """
    Renders an interactive Plotly radar chart.

    Parameters
    ----------
    labels    : Category names (e.g. ["Technical", "Communication", ...]).
    scores    : Numeric score for each category (same length as labels).
    title     : Chart title displayed above the plot.
    max_score : Radial axis maximum value (default 10).
    height    : Chart height in pixels.
    """
    if len(labels) != len(scores):
        st.error("radar_chart: labels and scores must have the same length.")
        return

    # Close the polygon by repeating the first value
    closed_labels = labels + [labels[0]]
    closed_scores = scores + [scores[0]]

    fig = go.Figure()

    # ── Filled radar trace ────────────────────────────────────────────────────
    fig.add_trace(
        go.Scatterpolar(
            r=closed_scores,
            theta=closed_labels,
            fill="toself",
            name="Your Score",
            line=dict(color=_ACCENT, width=2.5),
            fillcolor="rgba(41, 182, 246, 0.18)",
            marker=dict(size=7, color=_ACCENT),
            hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>",
        )
    )

    # ── Average benchmark trace (faint) ───────────────────────────────────────
    avg = sum(scores) / len(scores)
    bench_scores = [avg] * len(labels) + [avg]
    fig.add_trace(
        go.Scatterpolar(
            r=bench_scores,
            theta=closed_labels,
            mode="lines",
            name="Average",
            line=dict(color="rgba(255,255,255,0.20)", width=1.5, dash="dot"),
            hoverinfo="skip",
        )
    )

    # ── Layout ────────────────────────────────────────────────────────────────
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, max_score],
                tickfont=dict(color="rgba(255,255,255,0.40)", size=10),
                gridcolor=_GRID_COLOUR,
                linecolor=_GRID_COLOUR,
                tickvals=[2, 4, 6, 8, 10],
            ),
            angularaxis=dict(
                tickfont=dict(color=_TEXT_PRIMARY, size=12, family="Inter, sans-serif"),
                linecolor=_GRID_COLOUR,
                gridcolor=_GRID_COLOUR,
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            font=dict(color=_TEXT_PRIMARY, size=11),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
        ),
        title=dict(
            text=title,
            font=dict(color=_TEXT_PRIMARY, size=15, family="Inter, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        margin=dict(t=50, l=40, r=40, b=40),
        height=height,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
