import streamlit as st
from engine import AutonomousResearchEngine
import os
import time
from dotenv import load_dotenv
from dotenv import dotenv_values


# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Autonomous Cognitive Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f7f7f8;
}
.chat-container {
    max-width: 900px;
    margin: auto;
}
.user-msg {
    background: #e8f0fe;
    padding: 1rem;
    border-radius: 12px;
    margin: 1rem 0;
}
.ai-msg {
    background: #ffffff;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 1rem 0;
    border-left: 4px solid #10a37f;
}
.small-text {
    color: gray;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "engine" not in st.session_state:
    config = dotenv_values(".env")
    api_key = config.get("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found. Please set it in .env file")
        st.stop()

    st.session_state.engine = AutonomousResearchEngine(api_key)
    st.session_state.chat = []
    st.session_state.last_results = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🧠 Autonomous Engine")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat = []
        st.session_state.last_results = None
        st.session_state.engine.clear_memory()
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    enable_critic = st.checkbox("Enable Critic Agent", value=True)

    st.markdown("---")
    st.markdown("### 📊 Engine Status")
    status = st.session_state.engine.get_engine_status()
    st.metric("Memory Items", status["memory_items"])
    st.metric("Findings", status["research_findings"])
    st.metric("Knowledge Base", status["knowledge_base_size"])

    st.markdown("---")
    st.markdown("### 📚 Add Knowledge")
    knowledge_doc = st.text_area("Document Content", height=120)
    doc_source = st.text_input("Source (optional)")
    if st.button("Add Document", use_container_width=True):
        if knowledge_doc:
            st.session_state.engine.add_knowledge(knowledge_doc, doc_source)
            st.success("Document added successfully")
        else:
            st.warning("Document cannot be empty")

# ---------------- MAIN CHAT ----------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("## 💬 Research Chat")

# Display previous messages
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-msg'><b>You</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='ai-msg'><b>Autonomous Engine</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------------- INPUT ----------------
user_query = st.chat_input("Ask a deep research question...")

if user_query:
    # Save user message
    st.session_state.chat.append({
        "role": "user",
        "content": user_query
    })

    # ---------- PROFESSIONAL LOADING ----------
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        ("🧭 Planning research strategy...", 15),
        ("🔍 Searching internal & external knowledge...", 35),
        ("📚 Conducting deep research...", 60),
        ("🧠 Analyzing findings...", 80),
        ("✍️ Writing final answer...", 95),
    ]

    for msg, percent in steps:
        status_text.markdown(f"**{msg}**")
        progress_bar.progress(percent)
        time.sleep(0.3)

    # ---------- ENGINE EXECUTION ----------
    try:
        results = st.session_state.engine.process_query(
            user_query,
            enable_critic=enable_critic
        )
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Error generating response: {e}")
        st.stop()

    progress_bar.progress(100)
    status_text.markdown("✅ **Research complete**")
    time.sleep(0.2)

    progress_bar.empty()
    status_text.empty()

    # Save assistant response
    st.session_state.chat.append({
        "role": "assistant",
        "content": results["answer"]
    })

    st.session_state.last_results = results
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- EXPANDABLE DETAILS ----------------
if st.session_state.last_results:
    res = st.session_state.last_results

    with st.expander("🧩 Research Plan"):
        st.markdown(res["plan"])

    with st.expander("🔍 Research Findings"):
        st.markdown(res["research"])

    with st.expander("📊 Analysis"):
        st.markdown(res["analysis"])

    if res.get("evaluation"):
        with st.expander("✅ Critic Evaluation"):
            st.markdown(res["evaluation"])

    if res.get("improvements"):
        with st.expander("💡 Suggested Improvements"):
            st.markdown(res["improvements"])

    st.download_button(
        "📥 Download Answer",
        res["answer"],
        file_name="research_output.txt",
        mime="text/plain"
    )

# ---------------- FOOTER ----------------
st.markdown("""
<div class='small-text' style='text-align:center; margin-top:2rem;'>
Autonomous Cognitive Engine • Gemini Powered • Infosys Virtual Internship
</div>
""", unsafe_allow_html=True)
