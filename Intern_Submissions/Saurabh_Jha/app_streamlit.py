import streamlit as st

# ---- IMPORT CORE ENGINE ----
from src.core.engine import CognitiveEngine
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.agents.reflection import ReflectionAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.synthesizer import SynthesizerAgent
from src.memory.vector_memory import VectorMemory


def build_engine():
    return CognitiveEngine(
        planner=PlannerAgent(),
        executor=ExecutorAgent(),
        reflector=ReflectionAgent(),
        evaluator=EvaluatorAgent(),
        memory=VectorMemory(),
        synthesizer=SynthesizerAgent()
    )


# ---- STREAMLIT UI ----
st.set_page_config(
    page_title="Autonomous Cognitive Engine",
    layout="wide"
)

st.title("🧠 Autonomous Cognitive Engine")
st.markdown(
    """
    This system demonstrates an **autonomous cognitive engine** capable of:
    - Understanding high-level goals  
    - Decomposing tasks  
    - Performing tool-augmented research  
    - Maintaining memory  
    - Self-evaluating outputs  
    - Escalating to humans when confidence is low  
    """
)

goal = st.text_area(
    "Enter a high-level research goal",
    placeholder="e.g. Research autonomous AI agents in healthcare systems"
)

run_clicked = st.button("Run Cognitive Engine")

if run_clicked:
    if not goal.strip():
        st.error("Goal cannot be empty.")
    else:
        with st.spinner("Running autonomous cognitive engine..."):
            engine = build_engine()
            result = engine.run(goal)

        st.subheader("Execution Result")

        if result["status"] == "ESCALATED":
            st.warning("⚠️ Human Escalation Required")
            st.write("**Reason:**", result["reason"])
        else:
            st.success("✅ Execution Completed")
            st.subheader("Executive Summary")
            st.write(result["summary"])

        st.subheader("📚 Stored Memory (Evidence)")
        if engine.memory.texts:
            for i, item in enumerate(engine.memory.texts, 1):
                st.markdown(f"**{i}.** {item}")
        else:
            st.info("No memory stored.")
