"""
app/ui/styles.py
----------------
All custom CSS injected into Streamlit via st.markdown().
Keeps styling completely separate from layout/logic.
"""

CUSTOM_CSS = """
<style>
/* ── Google Fonts ────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ──────────────────────────────────────────────────── */
:root {
    --primary:        #1565C0;
    --primary-light:  #1E88E5;
    --primary-dark:   #0D47A1;
    --accent:         #29B6F6;
    --bg-dark:        #0A0F1E;
    --bg-card:        rgba(255, 255, 255, 0.05);
    --bg-card-hover:  rgba(255, 255, 255, 0.09);
    --text-primary:   #F0F4FF;
    --text-secondary: #9EB3D8;
    --border:         rgba(255, 255, 255, 0.10);
    --gradient:       linear-gradient(135deg, #1565C0 0%, #0288D1 50%, #0097A7 100%);
    --glow:           0 0 40px rgba(21, 101, 192, 0.35);
}

/* ── Global Reset ────────────────────────────────────────────────────── */
/* NOTE: [class*="css"] removed — it matched Streamlit's internal class names
   and forced color:#F0F4FF onto selectbox value spans, making text invisible. */
html, body {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}
/* Apply font family broadly without touching color, so widget text is unaffected */
* { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: var(--bg-dark) !important; }

/* ── Hide Streamlit Branding ─────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Streamlit Main Block Padding ────────────────────────────────────── */
.block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 860px !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B3E 0%, #0A0F1E 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Hero Banner ─────────────────────────────────────────────────────── */
.hero-banner {
    background: var(--gradient);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: var(--glow);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
    animation: shimmer 6s ease-in-out infinite;
}
@keyframes shimmer {
    0%, 100% { transform: translate(0, 0); }
    50%       { transform: translate(10%, 10%); }
}
.hero-icon   { font-size: 3.5rem; margin-bottom: 0.5rem; }
.hero-title  {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #fff !important;
    margin: 0 0 0.75rem 0;
}
.hero-tagline {
    font-size: 1.05rem;
    font-weight: 400;
    color: rgba(255,255,255,0.82) !important;
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Section Card ────────────────────────────────────────────────────── */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(12px);
    transition: background 0.25s ease, box-shadow 0.25s ease;
}
.section-card:hover {
    background: var(--bg-card-hover);
    box-shadow: 0 4px 24px rgba(21, 101, 192, 0.18);
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent) !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Streamlit Widgets ───────────────────────────────────────────────── */
/* Selectbox container */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
/* Selected value text — must be set explicitly; the old [class*="css"] rule
   was overriding this with a conflicting background-matched colour. */
div[data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"] span,
div[data-baseweb="select"] > div > div > div,
div[data-baseweb="select"] > div span {
    color: var(--text-primary) !important;
}
/* Dropdown arrow */
div[data-baseweb="select"] svg { fill: var(--accent) !important; }
/* Dropdown list */
div[data-baseweb="popover"] {
    background: #0D1B3E !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
div[data-baseweb="menu"] li {
    color: var(--text-primary) !important;
    background: transparent !important;
}
div[data-baseweb="menu"] li:hover,
div[data-baseweb="menu"] [aria-selected="true"] {
    background: rgba(21, 101, 192, 0.35) !important;
    color: #fff !important;
}

/* File Uploader */
section[data-testid="stFileUploadDropzone"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(41, 182, 246, 0.4) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease;
}
section[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--accent) !important;
}

/* Labels */
label[data-testid="stWidgetLabel"] p {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px;
}

/* ── Primary Button ("Start Assessment") ─────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--gradient) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #fff !important;
    padding: 0.75rem 2.5rem !important;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 18px rgba(21, 101, 192, 0.5) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    width: 100%;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(21, 101, 192, 0.65) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

/* ── Secondary Buttons ────────────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    transition: background 0.2s ease !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.12) !important;
}

/* ── Sidebar Nav Buttons ──────────────────────────────────────────────── */
.nav-btn {
    display: block;
    width: 100%;
    padding: 0.65rem 1rem;
    margin-bottom: 0.4rem;
    background: transparent;
    border: none;
    border-radius: 10px;
    color: var(--text-secondary) !important;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: left;
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
}
.nav-btn:hover, .nav-btn.active {
    background: rgba(21, 101, 192, 0.25) !important;
    color: #fff !important;
}

/* ── Feature Badges (stats row) ──────────────────────────────────────── */
.badge-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}
.badge {
    background: rgba(255,255,255,0.07);
    border: 1px solid var(--border);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--accent) !important;
}

/* ── Validation Toast ────────────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-weight: 500 !important;
}

/* ── Divider ─────────────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Scrollbar ───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 6px; }
</style>
"""
