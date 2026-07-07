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


def generate_interview_questions(resume_text: str, role: str, experience: str,company:str,perspectives:list[str]) -> list[str]:
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
Target company: {company}

Interview perspectives:
{", ".join(perspectives)}

Generate exactly FIVE interview questions.

The questions should be tailored to:

- Candidate's resume
- Selected target role
- Selected experience level
- Selected company
- ONLY the selected interview perspectives.

If Technical is selected, ask technical conceptual interview questions. Do not ask the candidate to write code.
If HR is selected, ask HR interview questions.

If Behavioral is selected, ask behavioral questions.

If AI/ML is selected, ask AI/ML interview questions.

If System Design is selected, ask system design interview questions.

Distribute the five questions naturally across the selected interview perspectives.

The interview style should resemble the interview process of the selected company.

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


def evaluate_interview_answers(resume_text: str, role: str, experience: str,company:str,perspectives:list[str], qa_pairs: list[dict]) -> dict:
    """
    Sends all question-answer pairs to Gemini and returns structured
    interview performance analytics matching our dashboard schema.
    """
    from datetime import datetime
    assessment_date = datetime.now().strftime("%B %d, %Y")

    qa_text = "\n\n".join(
        f"Q{i+1}: {pair['question']}\nA{i+1}: {pair['answer']}"
        for i, pair in enumerate(qa_pairs)
    )

    prompt = f"""
You are an experienced technical interviewer evaluating a candidate's responses.

Candidate's resume:
{resume_text}

Target role: {role}
Experience level: {experience}
Target company: {company}
Interview perspectives:
{', '.join(perspectives)}

Here are the interview questions and the candidate's answers:
{qa_text}

The interview questions were generated according to the selected company and interview perspectives.

Evaluate the candidate only on the basis of the selected interview perspectives and the answers provided.

Evaluate ONLY the interview perspectives that were selected.

Do not reduce the candidate's score for perspectives that were not selected.

Do not evaluate skills that were not covered during the interview.

Based on the resume and the candidate's actual answers, perform a rigorous evaluation and generate the performance analytics. All scores (overall, individual skills, and individual questions) must be realistic and proportional to the quality of the candidate's answers and their alignment with the target role. Do not use generic or static placeholders.
The evaluation should reflect the interview standards and expectations of the selected company.
If a skill was not evaluated because the corresponding interview perspective was not selected, assign a neutral score instead of inventing evidence.

Generate a valid JSON object matching the following structure:
{{
  "candidate_name": "extracted candidate name or 'Candidate' if not found",
  "target_role": "{role}",
  "experience_level": "{experience}",
  "assessment_date": "{assessment_date}",
  "overall_score": 75, // integer between 0 and 100
  "average_skill_score": 7.3, // float between 0.0 and 10.0 (average of the 5 skill scores below)
  "hiring_recommendation": "Strong Candidate", // one of: 'Strong Candidate', 'Pass', 'Pass with Reservations', 'Needs Improvement'
  "skills": {{
    "Technical Skills": 7.5, // float between 0.0 and 10.0
    "Communication": 7.0, // float between 0.0 and 10.0
    "Problem Solving": 7.2, // float between 0.0 and 10.0
    "Confidence": 6.8, // float between 0.0 and 10.0
    "Role Match": 8.0 // float between 0.0 and 10.0
  }},
  "question_scores": [7.0, 8.0, 6.0, 9.0, 7.0], // list of exactly 5 floats between 0.0 and 10.0 representing the score for Q1 to Q5
  "strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "weaknesses": [
    "weakness 1",
    "weakness 2"
  ],
  "next_steps": [
    "next step 1",
    "next step 2",
    "next step 3"
  ],
  "overall_text": "A descriptive summary paragraph explaining the strengths, weaknesses, and recommendation."
}}

Respond with ONLY the valid JSON object, nothing else. Do not wrap it in any formatting other than the JSON itself.
"""
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "candidate_name": "Candidate",
            "target_role": role,
            "experience_level": experience,
            "assessment_date": assessment_date,
            "overall_score": 50,
            "average_skill_score": 5.0,
            "hiring_recommendation": "Needs Review",
            "skills": {
                "Technical Skills": 5.0,
                "Communication": 5.0,
                "Problem Solving": 5.0,
                "Confidence": 5.0,
                "Role Match": 5.0,
            },
            "question_scores": [5.0, 5.0, 5.0, 5.0, 5.0],
            "strengths": ["Completed the assessment."],
            "weaknesses": ["Evaluation decoding failed."],
            "next_steps": ["Retry the assessment."],
            "overall_text": "We were unable to parse the AI evaluation response. Please retry."
        }

    # Ensure dynamic computation of average score is mathematically correct
    if "skills" in data and isinstance(data["skills"], dict):
        vals = [float(v) for v in data["skills"].values() if isinstance(v, (int, float))]
        if vals:
            data["average_skill_score"] = round(sum(vals) / len(vals), 1)
    if "question_labels" not in data:
        data["question_labels"] = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    return data