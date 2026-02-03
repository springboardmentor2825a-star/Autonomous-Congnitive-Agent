class PlannerAgent:
    def plan(self, goal: str):
        """
        Generate a multi-step research plan with diverse evidence goals.
        """
        return [
            f"Overview and definition of {goal}",
            f"Real-world enterprise use cases of {goal}",
            f"Architectural patterns used in {goal}",
            f"Risks, limitations, and safety concerns of {goal}",
            f"Future trends and research directions in {goal}"
        ]
