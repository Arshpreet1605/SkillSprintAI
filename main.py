"""
main.py
--------
SkillSprint AI — Streamlit application entry point.

Run with:
    streamlit run main.py
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="SkillSprint AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-org/skillsprint-ai",
        "Report a bug": "https://github.com/your-org/skillsprint-ai/issues",
        "About": "SkillSprint AI — AI-Powered Interview Simulation Platform",
    },
)

# ── Internal imports (after set_page_config) ──────────────────────────────────
from app.ui.styles import CUSTOM_CSS
from app.ui.components.sidebar import render_sidebar
from app.ui.pages.home import render_home_page
from app.ui.pages.about import render_about_page
from app.ui.pages.contact import render_contact_page

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar + routing ─────────────────────────────────────────────────────────
active_page = render_sidebar()

if "Home" in active_page:
    render_home_page()
elif "About" in active_page:
    render_about_page()
elif "Contact" in active_page:
    render_contact_page()
