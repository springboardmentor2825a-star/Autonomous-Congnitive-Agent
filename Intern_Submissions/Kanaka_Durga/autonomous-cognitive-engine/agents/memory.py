from typing import List, Dict
from datetime import datetime

class Memory:
    def __init__(self):
        self.conversation_history = []
        self.research_findings = []
        self.planning_steps = []
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_research_finding(self, finding: str, source: str = ""):
        """Store research findings"""
        self.research_findings.append({
            'finding': finding,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_planning_step(self, step: str):
        """Store planning steps"""
        self.planning_steps.append({
            'step': step,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_conversation_context(self, last_n: int = 5) -> str:
        """Get recent conversation context"""
        recent = self.conversation_history[-last_n:]
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
        return context
    
    def get_research_summary(self) -> str:
        """Get summary of research findings"""
        if not self.research_findings:
            return "No research findings yet."
        summary = "\n".join([f"- {finding['finding']}" for finding in self.research_findings])
        return summary
    
    def get_planning_summary(self) -> str:
        """Get planning steps"""
        if not self.planning_steps:
            return "No planning steps yet."
        summary = "\n".join([f"- {step['step']}" for step in self.planning_steps])
        return summary
    
    def clear(self):
        """Clear all memory"""
        self.conversation_history = []
        self.research_findings = []
        self.planning_steps = []
