"""
app/utils/gemini_client.py
----------------------------
Handles communication with the Gemini API:
  - generate_interview_questions: returns a list of tailored questions
  - evaluate_interview_answers: returns a strengths/weaknesses summary
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_interview_questions(resume_text: str, role: str, experience: str) -> list[str]:
    """
    Returns a list of 5 interview question strings, tailored to the resume,
    target role, and experience level.
    """
    prompt = f"""
You are an experienced technical interviewer.

Candidate's resume:
{resume_text}

Target role: {role}
Experience level: {experience}

Generate exactly 5 interview questions tailored to this candidate's
background, skills, and the target role.

Respond with ONLY a valid JSON array of 5 strings, nothing else.
Example format: ["question 1", "question 2", "question 3", "question 4", "question 5"]
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Clean up in case Gemini wraps it in markdown code fences
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError:
        questions = [raw]  # fallback: treat whole response as one question

    return questions


def evaluate_interview_answers(resume_text: str, role: str, experience: str, qa_pairs: list[dict]) -> str:
    """
    Sends all question-answer pairs to Gemini and returns a strengths/weaknesses
    summary as plain text.
    qa_pairs format: [{"question": "...", "answer": "..."}, ...]
    """
    qa_text = "\n\n".join(
        f"Q{i+1}: {pair['question']}\nA{i+1}: {pair['answer']}"
        for i, pair in enumerate(qa_pairs)
    )

    prompt = f"""
You are an experienced technical interviewer evaluating a candidate.

Candidate's resume:
{resume_text}

Target role: {role}
Experience level: {experience}

Here are the interview questions and the candidate's answers:
{qa_text}

Based on these answers, provide a concise overall summary covering:
1. Key strengths shown in the answers
2. Areas for improvement / weaknesses
3. One overall recommendation

Keep it structured and to the point.
"""
    response = model.generate_content(prompt)
    return response.text