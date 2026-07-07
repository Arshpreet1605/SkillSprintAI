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

    # -----------------------
    # Data & AI
    # -----------------------
    "Data Analyst",
    "Business Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Generative AI Engineer",
    "Data Engineer",
    "BI Developer",

    # -----------------------
    # Software Development
    # -----------------------
    "Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Python Developer",
    "Java Developer",

    # -----------------------
    # Cloud & DevOps
    # -----------------------
    "Cloud Engineer",
    "DevOps Engineer",
    "Site Reliability Engineer",

    # -----------------------
    # Cybersecurity
    # -----------------------
    "Cybersecurity Analyst",
    "Security Engineer",

    # -----------------------
    # QA
    # -----------------------
    "QA Engineer",
    "Automation Test Engineer",

    # -----------------------
    # Product & Design
    # -----------------------
    "Product Manager",
    "UI/UX Designer",
]
# ── Company Options (dropdown) ───────────────────────────────────────────────
COMPANY_OPTIONS = [
    "Google",
    "Microsoft",
    "Amazon",
    "OpenAI",
    "Anthropic",
    "NVIDIA",
    "Meta",
    "Apple",
    "Adobe",
    "Databricks",
    "Snowflake",
    "Oracle",
    "Salesforce",
    "IBM",
    "Intel",
    "Cisco",
    "Accenture",
    "Deloitte",
    "EY",
    "PwC",
    "KPMG",
    "Infosys",
    "TCS",
    "Wipro",
    "HCLTech",
    "Capgemini",
    "Cognizant",
    "Tech Mahindra",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "PhonePe",
    "Paytm",
    "Razorpay",
    "Meesho",
    "Other"
]
# ── Interview Perspectives ───────────────────────────────────────────────

INTERVIEW_PERSPECTIVES = [
    "Technical",
    "AI / ML",
    "DSA",
    "System Design",
    "Behavioral",
    "HR",
]
# ── Experience Level Options (dropdown) ─────────────────────────────────────
EXPERIENCE_OPTIONS = [
    "Student",
    "Fresher",
    "1–2 Years",
    "3–5 Years",
    "5+ Years",
]

# ── File Upload ──────────────────────────────────────────────────────────────
ALLOWED_FILE_TYPES = ["pdf"]
MAX_FILE_SIZE_MB   = 5

# ── Sidebar Navigation ───────────────────────────────────────────────────────
NAV_ITEMS = ["🏠  Home", "📊  Dashboard", "ℹ️  About", "✉️  Contact"]
