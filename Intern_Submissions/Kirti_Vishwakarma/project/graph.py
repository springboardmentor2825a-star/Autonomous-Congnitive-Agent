from typing_extensions import TypedDict
from typing import Annotated, List

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from llm import get_llm
from tools import TOOLS

# ---- State ----
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

# ---- LLM ----
llm = get_llm()
llm_with_tools = llm.bind_tools(TOOLS)

def tool_calling_llm(state: State):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

# ---- Graph ----
builder = StateGraph(State)

builder.add_node("llm", tool_calling_llm)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()
