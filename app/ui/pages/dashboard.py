"""
app/ui/pages/dashboard.py
--------------------------
Sprint 2 — Performance Dashboard page for SkillSprint AI.

Renders a Power BI-inspired, dark-themed analytics dashboard.
Currently uses DUMMY SAMPLE DATA.  Gemini integration (Sprint 3) will
replace the dummy payload with `st.session_state["evaluation_result"]`.

Layout (top → bottom):
  1. Dashboard header + meta badge row
  2. KPI tiles row  (Overall Score, Role Match, Recommendation badge, Q&A count)
  3. Two-column mid section:
       Left  → Radar chart (multi-skill spider)
       Right → Skill bars (individual categories)
  4. Interview Timeline chart  (Plotly bar — per-question score)
  5. Recommendation panel  (Strengths / Weaknesses / Next Steps)
  6. Footer CTA  (Start New Assessment)
"""

import streamlit as st
import plotly.graph_objects as go

from app.ui.components.kpi_card          import render_kpi_card
from app.ui.components.skill_bar         import render_skill_bar
from app.ui.components.radar_chart       import render_radar_chart
from app.ui.components.recommendation    import render_recommendation_panel


# ── Dummy sample data (Sprint 2 placeholder) ──────────────────────────────────
# This entire block will be replaced in Sprint 3 with parsed Gemini output.

_SAMPLE = {
    # Top-level meta
    "candidate_name": "Arshpreet Singh",
    "target_role":    "Data Scientist",
    "experience_level": "Fresher",
    "assessment_date": "July 5, 2026",
    "overall_score":  74,
    "average_skill_score": 7.1,
    "hiring_recommendation": "Strong Candidate",

    # Individual skill scores (out of 10)
    "skills": {
        "Technical Skills":  7.5,
        "Communication":     6.8,
        "Problem Solving":   7.2,
        "Confidence":        5.9,
        "Role Match":        8.1,
    },

    # Per-question scores for the timeline (out of 10)
    "question_scores": [7, 8, 6, 9, 7],
    "question_labels": ["Q1", "Q2", "Q3", "Q4", "Q5"],

    # Qualitative feedback
    "strengths": [
        "Strong command of Python and data manipulation libraries",
        "Demonstrated clear understanding of ML concepts",
        "Excellent role alignment — skills match job requirements",
        "Articulate in explaining thought processes",
    ],
    "weaknesses": [
        "Needs to deepen knowledge of distributed systems",
        "Some answers lacked structured depth in system design",
        "Confidence could improve when addressing ambiguous questions",
    ],
    "next_steps": [
        "Complete an advanced SQL and database optimisation course",
        "Practice 2–3 system design mock interviews per week",
        "Study distributed computing concepts (Spark, Kafka basics)",
        "Record yourself answering questions to improve delivery confidence",
    ],
    "overall_text": (
        "You demonstrate solid analytical foundations and role alignment. "
        "Targeted effort on system design and distributed computing will "
        "make you a very competitive candidate."
    ),
}


# ── CSS injected specifically for the dashboard ───────────────────────────────
# Uses CSS variables already defined in styles.py; only adds dashboard-specific rules.

_DASHBOARD_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   DASHBOARD — Premium Power BI-inspired dark theme
   All rules are scoped via class names so they never bleed into other pages.
═══════════════════════════════════════════════════════════════════════════ */

/* ── Page width unlock (dashboard only) ────────────────────────────────── */
/* The global styles.py caps max-width at 860px — override it here so the
   dashboard can breathe across the full viewport. */
.block-container {
    max-width: 1280px !important;
    padding: 1.5rem 2rem 3rem 2rem !important;
}

