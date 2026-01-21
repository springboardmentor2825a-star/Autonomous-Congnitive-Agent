from agent.planner import plan
from agent.executor import execute
from agent.memory import save_memory
from agent.reflector import reflect

class AutonomousAgent:
    """
    Central controller for the autonomous agent lifecycle.
    """
    def __init__(self, task: str):
        self.task = task

    def run(self):
        task_plan = plan(self.task)
        execution_results = execute(task_plan)
        save_memory(self.task, execution_results)
        reflection = reflect(execution_results)
        return execution_results, reflection
