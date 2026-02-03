from src.core.state import AgentState
from src.utils.cost_tracker import CostTracker


class CognitiveEngine:
    def __init__(
        self,
        planner,
        executor,
        reflector,
        evaluator,
        memory,
        synthesizer
    ):
        self.state = AgentState.IDLE

        self.planner = planner
        self.executor = executor
        self.reflector = reflector
        self.evaluator = evaluator
        self.memory = memory
        self.synthesizer = synthesizer

        self.cost_tracker = CostTracker(max_steps=8)

    def run(self, goal: str):
        # -------- PLANNING --------
        self.state = AgentState.PLANNING
        plan = self.planner.plan(goal)

        # -------- EXECUTION --------
        self.state = AgentState.EXECUTING
        for task in plan:
            self.cost_tracker.tick()
            results = self.executor.execute(task)
            for r in results:
                self.memory.add(r)

        # -------- REFLECTION --------
        self.state = AgentState.REFLECTING
        reflection_passed, reflection_reason = self.reflector.reflect(
            self.memory.texts
        )

        # -------- EVALUATION --------
        self.state = AgentState.EVALUATING
        decision = self.evaluator.evaluate(reflection_passed)

        if not decision:
            self.state = AgentState.ESCALATED
            return {
                "status": "ESCALATED",
                "reason": reflection_reason,
                "state": self.state.value
            }

        # -------- SYNTHESIS --------
        self.state = AgentState.COMPLETED
        summary = self.synthesizer.synthesize(
            goal=goal,
            memory=self.memory.texts
        )

        return {
            "status": "COMPLETED",
            "state": self.state.value,
            "summary": summary
        }
