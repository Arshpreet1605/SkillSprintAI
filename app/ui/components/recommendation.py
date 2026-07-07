"""
app/ui/components/recommendation.py
--------------------------------------
Reusable Strengths / Weaknesses / Next-Steps panel component.

Renders a two-column card layout:
  - Left  : ✅ Strengths list
  - Right : ⚠️ Weaknesses list
  - Below : 🎯 Next-Steps action items (numbered list)

Usage:
    from app.ui.components.recommendation import render_recommendation_panel

    render_recommendation_panel(
        strengths=["Strong Python skills", "Clear communication"],
        weaknesses=["Needs deeper SQL knowledge", "Improve system design"],
        next_steps=["Complete a SQL advanced course", "Practice mock system design interviews"],
        overall_text="You showed solid fundamentals. Focus on depth.",
    )
"""

import streamlit as st


# ── Internal helpers ──────────────────────────────────────────────────────────

def _bullet_items(items: list[str], icon: str, colour: str) -> str:
    """Returns an HTML unordered list of styled bullet items."""
    li_html = "".join(
        f'<li class="rec-item" style="border-left-color:{colour};">'
        f'<span class="rec-icon">{icon}</span>{item}</li>'
        for item in items
    )
    return f'<ul class="rec-list">{li_html}</ul>'


def _step_items(items: list[str]) -> str:
    """Returns numbered HTML list items for Next Steps."""
    li_html = "".join(
        f'<li class="step-item"><span class="step-num">{i + 1}</span>{item}</li>'
        for i, item in enumerate(items)
    )
    return f'<ol class="step-list">{li_html}</ol>'


# ── Public render function ────────────────────────────────────────────────────

def render_recommendation_panel(
    strengths: list[str],
    weaknesses: list[str],
    next_steps: list[str],
    overall_text: str = "",
) -> None:
    """
    Renders the full recommendation panel with strengths, weaknesses, and next steps.

    Parameters
    ----------
    strengths    : List of strength strings.
    weaknesses   : List of weakness / improvement area strings.
    next_steps   : Ordered list of actionable next-step strings.
    overall_text : Optional overall summary sentence shown at the top.
    """

    # ── Overall recommendation banner ─────────────────────────────────────────
    if overall_text:
        st.markdown(
            f"""
            <div class="overall-rec-banner">
                <span class="overall-rec-icon">💡</span>
                <span class="overall-rec-text">{overall_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Strengths & Weaknesses side-by-side ───────────────────────────────────
    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown(
            f"""
            <div class="rec-panel rec-strengths">
                <div class="rec-panel-title" style="color:#4CAF50;">✅ Strengths</div>
                {_bullet_items(strengths, "✓", "#4CAF50")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f"""
            <div class="rec-panel rec-weaknesses">
                <div class="rec-panel-title" style="color:#FFA726;">⚠️ Areas to Improve</div>
                {_bullet_items(weaknesses, "→", "#FFA726")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Next Steps ────────────────────────────────────────────────────────────
    if next_steps:
        st.markdown(
            f"""
            <div class="rec-panel rec-nextsteps">
                <div class="rec-panel-title" style="color:#29B6F6;">🎯 Recommended Next Steps</div>
                {_step_items(next_steps)}
            </div>
            """,
            unsafe_allow_html=True,
        )
