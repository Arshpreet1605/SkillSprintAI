"""
app/ui/pages/home.py
---------------------
Landing page (Home) for SkillSprint AI.

Responsibilities (Sprint 1 scope):
  - Hero banner with title & tagline
  - Resume upload (PDF only — stored in session state for later)
  - Role selection dropdown
  - Experience level dropdown
  - "Start Assessment" button with validation feedback
"""

from streamlit import delta_generator_singletons
import streamlit as st
from app.utils.resume_parser import extract_resume_text
from app.utils.gemini_client import generate_interview_questions, evaluate_interview_answers
from app.config.settings import (
    APP_NAME,
    APP_TAGLINE,
    APP_ICON,
    ROLE_OPTIONS,
    COMPANY_OPTIONS,
    INTERVIEW_PERSPECTIVES,
    EXPERIENCE_OPTIONS,
    ALLOWED_FILE_TYPES,
    MAX_FILE_SIZE_MB,
)


# ── Helper: section card wrapper ─────────────────────────────────────────────

def _card_open(title: str) -> None:
    """Renders the opening HTML of a styled card section."""
    st.markdown(
        f"""
        <div class="section-card">
            <div class="card-title">{title}</div>
        """,
        unsafe_allow_html=True,
    )


def _card_close() -> None:
    """Closes a card section."""
    st.markdown("</div>", unsafe_allow_html=True)


# ── Hero banner ──────────────────────────────────────────────────────────────

def _render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-icon">{APP_ICON}</div>
            <h1 class="hero-title">{APP_NAME}</h1>
            <p class="hero-tagline">{APP_TAGLINE}</p>
            <div class="badge-row">
                <span class="badge">🧠 AI-Powered</span>
                <span class="badge">📄 Resume Analysis</span>
                <span class="badge">💼 3 Interview Rounds</span>
                <span class="badge">📊 Performance Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Resume upload card ────────────────────────────────────────────────────────

def _render_resume_upload() -> None:
    st.markdown(
        """
        <div class="section-card">
            <div class="card-title">📄 Resume Upload</div>
        """,
        unsafe_allow_html=True,
    )

    # FIX 1: Use key="resume_file" ONLY as the widget binding.
    # Never write st.session_state["resume_file"] = ... manually while the
    # widget is alive — that causes a StreamlitAPIException / silent reset.
    # Instead, maintain a SEPARATE boolean flag "resume_valid" that tracks
    # whether the current upload passed validation.
    uploaded_file = st.file_uploader(
        label="Upload your resume (PDF, max 5 MB)",
        type=ALLOWED_FILE_TYPES,
        help="We support PDF format only. Your file is processed locally.",
        key="resume_file",
    )

    if uploaded_file is not None:
        file_size_mb = round(uploaded_file.size / (1024 * 1024), 2)

        if file_size_mb > MAX_FILE_SIZE_MB:
            # FIX 3: Mark as invalid — do NOT touch the widget key.
            st.session_state["resume_valid"] = False
            st.error(
                f"⚠️ File too large ({file_size_mb} MB). "
                f"Please upload a file under {MAX_FILE_SIZE_MB} MB."
            )
        else:
            # Valid upload — set the flag that gates the dropdowns.
            st.session_state["resume_valid"] = True
            st.session_state["resume_text"] = extract_resume_text(uploaded_file)
            st.success(
                f"✅ **{uploaded_file.name}** uploaded successfully "
                f"({file_size_mb} MB)"
            )
    else:
        # FIX 3: File was removed/not yet uploaded — reset flag so dropdowns
        # go back to disabled state correctly.
        st.session_state["resume_valid"] = False

    st.markdown("</div>", unsafe_allow_html=True)


# ── Role & experience selectors ──────────────────────────────────────────────

def _render_selectors() -> None:
    st.markdown(
        """
        <div class="section-card">
            <div class="card-title">🎯 Assessment Configuration</div>
        """,
        unsafe_allow_html=True,
    )

    # FIX 2: Gate both dropdowns on the validated upload flag.
    # disabled=True renders them greyed-out until a valid PDF is present.
    resume_valid = st.session_state.get("resume_valid", False)

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.selectbox(
            label="Target Job Role",
            options=ROLE_OPTIONS,
            key="selected_role",
            help="Upload a valid resume to enable this.",
            disabled=not resume_valid,
        )

    with col_right:
        st.selectbox(
            label="Experience Level",
            options=EXPERIENCE_OPTIONS,
            key="selected_experience",
            help="Upload a valid resume to enable this.",
            disabled=not resume_valid,
        )
