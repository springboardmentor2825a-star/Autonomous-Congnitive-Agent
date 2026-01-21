from llm import GeminiLLM
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.critic import CriticAgent
from agents.memory import Memory
from rag import RAGSystem
from typing import Dict, Generator

class AutonomousResearchEngine:
    """Main orchestrator for autonomous research"""
    
    def __init__(self, api_key: str):
        self.llm = GeminiLLM(api_key)
        self.planner = PlannerAgent(self.llm)
        self.researcher = ResearcherAgent(self.llm)
        self.writer = WriterAgent(self.llm)
        self.critic = CriticAgent(self.llm)
        self.memory = Memory()
        self.rag = RAGSystem(self.llm)
    
    def process_query(self, query: str, enable_critic: bool = True) -> Dict[str, str]:
        """Process a query through the entire research pipeline"""
        
        results = {
            'query': query,
            'plan': '',
            'research': '',
            'analysis': '',
            'answer': '',
            'evaluation': '',
            'improvements': ''
        }
        
        # Step 1: Planning
        print("\n[PLANNER] Creating research plan...")
        plan = self.planner.create_research_plan(query)
        results['plan'] = plan
        self.memory.add_to_history("Planner", plan)
        
        # Step 2: Research
        print("[RESEARCHER] Conducting research...")
        research = self.researcher.research_topic(query, context=plan)
        results['research'] = research
        self.memory.add_to_history("Researcher", research)
        self.memory.add_research_finding(research)
        
        # Step 3: Analysis
        print("[RESEARCHER] Analyzing findings...")
        analysis = self.researcher.analyze_findings(research, query)
        results['analysis'] = analysis
        self.memory.add_to_history("Researcher", analysis)
        
        # Step 4: Writing
        print("[WRITER] Writing comprehensive answer...")
        answer = self.writer.write_comprehensive_answer(query, research, analysis)
        results['answer'] = answer
        self.memory.add_to_history("Writer", answer)
        
        # Step 5: Criticism & Improvement
        if enable_critic:
            print("[CRITIC] Evaluating response...")
            evaluation = self.critic.evaluate_response(query, answer)
            results['evaluation'] = evaluation
            self.memory.add_to_history("Critic", evaluation)
            
            print("[CRITIC] Suggesting improvements...")
            improvements = self.critic.suggest_improvements(query, answer)
            results['improvements'] = improvements
            
            # Optionally enhance answer based on improvements
            print("[WRITER] Enhancing answer based on feedback...")
            enhanced_answer = self.writer.write_comprehensive_answer(
                query,
                research + "\n\nImprovement Suggestions:\n" + improvements,
                analysis
            )
            results['answer'] = enhanced_answer
            self.memory.add_to_history("Writer", "Enhanced answer based on critic feedback")
        
        return results
    
    def get_memory_context(self) -> Dict[str, str]:
        """Get current memory context"""
        return {
            'history': self.memory.get_conversation_context(),
            'research_summary': self.memory.get_research_summary(),
            'planning_summary': self.memory.get_planning_summary()
        }
    
    def clear_memory(self):
        """Clear all memory"""
        self.memory.clear()
    
    def add_knowledge(self, document: str, source: str = ""):
        """Add document to knowledge base"""
        self.rag.add_to_knowledge_base(document, source)
    
    def get_engine_status(self) -> Dict:
        """Get current engine status"""
        return {
            'memory_items': len(self.memory.conversation_history),
            'research_findings': len(self.memory.research_findings),
            'knowledge_base_size': len(self.rag.knowledge_base)
        }
