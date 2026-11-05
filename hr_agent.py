# agents/hr_agent.py
from crewai import Agent

def get_hr_agent(llm):
    return Agent(
        role="HR Interviewer",
        goal="Ask behavioral questions to assess culture fit and communication.",
        backstory="HR specialist focused on soft skills and fit.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
