# crew_setup.py — SAFE VERSION (no native Gemini required)
from crewai import Crew, Agent, Task, LLM
import os
from dotenv import load_dotenv
import json

load_dotenv()

# ---------------------------------------------------------
#  SAFE GEMINI LLM (Prevents native Google GenAI import)
# ---------------------------------------------------------
llm = LLM(
    model=os.getenv("CREWAI_MODEL", "gemini/gemini-flash-lite-latest"),
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
    use_native=False   # <<< THIS IS THE CRITICAL FIX
)

# ---------------------------------------------------------
#  FOUR INTERVIEWER AGENTS
# ---------------------------------------------------------

def get_technical_agent():
    return Agent(
        role="Technical Interviewer",
        goal="Ask deep technical and coding questions.",
        backstory="A senior engineer evaluating coding, systems, and algorithms.",
        llm=llm,
        allow_delegation=False
    )

def get_conceptual_agent():
    return Agent(
        role="Conceptual Interviewer",
        goal="Ask theory & conceptual CS questions.",
        backstory="A computer science professor testing fundamentals.",
        llm=llm,
        allow_delegation=False
    )

def get_problem_agent():
    return Agent(
        role="Problem-Solving Interviewer",
        goal="Ask algorithmic and reasoning-based questions.",
        backstory="A coding mentor evaluating logic and approach.",
        llm=llm,
        allow_delegation=False
    )

def get_hr_agent():
    return Agent(
        role="HR Interviewer",
        goal="Ask behavioural and communication questions.",
        backstory="An HR expert testing soft skills and mindset.",
        llm=llm,
        allow_delegation=False
    )

# ---------------------------------------------------------
#  TASK DEFINITIONS
# ---------------------------------------------------------

def ask_question_task(agent, branch, role, history):
    history_text = "\n".join(
        [f"Q: {h['question']}\nA: {h.get('answer', '')}" for h in history[-3:]]
    ) if history else "No previous questions."

    return Task(
        agent=agent,
        description=f"""
Ask ONLY ONE interview question for:

Role: {role}
Branch: {branch}

Recent history:
{history_text}

Rules:
- Output ONLY the question text.
- No explanation.
- No numbering.
""",
        expected_output="A single interview question."
    )


def evaluate_answer_task(agent, question, answer):
    return Task(
        agent=agent,
        description=f"""
Evaluate the candidate's answer STRICTLY.

Question: {question}
Answer: {answer}

Return ONLY valid JSON:
{{
  "feedback": "short constructive feedback",
  "follow_up": "follow-up question or empty string"
}}
""",
        expected_output="JSON with 'feedback' and 'follow_up'."
    )

# ---------------------------------------------------------
#  EXECUTION HELPERS
# ---------------------------------------------------------

def run_agent_ask(agent, branch, role, history):
    """Runs the ask-question task and returns question as string."""
    crew = Crew(
        agents=[agent],
        tasks=[ask_question_task(agent, branch, role, history)],
        verbose=False
    )
    return str(crew.kickoff()).strip()


def run_agent_evaluate(agent, question, answer):
    """Runs evaluation task and extracts JSON feedback."""
    crew = Crew(
        agents=[agent],
        tasks=[evaluate_answer_task(agent, question, answer)],
        verbose=False
    )
    output = str(crew.kickoff())

    # Extract JSON safely
    try:
        start = output.index("{")
        end = output.rindex("}")
        data = json.loads(output[start:end+1])
        return data.get("feedback", ""), data.get("follow_up", "")
    except:
        return (
            "Good attempt! Try giving more structured and detailed points.",
            ""
        )
