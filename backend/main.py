from fastapi import FastAPI
from pydantic import BaseModel
from agent import DeepResearchAgent

app = FastAPI()
agent = DeepResearchAgent("Autonomous Deep Research Engine")

class ResearchGoal(BaseModel):
    goal: str

@app.post("/research/run")
def run_research(goal_data: ResearchGoal):
    return agent.run(goal_data.goal)

