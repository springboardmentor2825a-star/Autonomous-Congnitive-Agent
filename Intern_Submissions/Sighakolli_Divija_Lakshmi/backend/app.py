import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from operator import add
import re

load_dotenv()

app = FastAPI(title="🧠 Autonomous Cognitive Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY or not TAVILY_API_KEY:
    raise ValueError("Missing API keys in .env")

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.1)
search_tool = TavilySearch(max_results=3, api_key=TAVILY_API_KEY)
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools)

# Simple in-memory store (no faiss)
memory_store: List[str] = []

class AgentState(Dict[str, Any]):
    messages: List[HumanMessage | AIMessage]
    confidence: float
    escalate: bool
    tasks: List[str]

# def planner(state: AgentState) -> AgentState:
#     """Decompose goal into tasks"""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are an autonomous cognitive agent. For the goal:
# 1. Break into 3-5 sub-tasks
# 2. Plan tool usage (search if needed)
# 3. Estimate confidence (0.0-1.0)
# 4. If confidence < 0.7, set escalate=true
# Respond with reasoning then JSON: {"tasks": ["task1", "task2"], "confidence": 0.85}"""),
#         MessagesPlaceholder(variable_name="messages"),
#         ("system", "Output ONLY final JSON")
#     ])
#     chain = prompt | llm_with_tools
#     response = chain.invoke({"messages": state["messages"]})
    
#     # Store reasoning in memory
#     memory_store.append(f"Planned tasks for '{state['messages'][0].content}': {response.content}")
    
#     # Simulate parsing (in prod, use structured output)
#     state["confidence"] = 0.85
#     state["tasks"] = ["Research trends", "Analyze impacts", "Generate report"]
#     state["messages"].append(response)
#     return state


# def planner(state: AgentState) -> AgentState:
#     """Decompose goal into tasks - FIXED PROMPT"""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are an autonomous cognitive agent. Analyze this high-level goal and:

# 1. Break into 3-5 actionable sub-tasks
# 2. Plan which tools to use (search for current info)
# 3. Estimate your confidence completing this (0.0-1.0)
# 4. If confidence < 0.7, recommend human escalation

# Example goal: "Research quantum trends"
# Response: First research recent developments using search tool. Confidence: 0.85

# Respond with clear reasoning then plan."""),
#         MessagesPlaceholder(variable_name="messages"),
#     ])
#     chain = prompt | llm_with_tools
#     response = chain.invoke({"messages": state["messages"]})
    
#     # Parse response for structured data (simplified)
#     content = response.content
#     memory_store.append(f"Goal analysis: {content[:200]}...")
    
#     # Extract/mock structured output
#     state["confidence"] = 0.85  # In prod: use PydanticOutputParser
#     state["tasks"] = ["Research key developments", "Identify business impacts", "Generate recommendations"]
#     state["messages"].append(AIMessage(content=f"PLAN: Tasks={state['tasks']}, Confidence={state['confidence']}"))
    
#     return state


# import re

# def planner(state: AgentState) -> AgentState:
#     """Dynamic confidence from LLM self-assessment"""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are an autonomous cognitive agent. For each goal:

# 1. Break into 3-5 specific sub-tasks
# 2. Assess COMPLEXITY: Easy=0.9+, Medium=0.7-0.89, Hard=0.4-0.69, Impossible<0.4
# 3. **MANDATORY**: End response with "CONFIDENCE: X.XX" (0.00-1.00 decimal)

# COMPLEXITY FACTORS:
# - Recent data needed? -0.1 (needs search)
# - Future prediction? -0.3 
# - Highly technical? -0.2
# - Ambiguous? -0.15
# - High risk? -0.4

# EXAMPLE: "Research 2025 trends" → CONFIDENCE: 0.88"""),
#         MessagesPlaceholder(variable_name="messages"),
#     ])
#     chain = prompt | llm_with_tools
#     response = chain.invoke({"messages": state["messages"]})
    
#     content = response.content
#     memory_store.append(f"Dynamic analysis: {content[:200]}")
    
#     # EXTRACT confidence dynamically
#     conf_match = re.search(r'CONFIDENCE:\s*(\d+\.?\d*)', content, re.IGNORECASE)
#     confidence = float(conf_match.group(1)) if conf_match else 0.5
    
#     # Mock tasks (parse in prod)
#     tasks = ["Research developments", "Analyze impacts", "Strategic recommendations"]
    
#     state["confidence"] = confidence
#     state["tasks"] = tasks
#     state["messages"].append(AIMessage(content=f"🚀 PLAN: {tasks} | Confidence: {confidence:.2f}"))
    
#     return state

import json

# def planner(state: AgentState) -> AgentState:
#     """Fixed JSON escaping + dynamic confidence"""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", """Analyze goal → Return ONLY valid JSON:

# {{
#   "tasks": ["task1", "task2"], 
#   "confidence": 0.85,
#   "reasoning": "why this score"
# }}

# Score 0.0-1.0 based on:
# -Highly recent data: +0.9
# -Future prediction: -0.3 
# -Technical complexity: -0.2
# -Business analysis: +0.8

# JSON ONLY - no other text."""),
#         MessagesPlaceholder(variable_name="messages"),
#     ])
    
#     # Fallback chain (no structured output - simple parsing)
#     chain = prompt | llm_with_tools
    
#     try:
#         response = chain.invoke({"messages": state["messages"]})
#         content = response.content
        
#         # Robust JSON/confidence extraction
#         start = content.find('{')
#         end = content.rfind('}') + 1
#         json_str = content[start:end] if start != -1 else '{}'
        
#         data = json.loads(json_str)
#         confidence = data.get('confidence', 0.5)
#         tasks = data.get('tasks', ['Research', 'Analyze', 'Recommend'])
#         reasoning = data.get('reasoning', 'No reasoning')
        
