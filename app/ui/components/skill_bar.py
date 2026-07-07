"""
app/ui/components/skill_bar.py
-------------------------------
Reusable animated horizontal skill/score progress bar.

Renders a labelled bar that fills proportionally to a score out of 10
(or a custom max), using a gradient consistent with the app's design system.

Usage:
    from app.ui.components.skill_bar import render_skill_bar

    render_skill_bar(label="Technical Skills", score=8, max_score=10)
    render_skill_bar(label="Communication",    score=6, max_score=10, colour="#29B6F6")
"""

import streamlit as st


# ── Default gradient matches --gradient CSS variable ─────────────────────────
_DEFAULT_GRADIENT = "linear-gradient(90deg, #1565C0 0%, #0288D1 60%, #29B6F6 100%)"

# Score → descriptive band
_SCORE_BANDS = [
    (8, "Excellent",  "#4CAF50"),
    (6, "Good",       "#29B6F6"),
    (4, "Average",    "#FFA726"),
    (0, "Needs Work", "#EF5350"),
]


def _get_band(score: float, max_score: float) -> tuple[str, str]:
    """Returns (band_label, band_colour) for a normalised score."""
    pct = score / max_score * 10
    for threshold, label, colour in _SCORE_BANDS:
        if pct >= threshold:
            return label, colour
    return "Needs Work", "#EF5350"


def render_skill_bar(
    label: str,
    score: float,
    max_score: float = 10,
    colour: str | None = None,
    show_band: bool = True,
) -> None:
    """
    Renders a single labelled progress bar.

    Parameters
    ----------
    label     : Display name for the skill (e.g. "Problem Solving").
    score     : Numeric score.
    max_score : Denominator for the percentage calculation (default 10).
    colour    : Override bar fill colour / gradient string.
    show_band : If True, shows a text badge (Excellent / Good / Average / Needs Work).
    """
    pct = min(max(score / max_score * 100, 0), 100)
    band_label, band_colour = _get_band(score, max_score)
    fill = colour or _DEFAULT_GRADIENT

    badge_html = (
        f'<span class="skill-band-badge" style="color:{band_colour};border-color:{band_colour};">'
        f'{band_label}</span>'
        if show_band
        else ""
    )

    st.markdown(
        f"""
        <div class="skill-bar-wrapper">
            <div class="skill-bar-header">
                <span class="skill-bar-label">{label}</span>
                <div class="skill-bar-meta">
                    {badge_html}
                    <span class="skill-bar-score">{score:.1f} / {max_score:.0f}</span>
                </div>
            </div>
            <div class="skill-bar-track">
                <div class="skill-bar-fill"
                     style="width:{pct:.1f}%;background:{fill};">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
