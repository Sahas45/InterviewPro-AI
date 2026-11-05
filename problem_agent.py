# agents/problem_agent.py
from crewai import Agent

def get_problem_agent(llm):
    return Agent(
        role="Problem-Solving Interviewer",
        goal="Ask a clear algorithmic/problem-solving question and evaluate solution approaches.",
        backstory="Algorithm coach used to evaluate correctness and complexity.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
