# agents/concept_agent.py
from crewai import Agent

def get_concept_agent(llm):
    return Agent(
        role="Conceptual Interviewer",
        goal="Ask conceptual and theory-based questions about fundamentals and trade-offs.",
        backstory="Experienced lecturer focusing on fundamentals.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
