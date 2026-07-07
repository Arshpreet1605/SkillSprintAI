"""
app/ui/components/kpi_card.py
------------------------------
Reusable KPI metric tile component.

Renders a styled HTML card showing:
  - An emoji icon
  - A headline metric value
  - A label
  - An optional subtitle / delta badge

Usage:
    from app.ui.components.kpi_card import render_kpi_card

    render_kpi_card(
        icon="🏆",
        label="Overall Score",
        value="78 / 100",
        subtitle="Above average",
        delta="positive",   # "positive" | "negative" | "neutral"
    )
"""

import streamlit as st


# ── Colour tokens matching styles.py ─────────────────────────────────────────
_DELTA_COLOURS = {
    "positive": ("#4CAF50", "▲"),
    "negative": ("#EF5350", "▼"),
    "neutral":  ("#9EB3D8", "●"),
}


def render_kpi_card(
    icon: str,
    label: str,
    value: str,
    subtitle: str = "",
    delta: str = "neutral",
) -> None:
    """
    Renders a glassmorphism KPI metric card.

    Parameters
    ----------
    icon     : Emoji or unicode symbol shown at the top of the card.
    label    : Short title label (e.g. "Overall Score").
    value    : Primary metric value displayed prominently.
    subtitle : Optional secondary line / description text.
    delta    : One of "positive", "negative", or "neutral". Controls the
               colour and arrow of the subtitle badge.
    """
    colour, arrow = _DELTA_COLOURS.get(delta, _DELTA_COLOURS["neutral"])

    subtitle_html = (
        f"""
        <div class="kpi-subtitle" style="color:{colour};">
            {arrow}&nbsp;{subtitle}
        </div>
        """
        if subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
