# InterviewPro AI — Multi-Agent AI Interview Preparation Platform

**An GenAI-powered interview preparation platform built using CrewAI, Google Gemini, and Streamlit.**

🔗 **Live Demo:** https://interviewpro-ai-sahas45.streamlit.app/

## Overview
InterviewPro AI is an intelligent interview preparation platform that simulates real interview experiences using multiple specialized AI agents.

Candidates can practice role-specific interviews, submit answers, receive AI-generated feedback, and answer follow-up questions to improve their interview performance.

## ✨ Key Features

- **Technical Interview Agent:** Evaluates technical knowledge.
- **Conceptual Interview Agent:** Tests understanding of core concepts.
- **Problem-Solving Agent:** Assesses analytical and logical thinking.
- **HR Interview Agent:** Simulates HR interview questions.
- **AI-Powered Evaluation:** Provides feedback on candidate answers.
- **Dynamic Follow-up Questions:** Generates relevant follow-up questions.
- **Role-Based Preparation:** Supports customized interview preparation.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| CrewAI | Multi-agent orchestration |
| Google Gemini | Large Language Model |
| python-dotenv | Environment configuration |

## 🏗️ Project Architecture

The application uses multiple specialized AI agents coordinated through CrewAI.

Candidate → Streamlit UI → CrewAI → Specialized AI Agents → Gemini → Evaluation & Feedback

## 📂 Project Structure

```text
InterviewPro-AI/
│
├── app.py
├── crew_setup.py
├── question_generator.py
├── technical_agent.py
├── concept_agent.py
├── problem_agent.py
├── hr_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Sahas45/InterviewPro-AI.git
cd InterviewPro-AI
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment (Windows)**

```bash
venv\Scripts\activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Configure environment variables**

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-flash-lite-latest
```

**6. Run the application**

```bash
streamlit run app.py
```

## 🔐 Security

- API keys are stored using environment variables or Streamlit Secrets.
- Sensitive credentials are excluded from GitHub.
- Never commit your `.env` file or expose API keys publicly.

## 🌐 Deployment

Deployed using **Streamlit Community Cloud**.

👉 https://interviewpro-ai-sahas45.streamlit.app/

## 👨‍💻 Author

**Sahas Bhosale**

GitHub: https://github.com/Sahas45

-
