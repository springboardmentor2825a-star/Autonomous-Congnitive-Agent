import os
import re
import torch
import time
import random
import faiss
import numpy as np
import gradio as gr
from typing import List, TypedDict, Dict, Any, Generator, Annotated
import operator
# Core Tools
from transformers import AutoModelForCausalLM, AutoTokenizer
from langgraph.graph import StateGraph, END, START
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS 
from markdown_pdf import MarkdownPdf, Section
from pypdf import PdfReader

# 1. My Agent State Definition
class AgentState(TypedDict):
    objective: str
    plan: List[str]
    findings: Annotated[List[str], operator.add] 
    current_step: int
    loop_count: int
# 2. Memory & RAG Module 
class LocalMemory:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.texts = []
    def add_to_memory(self, raw_text: str):
        chunks = [raw_text[i:i+500] for i in range(0, len(raw_text), 400)]
        self.texts.extend(chunks)
        embeddings = self.encoder.encode(self.texts)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
    def retrieve(self, query: str):
        if not self.index: return "No documents uploaded."
        query_vec = self.encoder.encode([query])
        _, indices = self.index.search(np.array(query_vec).astype('float32'), 2)
        return "\n".join([self.texts[i] for i in indices[0]])
# 3. The Main Agent Logic 
class AutonomousAgent:
    def __init__(self):
        model_name = "unsloth/Llama-3.2-1B-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float32, device_map="cpu"
        )
        self.memory = LocalMemory()
        self.graph = self._setup_graph()
    def call_llm(self, prompt: str, max_tokens: int = 400):
        input_text = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=max_tokens, temperature=0.5)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("assistant")[-1].strip()
    def plan_step(self, state: AgentState):
        prompt = f"Goal: {state['objective']}\nBreak this into 3 search queries. List them 1, 2, 3."
        response = self.call_llm(prompt)
        tasks = re.findall(r'\d\.\s*(.*)', response)
        return {"plan": tasks[:3], "current_step": 0, "loop_count": 0}
    def research_step(self, state: AgentState):
        current_query = state['plan'][state['current_step']]
        web_info = ""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(current_query, max_results=2))
                web_info = "\n".join([r['body'] for r in results])
        except: web_info = "Search failed."
        local_info = self.memory.retrieve(current_query)
        return {
            "findings": [f"Query: {current_query}\nWeb: {web_info}\nLocal: {local_info}"],
            "current_step": state['current_step'] + 1,
            "loop_count": state['loop_count'] + 1
        }
    def report_step(self, state: AgentState):
        full_context = "\n".join(state['findings'])
        prompt = f"Objective: {state['objective']}\nData: {full_context}\nWrite a detailed research report in Markdown."
        final_report = self.call_llm(prompt, max_tokens=1000)
        return {"findings": [final_report]}
    def _setup_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("planner", self.plan_step)
        workflow.add_node("researcher", self.research_step)
        workflow.add_node("reporter", self.report_step)
        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "researcher")
        def check_progress(state):
            if state['current_step'] < len(state['plan']) and state['loop_count'] < 5:
                return "researcher"
            return "reporter"
        workflow.add_conditional_edges("researcher", check_progress)
        workflow.add_edge("reporter", END)
        return workflow.compile()
# 4. The UI Layer
class MyAgentApp:
    def __init__(self):
        self.agent = AutonomousAgent()
        self.history = {}
    def handle_upload(self, file):
        if not file: return "No file selected."
        text = ""
        if file.name.endswith(".pdf"):
            pdf = PdfReader(file.name)
            text = " ".join([page.extract_text() for page in pdf.pages])
        else:
            with open(file.name, "r") as f: text = f.read()
        self.agent.memory.add_to_memory(text)
        return f"Added {file.name} to memory!"
    # Phase 1: Planning
    def start_planning(self, goal):
        state = {"objective": goal, "plan": [], "findings": [], "current_step": 0, "loop_count": 0}
        plan_output = self.agent.plan_step(state)
        formatted_plan = "\n".join([f"- {p}" for p in plan_output['plan']])
        state.update(plan_output)
        return gr.update(visible=True), f"### Suggested Plan:\n{formatted_plan}", state
    # Phase 2: Execution 
    def run_research(self, state):
        final_out = ""
        for update in self.agent.graph.stream(state):
            if "reporter" in update:
                final_out = update["reporter"]["findings"][-1]        
        # Save to history
        self.history[state['objective']] = final_out        
        # Export as PDF
        pdf_path = f"report_{int(time.time())}.pdf"
        doc = MarkdownPdf()
        doc.add_section(Section(final_out.encode('ascii', 'ignore').decode('ascii')))
        doc.save(pdf_path)       
        # Update history dropdown choices
        new_choices = list(self.history.keys())
        return final_out, pdf_path, gr.update(choices=new_choices), gr.update(visible=False)
    def view_history(self, selected_topic):
        if selected_topic in self.history:
            return self.history[selected_topic]
        return ""
    def launch(self):
        with gr.Blocks(theme=gr.themes.Soft()) as interface:
            gr.Markdown("# My Autonomous Research Engine")            
            active_state = gr.State()
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(label="Upload Knowledge Base")
                    upload_btn = gr.Button("Process Document")
                    gr.Markdown("---")
                    gr.Markdown("### Research History")
                    history_dropdown = gr.Dropdown(label="Select Past Report", choices=[])
                    history_btn = gr.Button("View Report")
                with gr.Column(scale=2):
                    goal_input = gr.Textbox(label="Research Topic", placeholder="Enter your goal...")
                    plan_btn = gr.Button("Generate Plan", variant="primary")                   
                    with gr.Group(visible=False) as approval_area:
                        plan_display = gr.Markdown()
                        proceed_btn = gr.Button("Approve & Execute Research", variant="stop")
                    output_area = gr.Markdown()
                    download_btn = gr.DownloadButton("Download PDF")
            upload_btn.click(self.handle_upload, [file_input], [])
            # Step 1: Plan
            plan_btn.click(self.start_planning, [goal_input], [approval_area, plan_display, active_state])            
            # Step 2: Execute (HITL)
            proceed_btn.click(self.run_research, [active_state], [output_area, download_btn, history_dropdown, approval_area])            
            # History Viewing
            history_btn.click(self.view_history, [history_dropdown], [output_area])
        interface.launch()
if __name__ == "__main__":
    app = MyAgentApp()
    app.launch()