# ---------------- Row 2 ----------------
    st.selectbox(
        label="Target Company",
        options=COMPANY_OPTIONS,
        key="selected_company",
        help="Choose the company you are preparing for.",
        disabled=not resume_valid,
    )
    st.markdown("### 🎤 Interview Perspectives")

    selected_perspectives = []

    cols = st.columns(3)

    for i, perspective in enumerate(INTERVIEW_PERSPECTIVES):
        with cols[i % 3]:
            if st.checkbox(
                perspective,
                key=f"perspective_{perspective}",
                disabled=not resume_valid,
            ):
                selected_perspectives.append(perspective)

    st.session_state["selected_perspectives"] = selected_perspectives
    if not resume_valid:
        st.caption("⬆️ Upload a valid PDF resume above to enable the dropdowns.")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Start Assessment button ──────────────────────────────────────────────────
def _render_start_button() -> None:
    st.markdown("<br>", unsafe_allow_html=True)

    resume_valid = st.session_state.get("resume_valid", False)
    role         = st.session_state.get("selected_role", "")
    experience   = st.session_state.get("selected_experience", "")
    company = st.session_state.get("selected_company", "")
    perspectives = st.session_state.get("selected_perspectives", [])
    ready = (
    resume_valid
    and bool(role)
    and bool(experience)
    and bool(company)
    and len(perspectives) > 0
)

    # Only show the Start button if the interview hasn't started yet
    if "interview_questions" not in st.session_state:
        clicked = st.button(
            "🚀  Start Assessment",
            type="primary",
            key="start_assessment_btn",
            disabled=not ready,
        )

        if clicked:
            st.session_state.pop("structured_result", None)
            resume_text = st.session_state.get("resume_text", "")
            if not resume_valid or not resume_text:
                st.warning("⚠️ Please upload your resume before starting the assessment.")
            else:
                with st.spinner("Generating your interview questions..."):
                    questions = generate_interview_questions(
                        resume_text,
                        role,
                        experience,
                        company,
                        perspectives,
                    )               
                st.session_state["interview_questions"] = questions
                st.session_state["current_q_index"] = 0
                st.session_state["qa_pairs"] = []
                st.rerun()


def _render_interview_flow() -> None:
    """Shows one question at a time, collects answers, then shows results."""
    if "interview_questions" not in st.session_state:
        return  # interview hasn't started yet

    questions = st.session_state["interview_questions"]
    index = st.session_state["current_q_index"]

    # ── Interview finished — show results ──────────────────────────────
    if index >= len(questions):
        if "structured_result" not in st.session_state:
            resume_text = st.session_state.get("resume_text", "")
            role = st.session_state.get("selected_role", "")
            experience = st.session_state.get("selected_experience", "")
            company = st.session_state.get("selected_company", "")
            perspectives = st.session_state.get("selected_perspectives", [])
            qa_pairs = st.session_state.get("qa_pairs", [])

            with st.spinner("Evaluating your answers..."):
                result = evaluate_interview_answers(resume_text, role, experience,company,perspectives, qa_pairs)
            st.session_state["structured_result"] = result

        # Redirect directly to the newly generated Performance Dashboard page
        st.session_state["nav_selection"] = "📊  Dashboard"
        st.rerun()
        return

    # ── Show current question ──────────────────────────────────────────
    st.markdown("---")
    st.subheader(f"Question {index + 1} of {len(questions)}")
    st.write(questions[index])

    answer = st.text_area("Your answer", key=f"answer_{index}")

    if st.button("Submit Answer", key=f"submit_{index}"):
        st.session_state["qa_pairs"].append({
            "question": questions[index],
            "answer": answer,
        })
        st.session_state["current_q_index"] += 1
        st.rerun()
# ── Public render function ────────────────────────────────────────────────────

def render_home_page() -> None:
    """
    Main entry-point called by main.py when the Home nav item is active.
    Composes all sections of the landing page in order.
    """
    
    _render_hero()
    _render_resume_upload()
    _render_selectors()
    _render_start_button()
    _render_interview_flow()