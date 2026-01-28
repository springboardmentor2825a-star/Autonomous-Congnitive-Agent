## 🏗️ System Architecture

This project is a full-stack **Autonomous Cognitive Engine** built with:

- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI
- **Agent Orchestration:** LangGraph
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Tools:** Tavily web search
- **Memory:** In-memory store (list of snippets) per run

### 1. High-Level Flow

1. **User Goal (UI)**
   - User enters a high-level goal in the Streamlit app (e.g.,  
     “Research quantum computing advancements in 2026 and generate an executive summary with strategic business recommendations.”).
   - Frontend sends a POST request to the FastAPI endpoint `/execute`.

2. **Planner Node (LangGraph)**
   - Receives the goal as the first `HumanMessage`.
   - Uses `llm_with_tools` to:
     - Restate the goal.
     - Break it into 3–5 ordered sub-tasks.
     - Decide where to use web search vs pure reasoning.
   - The generated plan is:
     - Stored in `memory_store`.
     - Saved in `state["tasks"]`.
     - Appended to `state["messages"]` as an `AIMessage` (“🧠 Plan created…”).

3. **Researcher Node (Tools Layer)**
   - Uses a `ToolNode` with **TavilySearch** to perform web search on the planned sub-tasks.
   - The latest tool outputs (web results) are:
     - Appended to `state["messages"]`.
     - Summarized and stored into `memory_store` (simple list of text snippets).

4. **Confidence Gate (LLM Self-Evaluation)**
   - Before deciding the next step, a dedicated function `llm_confidence_from_messages`:
     - Reads the full conversation (`state["messages"]`).
     - Asks the LLM to output a numeric confidence score between 0.0 and 1.0 based on how realistic and well-grounded the answer is.
     - Clamps the score to a safe range (e.g., max 0.95, lower for clearly impossible tasks like exact stock price predictions).
   - This score is stored in `state["confidence"]`.

5. **Routing: Autonomous vs Human-in-the-Loop**
   - If `confidence < 0.7`:
     - `state["escalate"] = True`
     - Agent appends: `LOW CONFIDENCE (x.xx) – ESCALATING TO HUMAN`
     - Graph ends the workflow (no final long report).
   - If `confidence ≥ 0.7`:
     - Graph proceeds to the **synthesizer** node.

6. **Synthesizer Node (Executive Report)**
   - Uses the base `llm` (no tools) with all messages for this goal.
   - Generates a structured executive report:
     - Executive Summary
     - Key Findings
     - Strategic Recommendations
     - A textual “Confidence Score: X/10 – …” line for human readers
   - The report is appended to `state["messages"]` and returned to the frontend.

7. **Response to Frontend**
   - FastAPI returns a JSON response with:
     - `output`: final text (plan + report or escalation message)
     - `confidence`: numeric confidence from the gate
     - `escalate`: true/false
     - `tasks`: list of planned sub-tasks
     - `memory`: recent snippets from `memory_store`

The Streamlit UI displays:
- The conversation (user goal + agent responses).
- The final confidence score.
- A warning banner when the agent escalates to human.

### 2. LangGraph Topology

The internal agent is wired as a simple graph:

- Nodes:
  - `planner`
  - `researcher`
  - `synthesizer`

- Edges:
  - Entry → `planner`
  - `planner` → `researcher`
  - `researcher` → (conditional)
    - `synthesizer` when `confidence ≥ 0.7`
    - `END` when `confidence < 0.7`
  - `synthesizer` → `END`

This models a **single-pass, long-horizon agent** with:
- Task decomposition
- Tool-augmented research
- Self-evaluation
- Human escalation

### 3. Safety & Design Choices

- **LLM-based confidence scoring** instead of fixed rules.
- **Explicit escalation** when confidence is low, especially on:
  - Exact future predictions (e.g., stock price with 99% accuracy).
  - Highly speculative or unsafe queries.
- **No direct tool calls from the UI** (all tool use controlled by backend).
- **Per-request memory** (no cross-user data mixing).

This architecture demonstrates a realistic enterprise-style cognitive engine that can:
- Break down complex goals,
- Use tools,
- Maintain contextual memory within a run,
- Evaluate its own answers,
- And know when to defer to a human.
