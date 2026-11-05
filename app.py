
import streamlit as st
import html
import os

if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

if "GEMINI_MODEL" in st.secrets:
    os.environ["GEMINI_MODEL"] = st.secrets["GEMINI_MODEL"]

from question_generator import start_interview, next_question

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="InterviewPro AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
defaults = {
    "session": None,
    "chat": [],
    "answer_key": 0,
    "branch": "",
    "role": "",
    "error": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7fb;
}

[data-testid="stSidebar"] {
    background: #101a30;
}

[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* FIX 1: SIDEBAR INPUT VISIBILITY */
[data-testid="stSidebar"] input {
    color: #17233b !important;
    background: #ffffff !important;
}

[data-testid="stSidebar"] input::placeholder {
    color: #64748b !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #17233b !important;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    color: #2563eb;
    margin-bottom: 2px;
}

.brand-sub {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 25px;
}

.main-heading {
    font-size: 30px;
    font-weight: 800;
    color: #17233b;
    margin-bottom: 4px;
}

.sub-heading {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 24px;
}

.info-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-bottom: 14px;
}

.info-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
}

.info-value {
    font-size: 19px;
    font-weight: 700;
    color: #17233b;
    margin-top: 5px;
}

.chat-card {
    padding: 17px 19px;
    border-radius: 14px;
    margin: 12px 0;
    line-height: 1.65;
    font-size: 14px;
    overflow-wrap: anywhere;
}

.interviewer {
    background: #ffffff;
    border: 1px solid #dbeafe;
    color: #17233b;
    border-left: 4px solid #2563eb;
}

.candidate {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1e3a8a;
    border-left: 4px solid #60a5fa;
}

.evaluation {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #713f12;
    border-left: 4px solid #f59e0b;
}

.system {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
}

.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #17233b;
    margin-bottom: 12px;
}

div.stButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 43px;
}

div.stButton > button[kind="primary"] {
    background: #2563eb;
    border: none;
}

div.stTextArea textarea {
    border-radius: 10px;
    background: white;
}

