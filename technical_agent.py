# agents/technical_agent.py
from crewai import Agent

def get_technical_agent(llm):
    return Agent(
        role="Technical Interviewer",
        goal="Ask a concise technical interview question relevant to the role and evaluate answers.",
        backstory="Senior backend engineer and system designer.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
