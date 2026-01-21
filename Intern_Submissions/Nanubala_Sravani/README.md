# Autonomous Cognitive Agent

## Overview
The **Autonomous Cognitive Agent** is a minimal autonomous system capable of:

- Planning tasks
- Executing multi-step workflows
- Storing execution memory
- Reflecting on outcomes
- Simulating reasoning with LLMs
- Performing basic NLP tasks via Hugging Face
- Providing a simple web interface for interaction

This project demonstrates core principles of **modern GenAI autonomous agents** in a structured, explainable way.

---

## Problem Statement
Traditional automation systems lack reasoning, memory, and adaptability.  
This agent addresses these gaps by simulating a **full autonomous workflow**:

1. Understanding tasks
2. Planning steps
3. Executing actions
4. Storing results
5. Reflecting and analyzing
6. Generating insights with AI tools

---

## Objectives
- Build a modular autonomous agent pipeline
- Simulate task planning, execution, and reflection
- Demonstrate integration with AI tools (LLM & Hugging Face)
- Provide a web interface for interactive demonstrations

---

## Architecture Overview
**Agent Components:**

| Component  | Responsibility |
|------------|----------------|
| Planner    | Breaks tasks into sequential steps |
| Executor   | Executes each step using pandas/numpy for data simulation |
| Memory     | Stores task outcomes in `memory.json` |
| Reflector  | Evaluates execution success and provides feedback |
| Tools      | Simulates AI tools: OpenAI LLM & Hugging Face transformers |
| Controller | Orchestrates the full agent lifecycle |

**Agent Workflow:**

<img width="1536" height="1024" alt="de6d06d9-f77f-4958-bf01-d83188900726" src="https://github.com/user-attachments/assets/b7ec134c-8d12-4060-8891-6ce4cc4f35df" />

---

## Python Backend

### Requirements
Install dependencies:

```bash
pip install -r requirements.txt
