# core_engine/engine.py
from dotenv import load_dotenv
load_dotenv()

from core_engine.llm.gemini_tool import GeminiTool
from core_engine.agents.planner_agent import PlannerAgent
from core_engine.agents.research_agent import ResearchAgent
from core_engine.agents.critic_agent import CriticAgent
from core_engine.agents.writer_agent import WriterAgent
from core_engine.memory.episodic_memory import EpisodicMemory
from core_engine.rag.vector_store import VectorStore
from core_engine.rag.retriever import retrieve
from core_engine.actions.browser_tool import BrowserTool


import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")



def run_agent(goal: str):
    """
    Runs the Autonomous Cognitive Engine for a given goal.
    Returns structured logs for UI / API usage.
    """

    logs = []

    # -------------------------------
    # INITIALIZATION
    # -------------------------------
    llm = GeminiTool(GEMINI_API_KEY)
    browser = BrowserTool(SERPER_API_KEY)

    vector_store = VectorStore()
    memory = EpisodicMemory(vector_store)

    planner = PlannerAgent(llm)
    researcher = ResearchAgent(llm, memory, browser)
    critic = CriticAgent(llm)
    writer = WriterAgent(llm)

    logs.append(f"🎯 GOAL: {goal}")

    # -------------------------------
    # PLANNING PHASE
    # -------------------------------
    plan = planner.create_plan(goal)
    steps = [s.strip() for s in plan.split("\n") if s.strip()]

    logs.append("🧠 PLAN GENERATED:")
    for i, step in enumerate(steps, 1):
        logs.append(f"{i}. {step}")

    # -------------------------------
    # EXECUTION PHASE
    # -------------------------------
    for i, step in enumerate(steps[:3], 1):  # limit steps (safe + fast)
        logs.append(f"\n🔹 STEP {i}")
        logs.append(f"📌 TASK: {step}")

        # RAG context
        context_chunks = retrieve(vector_store, step)
        context = "\n".join(context_chunks)

        if context:
            logs.append("📚 CONTEXT FROM MEMORY:")
            logs.append(context)
        else:
            logs.append("📚 CONTEXT FROM MEMORY: None")

        # Research
        research_output = researcher.research(step, context)
        logs.append("🔍 RESEARCH OUTPUT:")
        logs.append(research_output)

        # Critique
        critique = critic.critique(step, research_output)
        logs.append("🧠 CRITIC FEEDBACK:")
        logs.append(critique)

    # -------------------------------
    # REPORTING PHASE
    # -------------------------------
    final_report = writer.write_report(memory.load_all())
    logs.append("\n✍️ FINAL REPORT:")
    logs.append(final_report)

    logs.append("\n✅ EXECUTION COMPLETED")

    return logs
