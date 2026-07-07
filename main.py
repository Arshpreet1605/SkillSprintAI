"""
main.py
--------
SkillSprint AI — Streamlit application entry point.

Run with:
    streamlit run main.py
"""

import streamlit as st
import pdfplumber
from docx import Document
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
from app.ui.pages.home      import render_home_page
from app.ui.pages.dashboard import render_dashboard_page
from app.ui.pages.about     import render_about_page
from app.ui.pages.contact   import render_contact_page

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar + routing ─────────────────────────────────────────────────────────
active_page = render_sidebar()

if "Home" in active_page:
    render_home_page()
elif "Dashboard" in active_page:
    render_dashboard_page()
elif "About" in active_page:
    render_about_page()
elif "Contact" in active_page:
    render_contact_page()

# main.py


# # ---- Helper functions (put these near the top, after imports) ----
# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     with pdfplumber.open(uploaded_file) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# def extract_text_from_docx(uploaded_file):
#     doc = Document(uploaded_file)
#     return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# def extract_resume_text(uploaded_file):
#     file_type = uploaded_file.name.split(".")[-1].lower()
#     if file_type == "pdf":
#         return extract_text_from_pdf(uploaded_file)
#     elif file_type == "docx":
#         return extract_text_from_docx(uploaded_file)
#     else:
#         st.error("Unsupported file type. Please upload a PDF or DOCX.")
#         return None

# # ---- Your existing Streamlit UI code goes below ----
# st.title("Interview Simulator")  # or whatever your title already is

# uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

# if uploaded_file is not None:
#     resume_text = extract_resume_text(uploaded_file)
#     if resume_text:
#         st.success("Resume parsed successfully!")
#         with st.expander("Preview extracted text"):
#             st.text(resume_text)
#         # next: pass resume_text into your Gemini call



