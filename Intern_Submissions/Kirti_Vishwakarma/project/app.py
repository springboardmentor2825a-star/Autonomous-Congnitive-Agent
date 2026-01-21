from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph import graph

app = FastAPI(title="Multi Tool AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "Backend is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    result = graph.invoke({
        "messages": req.question
    })
    return {
        "answer": result["messages"][-1].content
    }
