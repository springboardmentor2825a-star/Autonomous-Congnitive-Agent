class PlannerAgent:
    def __init__(self, llm_tool):
        self.llm = llm_tool

    def create_plan(self, goal):
        prompt = f"""
You are a planning agent in an autonomous cognitive engine.

Break the following goal into clear, logical, ordered steps
suitable for a long-horizon research task.

Goal:
{goal}

Return ONLY a numbered list of steps.
"""

        plan = self.llm.generate(prompt)
        return plan
