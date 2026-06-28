"""
app/config/settings.py
----------------------
Central configuration for SkillSprint AI.
All tuneable values live here so the rest of the app stays clean.
"""

# ── Application Meta ────────────────────────────────────────────────────────
APP_NAME        = "SkillSprint AI"
APP_TAGLINE     = "AI-Powered Technical Interview Simulation & Skill Assessment Platform"
APP_VERSION     = "0.1.0"
APP_ICON        = "⚡"          # Streamlit page icon

# ── Role Options (dropdown) ─────────────────────────────────────────────────
ROLE_OPTIONS = [
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
]

# ── Experience Level Options (dropdown) ─────────────────────────────────────
EXPERIENCE_OPTIONS = [
    "Student",
    "Fresher",
    "1–2 Years",
]

# ── File Upload ──────────────────────────────────────────────────────────────
ALLOWED_FILE_TYPES = ["pdf"]
MAX_FILE_SIZE_MB   = 5

# ── Sidebar Navigation ───────────────────────────────────────────────────────
NAV_ITEMS = ["🏠  Home", "ℹ️  About", "✉️  Contact"]