#     except:
#         # Ultimate fallback
#         confidence = 0.6
#         tasks = ['General research', 'Analysis', 'Recommendations']
#         reasoning = 'Fallback scoring'
    
#     memory_store.append(f"Plan: conf={confidence}, tasks={tasks}")
    
#     state["confidence"] = confidence
#     state["tasks"] = tasks
#     state["messages"].append(AIMessage(content=f"✅ DYNAMIC PLAN: {tasks} | Conf: {confidence:.2f} | {reasoning}"))
    
#     return state

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def planner(state: AgentState) -> AgentState:
    """Planner: break the high-level goal into sub-tasks (no confidence here)."""
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an autonomous cognitive agent.

Given the user's high-level goal, do ONLY these things:
1. Briefly restate the goal in your own words.
2. Break it into 3–5 clear, ordered sub-tasks.
3. For each sub-task, mention whether you will use web search tools or just reasoning.

Respond in this format (no JSON, no extra sections):

Restated goal: ...
Sub-tasks:
1. ...
2. ...
3. ...
Tool plan:
- Task 1: ...
- Task 2: ...
"""
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = prompt | llm_with_tools
    response = chain.invoke({"messages": state["messages"]})

    # Save plan in memory and state; do NOT set confidence here
    plan_text = response.content
    memory_store.append(f"Plan for goal '{state['messages'][0].content}': {plan_text[:200]}...")

    # Very simple task list extraction – safe fallback for your UI
    tasks = []
    for line in plan_text.splitlines():
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            tasks.append(line)

    if not tasks:
        tasks = ["Understand goal", "Research information", "Analyze findings", "Generate report"]

    state["tasks"] = tasks
    state["messages"].append(AIMessage(content=f"🧠 Plan created:\n" + "\n".join(tasks)))
    return state


def llm_confidence_from_messages(messages) -> float:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are evaluating the previous AI plan.

Read the conversation and output only a number between 0.0 and 1.0
showing how confident you are that the agent can complete this goal
with currently available tools and public information.

Examples:
- Pure prediction of exact future values → 0.1 - 0.3
- Complex but researchable technical topic → 0.5 - 0.8
- Simple summary or general research → 0.8 - 0.95
Never output 1.0; maximum is 0.95.
Respond with NUMBER ONLY, like: 0.82"""),
        ("human", "Here is the conversation and plan so far:"),
        *[(m.type, m.content) for m in messages],
    ])

    chain = prompt | llm  # use your Groq llm (not with_tools)
    resp = chain.invoke({})
    try:
        return float(resp.content.strip())
    except:
        return 0.5

def researcher(state: AgentState) -> AgentState:
    """Execute research with tools"""
    tool_node = ToolNode(tools)
    result = tool_node.invoke({"messages": state["messages"]})
    
    # Store research in memory
    research_content = " | ".join([msg.content for msg in result["messages"][-3:] if hasattr(msg, 'content')])
    memory_store.append(f"Research: {research_content}")
    
    state["messages"] = result["messages"]
    return state

def synthesizer(state: AgentState) -> AgentState:
    """Synthesize final report"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Synthesize research into executive report. Use memory:
""" + "\n".join(memory_store[-5:]) + """
Structure: Executive Summary | Key Findings | Recommendations.
Score final confidence."""),
        MessagesPlaceholder(variable_name="messages"),
    ])
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    state["messages"].append(response)
    #state["confidence"] = 0.92  # Final score
    return state

# def should_escalate(state: AgentState) -> str:
#     """Router: escalate or continue"""
#     if state.get("confidence", 1.0) < 0.7:
#         state["escalate"] = True
#         return "escalate"
#     return "synthesizer"


# def should_escalate(state: AgentState) -> str:
#     """Router - FIXED"""
#     confidence = state.get("confidence", 1.0)
#     if confidence < 0.7:
#         state["escalate"] = True
#         state["messages"].append(AIMessage(content="LOW CONFIDENCE - ESCALATING TO HUMAN"))
#         return END
#     return "synthesizer"



def should_escalate(state):
    # ask LLM to rate confidence based on full context
    confidence = llm_confidence_from_messages(state["messages"])
    state["confidence"] = confidence

    if confidence < 0.7:
        state["escalate"] = True
        state["messages"].append(
            AIMessage(content=f"LOW CONFIDENCE ({confidence:.2f}) - ESCALATING TO HUMAN")
        )
        return END
    return "synthesizer"


# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("synthesizer", synthesizer)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_conditional_edges("researcher", should_escalate, {
    "synthesizer": "synthesizer",
    END : END
})
workflow.add_edge("synthesizer", END)

agent = workflow.compile()

class GoalRequest(BaseModel):
    goal: str

class AgentResponse(BaseModel):
    output: str
    confidence: float
    escalate: bool
    tasks: List[str]
    memory: List[str]

@app.post("/execute", response_model=AgentResponse)
async def execute_goal(request: GoalRequest):
    """Main autonomous execution endpoint"""
    initial_state = {
        "messages": [HumanMessage(content=request.goal)],
        "confidence": 1.0,
        "escalate": False,
        "tasks": []
    }
    
    result = agent.invoke(initial_state)
    
    # Extract output
    output_msgs = [msg.content for msg in result["messages"] if hasattr(msg, 'content')]
    final_output = "\n\n".join(output_msgs[-3:])
    
    memory_snippets = memory_store[-4:] if memory_store else ["No memory yet"]
    
    return AgentResponse(
        output=final_output,
        confidence=result["confidence"],
        escalate=result.get("escalate", False),
        tasks=result.get("tasks", []),
        memory=[m[:150] + "..." for m in memory_snippets]
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "memory_count": len(memory_store)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
