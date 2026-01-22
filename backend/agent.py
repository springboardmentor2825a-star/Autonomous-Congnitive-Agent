from memory import ResearchMemory
from planner import TaskPlanner

class DeepResearchAgent:
    def __init__(self, name):
        self.name = name
        self.memory = ResearchMemory()
        self.planner = TaskPlanner()

    def perceive_goal(self, goal):
        return f"Research goal received: {goal}"

    def plan(self, goal):
        return self.planner.create_plan(goal)

    def reason(self, step):
        return f"Reasoning over step: {step}"

    def act(self, reasoning):
        return f"Completed: {reasoning}"

    def run(self, goal):
        perception = self.perceive_goal(goal)
        plan = self.plan(goal)

        execution_trace = []

        for step in plan:
            reasoning = self.reason(step)
            action = self.act(reasoning)

            trace = {
                "step": step,
                "reasoning": reasoning,
                "action": action
            }

            self.memory.store(trace)
            execution_trace.append(trace)

        return {
            "perception": perception,
            "plan": plan,
            "execution_trace": execution_trace,
            "long_term_memory": self.memory.retrieve_all()
        }
