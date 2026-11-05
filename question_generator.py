
from crew_setup import (
    get_technical_agent,
    get_conceptual_agent,
    get_problem_agent,
    get_hr_agent,
    run_agent_ask,
    run_agent_evaluate
)

# Four specialized interviewer agents
AGENTS = [
    ("Technical Interviewer", get_technical_agent),
    ("Conceptual Interviewer", get_conceptual_agent),
    ("Problem-Solving Interviewer", get_problem_agent),
    ("HR Interviewer", get_hr_agent),
]


def start_interview(branch, role):
    session = {
        "branch": branch,
        "role": role,
        "history": [],
        "current_agent_index": 0,
        "completed": False
    }

    agent_name, agent_fn = AGENTS[0]
    agent = agent_fn()

    first_question = run_agent_ask(
        agent, branch, role, session["history"]
    )

    session["history"].append({
        "agent": agent_name,
        "question": first_question,
        "answer": None,
        "feedback": None
    })

    return {
        "session": session,
        "question": first_question
    }


def next_question(session, answer):

    # Prevent submissions after completion
    if session.get("completed", False):
        return {
            "next_question": "",
            "feedback": "",
            "session": session,
            "done": True
        }

    idx = session["current_agent_index"]
    agent_name, agent_fn = AGENTS[idx]
    agent = agent_fn()

    # Save candidate's answer
    session["history"][-1]["answer"] = answer

    # Evaluate candidate's answer
    feedback, follow_up = run_agent_evaluate(
        agent,
        session["history"][-1]["question"],
        answer
    )

    session["history"][-1]["feedback"] = feedback

    # Ask follow-up question if generated
    if follow_up and follow_up.strip():

        next_q = follow_up.strip()

        session["history"].append({
            "agent": agent_name,
            "question": next_q,
            "answer": None,
            "feedback": None
        })

        return {
            "next_question": next_q,
            "feedback": feedback,
            "session": session,
            "done": False
        }

    # Move to next interviewer
    if idx + 1 < len(AGENTS):

        session["current_agent_index"] += 1

        next_agent_name, next_agent_fn = AGENTS[
            session["current_agent_index"]
        ]

        next_agent = next_agent_fn()

        next_q = run_agent_ask(
            next_agent,
            session["branch"],
            session["role"],
            session["history"]
        )

        session["history"].append({
            "agent": next_agent_name,
            "question": next_q,
            "answer": None,
            "feedback": None
        })

        return {
            "next_question": next_q,
            "feedback": feedback,
            "session": session,
            "done": False
        }

    # All four agents have completed
    session["completed"] = True

    return {
        "next_question": "",
        "feedback": feedback,
        "session": session,
        "done": True
    }
