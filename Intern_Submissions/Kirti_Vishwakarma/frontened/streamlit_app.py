import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000/chat"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Autonomous Cognitive Engine",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #f5f5f5;
}

/* Title */
.title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cfd8dc;
    margin-bottom: 2rem;
}

/* Card */
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 30px;
    padding: 12px 28px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* Input box */
textarea {
    border-radius: 14px !important;
}

/* Chat bubbles */
.user-bubble {
    background: #0072ff;
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 80%;
}

.ai-bubble {
    background: #263238;
    color: #e0f7fa;
    padding: 16px 18px;
    border-radius: 18px;
    margin: 10px 0;
    max-width: 85%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🧠 Autonomous Cognitive Engine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Deep Research • Multi-Step Reasoning • Long-Horizon Intelligence</div>',
    unsafe_allow_html=True
)

# ---------------- DESCRIPTION CARD ----------------
st.markdown("""
<div class="card">
<b>What this system does</b><br><br>
• Understands complex research goals<br>
• Autonomously selects research tools (Arxiv, Web, Knowledge Bases)<br>
• Performs multi-step reasoning and synthesis<br>
• Produces deep, structured research insights
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

goal = st.text_area(
    "🎯 Research Goal",
    placeholder=(
        "Example:\n"
        "Analyze recent advancements in Generative AI and identify "
        "key research trends, challenges, and future directions."
    ),
    height=130
)

if st.button("🚀 Run Autonomous Research"):
    if goal.strip() == "":
        st.warning("Please enter a research goal.")
    else:
        with st.spinner("🧠 Planning research steps and gathering knowledge..."):
            response = requests.post(
                BACKEND_URL,
                json={"question": goal}
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.history.append({
                    "time": datetime.now().strftime("%d %b %H:%M"),
                    "goal": goal,
                    "answer": answer
                })
            else:
                st.error("Backend error. Please ensure the backend is running.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESULTS ----------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📑 Research Sessions")

if not st.session_state.history:
    st.info("No research sessions yet. Start by entering a research goal above.")
else:
    for item in reversed(st.session_state.history):
        st.markdown(f"🕒 **{item['time']}**")

        st.markdown(
            f'<div class="user-bubble"><b>Research Goal</b><br>{item["goal"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="ai-bubble"><b>Autonomous Engine Output</b><br>{item["answer"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

# ---------------- FOOTER ----------------
st.markdown(
    "<center style='color:#b0bec5'>"
    "Autonomous Cognitive Engine • Built with LangGraph, FastAPI & Streamlit"
    "</center>",
    unsafe_allow_html=True
)
