from crewai import Crew
from agents import research_agent, reasoning_agent, synthesis_agent
from tasks import create_tasks

def run_crew(user_prompt):
    tasks = create_tasks(user_prompt)

    crew = Crew(
        agents=[research_agent, reasoning_agent, synthesis_agent],
        tasks=tasks,
        process="sequential",
        verbose=True
    )

    return crew.kickoff()
