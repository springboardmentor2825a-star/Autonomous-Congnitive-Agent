from crewai import Agent
from crewai.llm import LLM

llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

research_agent = Agent(
    role="Research Agent",
    goal="Research the given topic deeply",
    backstory="Expert research analyst",
    llm=llm
)

reasoning_agent = Agent(
    role="Reasoning Agent",
    goal="Analyze and structure research findings",
    backstory="Critical thinking specialist",
    llm=llm
)

synthesis_agent = Agent(
    role="Synthesis Agent",
    goal="Produce final clear explanation",
    backstory="Professional technical writer",
    llm=llm
)