/* ── Dummy data notice ─────────────────────────────────────────────────── */
.dummy-notice {
    background: rgba(255,167,38,0.08);
    border: 1px solid rgba(255,167,38,0.28);
    border-left: 3px solid #FFA726;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.76rem; color: #FFB74D;
    font-weight: 500; letter-spacing: 0.2px;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* ── Dashboard Header ──────────────────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, #0D1B3E 0%, #091426 50%, #060D1F 100%);
    border: 1px solid rgba(41,182,246,0.15);
    border-top: 3px solid #1565C0;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.8rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.04) inset;
}
.dash-header-left h2 {
    font-size: 1.4rem; font-weight: 800;
    color: #F0F4FF !important;
    margin: 0 0 0.2rem 0 !important;
    letter-spacing: -0.4px;
    line-height: 1.2;
}
.dash-header-left p {
    font-size: 0.85rem; color: #7A9CC4 !important; margin: 0 !important;
}
.dash-meta-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
.dash-meta-badge {
    background: rgba(21,101,192,0.18);
    border: 1px solid rgba(21,101,192,0.38);
    border-radius: 6px;
    padding: 0.28rem 0.8rem;
    font-size: 0.75rem; font-weight: 600;
    color: #29B6F6;
    letter-spacing: 0.3px;
    white-space: nowrap;
}
.dash-meta-badge.role { background: rgba(41,182,246,0.12); border-color: rgba(41,182,246,0.30); }
.dash-meta-badge.date { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.10); color: #7A9CC4; }

/* ── KPI Cards ─────────────────────────────────────────────────────────── */
.kpi-card {
    position: relative;
    background: linear-gradient(160deg, rgba(21,101,192,0.12) 0%, rgba(10,15,30,0.85) 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.35rem 1.1rem 1.15rem 1.1rem;
    text-align: center;
    backdrop-filter: blur(18px);
    overflow: hidden;
    box-shadow:
        0 2px 12px rgba(0,0,0,0.35),
        0 0 0 0 rgba(41,182,246,0);
    transition:
        transform 0.22s cubic-bezier(0.34,1.56,0.64,1),
        box-shadow 0.22s ease,
        border-color 0.22s ease;
    height: 100%;
    cursor: default;
}
/* Gradient top-accent line */
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1565C0 0%, #0288D1 50%, #29B6F6 100%);
    border-radius: 14px 14px 0 0;
}
/* Radial glow in background on hover */
.kpi-card::after {
    content: '';
    position: absolute;
    top: -30%; left: 50%;
    transform: translateX(-50%);
    width: 120%;
    height: 120%;
    background: radial-gradient(ellipse at center, rgba(41,182,246,0.07) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}
.kpi-card:hover {
    transform: translateY(-5px) scale(1.01);
    border-color: rgba(41,182,246,0.28);
    box-shadow:
        0 12px 36px rgba(0,0,0,0.45),
        0 0 0 1px rgba(41,182,246,0.15),
        0 0 40px rgba(21,101,192,0.18);
}
.kpi-card:hover::after { opacity: 1; }

.kpi-icon {
    font-size: 1.85rem;
    margin-bottom: 0.45rem;
    display: block;
    line-height: 1;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #7A9CC4;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-size: 1.95rem;
    font-weight: 900;
    color: #F0F4FF;
    letter-spacing: -0.8px;
    line-height: 1;
    margin-bottom: 0.45rem;
}
.kpi-subtitle {
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 0.2rem;
}

/* ── Section Headers ───────────────────────────────────────────────────── */
.dash-section-header {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.78rem;
    font-weight: 800;
    color: #B0CFEA;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 1rem;
    padding: 0.6rem 0.9rem;
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #1565C0;
    border-radius: 0 8px 8px 0;
}
.dash-section-icon { font-size: 1rem; }

/* ── Card wrapper ───────────────────────────────────────────────────────── */
.dash-card {
    background: rgba(9,18,40,0.70);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.25rem 1.4rem 1.1rem 1.4rem;
    margin-bottom: 0.85rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.30);
}

/* ── Skill Bars ─────────────────────────────────────────────────────────── */
.skill-bar-wrapper  { margin-bottom: 0.95rem; }
.skill-bar-header   { display: flex; justify-content: space-between;
                      align-items: center; margin-bottom: 0.4rem; }
