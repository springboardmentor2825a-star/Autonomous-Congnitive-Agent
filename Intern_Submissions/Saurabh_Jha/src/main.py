from src.core.engine import CognitiveEngine
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.agents.reflection import ReflectionAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.synthesizer import SynthesizerAgent
from src.memory.vector_memory import VectorMemory


def main():
    print("\n===== Autonomous Cognitive Engine (CLI) =====\n")

    # ---- GOAL INTAKE LAYER ----
    goal = input("Enter a high-level research goal:\n> ").strip()

    if not goal:
        print("\nERROR: Goal cannot be empty.")
        return

    print(f"\nGOAL RECEIVED: {goal}\n")

    # ---- COMPONENT INITIALIZATION ----
    engine = CognitiveEngine(
        planner=PlannerAgent(),
        executor=ExecutorAgent(),
        reflector=ReflectionAgent(),
        evaluator=EvaluatorAgent(),
        memory=VectorMemory(),
        synthesizer=SynthesizerAgent()
    )

    # ---- RUN ENGINE ----
    result = engine.run(goal)

    print("\n===== FINAL RESULT =====\n")

    if result["status"] == "ESCALATED":
        print("STATUS: HUMAN ESCALATION REQUIRED")
        print(f"REASON: {result['reason']}")
    else:
        print("STATUS: COMPLETED")
        print("\nEXECUTIVE SUMMARY:\n")
        print(result["summary"])

    # ---- MEMORY VISIBILITY ----
    print("\n===== STORED MEMORY (EVIDENCE) =====\n")

    if not engine.memory.texts:
        print("No memory stored.")
    else:
        for idx, item in enumerate(engine.memory.texts, 1):
            print(f"[{idx}] {item}\n")


if __name__ == "__main__":
    main()