.progress-caption {
    color: #64748b;
    font-size: 12px;
    margin-bottom: 7px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    padding: 25px 0 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        '<div class="brand">🎯 InterviewPro AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">Your personal AI interview coach</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### ⚙️ Interview Setup")

    branch = st.selectbox(
        "Engineering Branch",
        ["CSE", "AI", "ENTC", "CIVIL", "MECH"]
    )

    role = st.text_input(
        "Target Job Role",
        placeholder="e.g. Data Analyst"
    )

    start_clicked = st.button(
        "🚀 Start Interview",
        type="primary",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### 🤖 Your AI Interview Panel")

    for name, description in [
        ("Technical", "Technical knowledge"),
        ("Conceptual", "Core concepts"),
        ("Problem Solving", "Logic and reasoning"),
        ("HR", "Communication and behaviour")
    ]:
        st.markdown(
            f"**● {name}**  \n"
            f"<small>{description}</small>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("Powered by CrewAI + Gemini")


# ---------------- START INTERVIEW ----------------
if start_clicked:

    if not role.strip():
        st.sidebar.error("Please enter a job role.")

    else:
        try:
            with st.spinner(
                "AI interviewers are preparing your interview..."
            ):
                result = start_interview(branch, role.strip())

            st.session_state.session = result["session"]

            st.session_state.chat = [
                {
                    "speaker": "Interviewer",
                    "text": result["question"]
                }
            ]

            st.session_state.answer_key = 0
            st.session_state.branch = branch
            st.session_state.role = role.strip()
            st.session_state.error = None

            st.rerun()

        except Exception as e:
            st.sidebar.error(f"Could not start interview: {e}")


# ---------------- MAIN HEADER ----------------
st.markdown(
    '<div class="main-heading">Interview Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">'
    'Practice, improve and prepare for your next opportunity with AI.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- DASHBOARD CONTENT ----------------
if st.session_state.session is None:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-label">AI Interviewers</div>
            <div class="info-value">04 Agents</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-label">Interview Mode</div>
            <div class="info-value">Multi-Agent</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-label">AI Engine</div>
            <div class="info-value">Gemini</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 👋 Welcome to InterviewPro AI")

    st.info(
        "Your interview workspace is ready. "
        "Choose your engineering branch and target job role "
        "from the sidebar, then click Start Interview."
    )

    st.markdown("#### How your interview works")

    a, b, c, d = st.columns(4)

    a.markdown("**01 · Technical**")
    a.caption("Test technical knowledge")

    b.markdown("**02 · Conceptual**")
    b.caption("Understand core concepts")

    c.markdown("**03 · Problem Solving**")
    c.caption("Evaluate your logic")

    d.markdown("**04 · HR**")
    d.caption("Assess communication")


else:

    session = st.session_state.session
    completed = session.get("completed", False)

    agent_index = session.get("current_agent_index", 0)

    agent_names = [
        "Technical",
        "Conceptual",
        "Problem Solving",
        "HR"
    ]

    # FIX 2: PROGRESS BAR STARTS AT 25%
    progress = (
        1.0 if completed
        else min((agent_index + 1) / 4, 1.0)
    )

    # ---------------- INTERVIEW DETAILS ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Target Role</div>
                <div class="info-value">
                    {html.escape(st.session_state.role)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Branch</div>
                <div class="info-value">
                    {html.escape(st.session_state.branch)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Interview Status</div>
                <div class="info-value">
                    {"Completed" if completed else "In Progress"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- PROGRESS TRACKER ----------------
    st.markdown(
        '<div class="section-title">Interview Progress</div>',
        unsafe_allow_html=True
    )

    st.progress(progress)

    progress_cols = st.columns(4)

    for i, name in enumerate(agent_names):

        if completed or i < agent_index:
            status = "✓ Completed"

        elif i == agent_index:
            status = "● Active"

        else:
            status = "○ Pending"

        progress_cols[i].caption(f"**{name}**")
        progress_cols[i].caption(status)

    st.markdown("---")

    # ---------------- CHAT SECTION ----------------
    st.markdown(
        '<div class="section-title">💬 Live Interview Room</div>',
        unsafe_allow_html=True
    )

    for msg in st.session_state.chat:

        speaker = msg["speaker"]

        message = html.escape(
            str(msg["text"])
        ).replace("\n", "<br>")

        if speaker == "Candidate":
            css_class = "candidate"
            icon = "👤"

        elif speaker == "Evaluation":
            css_class = "evaluation"
            icon = "🧠"

        elif speaker == "System":
            css_class = "system"
            icon = "🎉"

        else:
            css_class = "interviewer"
            icon = "🤖"

        st.markdown(
            f"""
            <div class="chat-card {css_class}">
                <strong>{icon} {speaker}</strong><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- INTERVIEW COMPLETION ----------------
    if completed:

        st.success(
            "🎉 Congratulations! Your interview is completed."
        )

        st.info(
            "All four interview stages have finished. "
            "Your final performance report will be added "
            "in the next upgrade."
        )

        if st.button(
            "🔄 Start New Interview",
            type="primary"
        ):

            st.session_state.session = None
            st.session_state.chat = []
            st.session_state.answer_key = 0
            st.session_state.branch = ""
            st.session_state.role = ""

            st.rerun()

    # ---------------- ANSWER SECTION ----------------
    else:

        st.markdown("---")
        st.markdown("### ✍️ Submit Your Answer")

        answer = st.text_area(
            "Your response",
            key=f"answer_{st.session_state.answer_key}",
            placeholder="Write your answer here. Explain your approach clearly...",
            height=150,
            label_visibility="collapsed"
        )

        if st.button(
            "📨 Submit Answer",
            type="primary",
            use_container_width=True
        ):

            if not answer.strip():

                st.warning(
                    "Please write your answer before submitting."
                )

            else:

                try:
                    with st.spinner(
                        "AI is evaluating your answer and preparing the next question..."
                    ):

                        result = next_question(
                            session,
                            answer
                        )

                    st.session_state.chat.append({
                        "speaker": "Candidate",
                        "text": answer
                    })

                    st.session_state.chat.append({
                        "speaker": "Evaluation",
                        "text": result["feedback"]
                    })

                    st.session_state.session = result["session"]

                    if result["done"]:

                        st.session_state.chat.append({
                            "speaker": "System",
                            "text": "Interview completed successfully!"
                        })

                    else:

                        st.session_state.chat.append({
                            "speaker": "Interviewer",
                            "text": result["next_question"]
                        })

                    st.session_state.answer_key += 1

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not process your answer: {e}"
                    )


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">'
    'InterviewPro AI · Intelligent Interview Preparation'
    '</div>',
    unsafe_allow_html=True
)
