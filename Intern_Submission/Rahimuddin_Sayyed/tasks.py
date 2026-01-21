from crewai import Task
from agents import research_agent, reasoning_agent, synthesis_agent

def create_tasks(user_prompt):
    research_task = Task(
        description=f"Research the following topic in detail:\n{user_prompt}",
        expected_output="Detailed research notes",
        agent=research_agent
    )

    reasoning_task = Task(
        description="Analyze the research and extract key insights",
        expected_output="Structured insights",
        agent=reasoning_agent
    )

    synthesis_task = Task(
        description="Explain the topic clearly for a general audience",
        expected_output="Final explanation",
        agent=synthesis_agent
    )

    return [research_task, reasoning_task, synthesis_task]
