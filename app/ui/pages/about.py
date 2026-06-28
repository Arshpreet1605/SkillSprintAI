"""
app/ui/pages/about.py
----------------------
About page — describes the platform, tech stack, and team.
No interactive elements in Sprint 1.
"""

import streamlit as st
from app.config.settings import APP_NAME, APP_TAGLINE


def render_about_page() -> None:
    """Renders the About page content."""

    # ── Page header ──────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="margin-bottom:2rem;">
            <h2 style="font-size:2rem;font-weight:800;color:#F0F4FF;
                       margin-bottom:0.4rem;">About {APP_NAME}</h2>
            <p style="color:#9EB3D8;font-size:1rem;">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Mission card ─────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="section-card">
            <div class="card-title">🎯 Our Mission</div>
            <p style="color:#C8D8EF;line-height:1.8;">
                SkillSprint AI bridges the gap between learning and landing a job.
                We simulate realistic interview scenarios — HR, Technical, and
                Scenario-based — personalised to your resume and target role,
                so you can walk into any interview room with confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature grid ─────────────────────────────────────────────────────
    st.markdown(
        """<div class="card-title" style="margin-top:1.5rem;">
               ✨ Core Features</div>""",
        unsafe_allow_html=True,
    )

    features = [
        ("📄", "Resume Upload & Parsing", "PDF resume parsed automatically to extract your skills and experience."),
        ("🎯", "Role-Specific Questions",  "Questions tailored to Data Analyst, Data Scientist, and ML Engineer roles."),
        ("🧠", "AI-Powered Evaluation",    "Google Gemini API evaluates your answers in real-time."),
        ("🏢", "3 Interview Rounds",        "HR, Technical, and Scenario-based rounds — just like the real thing."),
        ("📊", "Performance Dashboard",     "Visual breakdown of your performance with actionable feedback."),
        ("🔒", "Privacy First",             "Your resume is processed locally — we never store personal data."),
    ]

    col1, col2 = st.columns(2, gap="medium")
    for idx, (icon, title, desc) in enumerate(features):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(
                f"""
                <div class="section-card" style="min-height:120px;">
                    <div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-weight:700;color:#F0F4FF;
                                margin-bottom:0.3rem;">{title}</div>
                    <div style="font-size:0.85rem;color:#9EB3D8;
                                line-height:1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Tech stack ────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="section-card" style="margin-top:1rem;">
            <div class="card-title">🛠️ Tech Stack</div>
            <div style="display:flex;flex-wrap:wrap;gap:0.75rem;">
                <span class="badge">🐍 Python</span>
                <span class="badge">🌐 Streamlit</span>
                <span class="badge">✨ Gemini API</span>
                <span class="badge">📑 PyMuPDF</span>
                <span class="badge">🐼 Pandas</span>
                <span class="badge">📈 Plotly</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
