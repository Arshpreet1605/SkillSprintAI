<div align="center">

# ⚡ SkillSprintAI

### AI-Powered Technical Interview Simulation & Skill Assessment Platform

Generate company-specific mock interviews, answer AI-generated questions, receive detailed feedback, and visualize your interview performance through an interactive analytics dashboard.

<img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>

</div>

---

# 📖 Overview

SkillSprintAI is an AI-powered interview preparation platform that simulates realistic technical interviews tailored to a candidate's:

- Resume
- Target Job Role
- Experience Level
- Target Company
- Selected Interview Perspectives

Instead of asking generic interview questions, SkillSprintAI creates personalized interview experiences similar to those conducted by leading technology companies.

After the interview, the platform performs an AI-powered evaluation and displays an interactive performance dashboard with detailed analytics, skill scores, and hiring recommendations.

---

# ✨ Features

## 📄 Resume Analysis

- PDF Resume Upload
- Resume Text Extraction
- Personalized Interview Generation

---

## 🎯 Interview Configuration

Customize interviews using:

- Target Job Role
- Experience Level
- Target Company

Examples:

- Google
- Microsoft
- Amazon
- Meta
- NVIDIA
- Oracle
- Infosys
- Deloitte
- TCS
- Flipkart
- and many more...

---

## 🎤 Multiple Interview Perspectives

Choose one or multiple interview rounds:

- Technical
- HR
- Behavioral
- AI / Machine Learning
- System Design

Questions are intelligently distributed across the selected interview perspectives.

---

## 🤖 AI Interview Generation

Powered by **Google Gemini 2.5 Flash**

Interview questions are generated using:

- Resume
- Job Role
- Company
- Experience
- Interview Perspective

Each interview is unique.

---

## 📝 AI Evaluation

After completing the interview, Gemini evaluates:

- Technical Skills
- Communication
- Problem Solving
- Confidence
- Role Match

The evaluation also includes:

- Overall Score
- Question-wise Scores
- Hiring Recommendation
- Strengths
- Weaknesses
- Personalized Next Steps

---

## 📊 Performance Dashboard

Interactive dashboard including:

- KPI Cards
- Skill Progress Bars
- Radar Chart
- Question-wise Performance
- Hiring Recommendation
- AI Feedback
- Performance Summary

---

# 🖥 Screenshots

> Add screenshots here after deployment.

### 🏠 Home Page

```
images/home.png
```

---

### 🎤 Interview Setup

```
images/interview_setup.png
```

---

### 💬 AI Interview

```
images/interview.png
```

---

### 📊 Dashboard

```
images/dashboard.png
```

---

### 📈 Radar Chart

```
images/radar_chart.png
```

---

# 🏗 Project Architecture

```
                Resume Upload
                      │
                      ▼
              Resume Parser
                      │
                      ▼
          Interview Configuration
      (Role + Company + Perspective)
                      │
                      ▼
        Google Gemini 2.5 Flash
      Generates Interview Questions
                      │
                      ▼
              Candidate Answers
                      │
                      ▼
        Google Gemini Evaluation
                      │
                      ▼
          Structured JSON Response
                      │
                      ▼
         Interactive Dashboard
```

---

# 📂 Project Structure

```
SkillSprintAI/

│
├── app/
│   │
│   ├── config/
│   │
│   ├── ui/
│   │   ├── components/
│   │   └── pages/
│   │
│   └── utils/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI

- Google Gemini 2.5 Flash

### Data Visualization

- Plotly

### Libraries

- pdfplumber
- python-dotenv
- google-generativeai
- streamlit
- plotly

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SkillSprintAI.git
```

Move into the project

```bash
cd SkillSprintAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run main.py
```

---

# 💡 Future Improvements

- Voice Interview
- Video Interview
- Coding Round
- Live Code Editor
- ATS Resume Score
- PDF Performance Report
- Interview History
- Authentication
- Cloud Deployment
- Multi-language Support
- AI Career Coach

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👩‍💻 Authors

**Arshpreet Kaur**

M.Sc. Data Science | Student | Data Science Enthusiast

 **Priya**
 
B.E(IT) | Student | AI/ML Enthusiast

GitHub:
https://github.com/Arshpreet1605

---

<div align="center">

⭐ If you like this project, consider giving it a Star!

</div>
