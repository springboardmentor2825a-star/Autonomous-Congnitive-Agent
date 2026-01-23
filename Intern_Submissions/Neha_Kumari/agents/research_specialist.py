import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool


# LLM configurations - Agent specific config
model = os.getenv("RESEARCH_AGENT_LLM")
temperature = float(os.getenv("RESEARCH_AGENT_TEMPERATURE"))

llm = LLM(
    model=model,
    temperature=temperature,
    max_tokens=250
)

research_specialist_agent = Agent(
    role="Research Specialist",
    goal="Gather comprehensive and accurate information on given topics from multiple sources",
    backstory = (
                "You are an expert research specialist with years of experience in information gathering "
                "and fact-checking. You have a keen eye for reliable sources and can quickly identify the "
                "most relevant and up-to-date information on any topic."
            ),
    llm=llm,
    tools=[SerperDevTool()],
    verbose=True,
)
