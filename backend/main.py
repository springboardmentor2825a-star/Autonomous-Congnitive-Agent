from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Goal(BaseModel):
    goal: str

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/run")
def run_agent(data: Goal):
    return {"goal": data.goal, "status": "Cognitive engine started"}