.skill-bar-label    { font-size: 0.86rem; font-weight: 600; color: #D0E8FF; }
.skill-bar-meta     { display: flex; align-items: center; gap: 0.45rem; }
.skill-bar-score    { font-size: 0.8rem; font-weight: 700; color: #7A9CC4; }
.skill-band-badge   {
    font-size: 0.65rem; font-weight: 700;
    padding: 0.1rem 0.5rem;
    border-radius: 4px; border: 1px solid;
    letter-spacing: 0.3px;
}
.skill-bar-track {
    background: rgba(255,255,255,0.06);
    border-radius: 3px;
    height: 8px;
    overflow: hidden;
}
.skill-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.9s cubic-bezier(0.4,0,0.2,1);
}

/* ── Recommendation Panel ──────────────────────────────────────────────── */
.overall-rec-banner {
    background: linear-gradient(135deg, rgba(21,101,192,0.18) 0%, rgba(2,136,209,0.10) 100%);
    border: 1px solid rgba(41,182,246,0.22);
    border-left: 3px solid #29B6F6;
    border-radius: 10px;
    padding: 0.9rem 1.3rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
}
.overall-rec-icon { font-size: 1.3rem; flex-shrink: 0; margin-top: 0.05rem; }
.overall-rec-text { font-size: 0.9rem; color: #C0DCEF; line-height: 1.65; font-style: italic; }

.rec-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0;
    height: 100%;
    box-sizing: border-box;
}
.rec-panel-title {
    font-size: 0.72rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-bottom: 0.8rem;
}
.rec-list  { list-style: none; padding: 0; margin: 0; }
.rec-item  {
    padding: 0.45rem 0.7rem 0.45rem 0.9rem;
    margin-bottom: 0.4rem;
    border-left: 2px solid;
    border-radius: 0 7px 7px 0;
    background: rgba(255,255,255,0.025);
    font-size: 0.84rem; color: #C0DCEF; line-height: 1.55;
    display: flex; align-items: flex-start; gap: 0.4rem;
}
.rec-icon  { flex-shrink: 0; font-size: 0.75rem; margin-top: 0.1rem; }

.step-list { list-style: none; padding: 0; margin: 0; }
.step-item {
    display: flex; align-items: flex-start; gap: 0.7rem;
    padding: 0.5rem 0.7rem;
    margin-bottom: 0.4rem;
    background: rgba(255,255,255,0.025);
    border-radius: 7px;
    font-size: 0.84rem; color: #C0DCEF; line-height: 1.55;
}
.step-num  {
    flex-shrink: 0;
    background: linear-gradient(135deg, #1565C0, #0288D1);
    color: #fff; font-size: 0.68rem; font-weight: 900;
    width: 1.35rem; height: 1.35rem;
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    margin-top: 0.08rem;
    letter-spacing: 0;
}

/* ── Score Gauge Ring (preserved) ──────────────────────────────────────── */
.score-gauge-wrapper {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 0.75rem 0;
}
.score-gauge-ring {
    width: 130px; height: 130px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.1rem; font-weight: 900;
    color: #F0F4FF;
    letter-spacing: -1px;
    margin-bottom: 0.6rem;
    position: relative;
}
.score-gauge-label {
    font-size: 0.75rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; color: #7A9CC4;
}
.score-gauge-tag {
    margin-top: 0.35rem;
    background: rgba(76,175,80,0.18);
    border: 1px solid rgba(76,175,80,0.40);
    border-radius: 4px; padding: 0.18rem 0.75rem;
    font-size: 0.75rem; font-weight: 700; color: #4CAF50;
}
</style>
"""


# ── Internal helpers ──────────────────────────────────────────────────────────

def _section_header(icon: str, title: str) -> None:
    """Renders a styled section divider with icon and title."""
    st.markdown(
        f'<div class="dash-section-header">'
        f'<span class="dash-section-icon">{icon}</span>{title}'
        f'</div>',
        unsafe_allow_html=True,
    )


def _score_colour(score: int) -> tuple[str, str]:
    """Returns (gradient_css, hex_hex) based on the overall score."""
    if score >= 80:
        return "conic-gradient(#4CAF50 0% {p}%, rgba(255,255,255,0.08) {p}% 100%)".format(p=score), "#4CAF50"
    if score >= 60:
        return "conic-gradient(#29B6F6 0% {p}%, rgba(255,255,255,0.08) {p}% 100%)".format(p=score), "#29B6F6"
    if score >= 40:
        return "conic-gradient(#FFA726 0% {p}%, rgba(255,255,255,0.08) {p}% 100%)".format(p=score), "#FFA726"
    return "conic-gradient(#EF5350 0% {p}%, rgba(255,255,255,0.08) {p}% 100%)".format(p=score), "#EF5350"


def _render_header(data: dict) -> None:
    """Renders the top dashboard header strip."""
    st.markdown(
        f"""
        <div class="dash-header">
            <div class="dash-header-left">
                <h2>📊 Interview Performance Dashboard</h2>
                <p>AI-generated analysis for <strong style="color:#F0F4FF;">
                {data['candidate_name']}</strong></p>
            </div>
            <div class="dash-meta-badges">
                <span class="dash-meta-badge role">🎯 {data['target_role']}</span>
                <span class="dash-meta-badge">🎓 {data['experience_level']}</span>
                <span class="dash-meta-badge date">📅 {data['assessment_date']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_row(data: dict) -> None:
    """Renders the four top-level KPI metric tiles."""
    score   = data["overall_score"]
    _, ring_colour = _score_colour(score)

    # Determine delta sentiment
    sentiment = "positive" if score >= 70 else ("neutral" if score >= 50 else "negative")
    band      = data["hiring_recommendation"]
    avg_skill = data["average_skill_score"]

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        render_kpi_card(
            icon="🏆",
            label="Overall Score",
            value=f"{score} / 100",
            subtitle=band,
            delta=sentiment,
        )
    with c2:
        render_kpi_card(
            icon="🎯",
            label="Role Match",
            value=f"{data['skills']['Role Match']:.1f} / 10",
            subtitle="Excellent fit" if data["skills"]["Role Match"] >= 8 else "Good fit",
            delta="positive" if data["skills"]["Role Match"] >= 7 else "neutral",
        )
    with c3:
        render_kpi_card(
            icon="💬",
            label="Avg Skill Score",
            value=f"{avg_skill:.1f} / 10",
            subtitle="Across 5 dimensions",
            delta="neutral",
        )
    with c4:
        render_kpi_card(
            icon="📝",
            label="Questions Answered",
            value=str(len(data["question_scores"])),
            subtitle="All completed",
            delta="positive",
        )


def _render_mid_section(data: dict) -> None:
    """Renders radar chart (left) and skill bars (right) side-by-side."""
    # 7:5 split — radar gets more horizontal space for the polygon
    col_radar, col_bars = st.columns([7, 5], gap="medium")

    with col_radar:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        _section_header("🕸️", "Skill Radar")
        render_radar_chart(
            labels=list(data["skills"].keys()),
            scores=list(data["skills"].values()),
            title="",
            height=460,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bars:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        _section_header("📈", "Category Breakdown")
        for skill, score in data["skills"].items():
            render_skill_bar(label=skill, score=score, max_score=10)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_timeline(data: dict) -> None:
    """Renders the per-question score timeline as a Plotly bar chart."""
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    _section_header("⏱️", "Interview Timeline — Per-Question Score")

    q_labels = data["question_labels"]
    q_scores = data["question_scores"]

    # Per-bar gradient simulation: use a colour list that maps to quality
    bar_colours = [
        "#4CAF50" if s >= 8 else ("#29B6F6" if s >= 6 else "#FFA726")
        for s in q_scores
    ]
    # Slightly lighter top edge to simulate a gradient bar
    bar_colours_light = [
        "#81C784" if s >= 8 else ("#4FC3F7" if s >= 6 else "#FFB74D")
        for s in q_scores
    ]

    fig = go.Figure()

    # Bar trace with richer styling
    fig.add_trace(go.Bar(
        x=q_labels,
        y=q_scores,
        marker=dict(
            color=bar_colours,
            line=dict(color=bar_colours_light, width=1.5),
            cornerradius=6,
            opacity=0.92,
        ),
        text=[f"<b>{s}</b>/10" for s in q_scores],
        textposition="outside",
        textfont=dict(color="#D0E8FF", size=13, family="Inter, sans-serif"),
        hovertemplate=(
            "<b style='font-size:14px'>%{x}</b><br>"
            "Score: <b>%{y}/10</b><extra></extra>"
        ),
        name="Score",
    ))

    # Average benchmark line
    avg = sum(q_scores) / len(q_scores)
    fig.add_hline(
        y=avg,
        line=dict(color="rgba(255,255,255,0.25)", width=1.5, dash="dash"),
        annotation_text=f" Avg  {avg:.1f}",
        annotation_position="top right",
        annotation_font=dict(color="#9EB3D8", size=11, family="Inter, sans-serif"),
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(t=30, b=10, l=10, r=20),
        yaxis=dict(
            range=[0, 12],
            tickvals=[0, 2, 4, 6, 8, 10],
            tickfont=dict(color="#7A9CC4", size=10, family="Inter, sans-serif"),
            gridcolor="rgba(255,255,255,0.05)",
            gridwidth=1,
            zeroline=False,
            showline=False,
        ),
        xaxis=dict(
            tickfont=dict(color="#D0E8FF", size=14, family="Inter, sans-serif"),
            linecolor="rgba(255,255,255,0.08)",
            showline=True,
            linewidth=1,
        ),
        showlegend=False,
        bargap=0.38,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def _render_recommendation_section(data: dict) -> None:
    """Renders the Strengths / Weaknesses / Next Steps panel."""
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    _section_header("🧠", "AI Recommendation Report")

    render_recommendation_panel(
        strengths=data["strengths"],
        weaknesses=data["weaknesses"],
        next_steps=data["next_steps"],
        overall_text=data["overall_text"],
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_footer_cta() -> None:
    """Renders the Start New Assessment CTA footer."""
    st.markdown(
        """
        <div style="
            text-align:center;
            padding: 1rem 0 0.25rem 0;
            border-top: 1px solid rgba(255,255,255,0.06);
            margin-top: 0.5rem;
        ">
            <p style="color:#7A9CC4;font-size:0.84rem;margin-bottom:0.9rem;letter-spacing:0.2px;">
                Ready to level up? Take another assessment to track your progress.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button(
            "🔄 Start New Assessment",
            key="dash_new_assessment_btn",
            type="primary",
            use_container_width=True,
        ):
            # Clear all interview session state so the home page resets
            for key in [
                "interview_questions", "current_q_index",
                "qa_pairs", "evaluation_result", "structured_result",
            ]:
                st.session_state.pop(key, None)
            st.session_state["nav_selection"] = "🏠  Home"
            st.rerun()


# ── Public render function ────────────────────────────────────────────────────

def render_dashboard_page() -> None:
    """
    Main entry-point called by main.py when the Dashboard nav item is active.
    Reads from st.session_state["structured_result"] or falls back to _SAMPLE.
    """
    # Inject dashboard-specific CSS
    st.markdown(_DASHBOARD_CSS, unsafe_allow_html=True)

    # Check if we have real evaluation result in session state
    is_live = "structured_result" in st.session_state
    data = st.session_state.get("structured_result", _SAMPLE)

    # Dummy data notice banner — only visible when no real data exists
    if not is_live:
        st.markdown(
            '<div class="dummy-notice">'
            '⚠️&nbsp;&nbsp;<strong>Sprint 2 Preview</strong> — '
            'Dashboard is displaying sample dummy data. '
            'Gemini integration will be wired in Sprint 3.'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── 1. Header ─────────────────────────────────────────────────────────────
    _render_header(data)

    # ── 2. KPI tiles ──────────────────────────────────────────────────────────
    _render_kpi_row(data)

    # ── 3. Radar + Skill bars ─────────────────────────────────────────────────
    _render_mid_section(data)

    # ── 4. Interview Timeline ─────────────────────────────────────────────────
    _render_timeline(data)

    # ── 5. Recommendation panel ───────────────────────────────────────────────
    _render_recommendation_section(data)

    # ── 6. Footer CTA ─────────────────────────────────────────────────────────
    _render_footer_cta()

