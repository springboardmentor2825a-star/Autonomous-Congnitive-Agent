from llm import GeminiLLM

class PlannerAgent:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.name = "Planner"
    
    def create_research_plan(self, query: str) -> str:
        """Create a detailed research plan for the given query"""
        prompt = f"""You are a research planner. Given the user query, create a detailed step-by-step research plan.
        
User Query: {query}

Create a structured research plan with the following sections:
1. Main Research Questions (3-5 key questions to answer)
2. Research Areas (What topics need to be explored)
3. Information Sources (Types of sources to look for)
4. Analysis Approach (How to analyze the findings)
5. Expected Outputs (What the final answer should contain)

Be specific and actionable."""
        
        plan = self.llm.generate(prompt, temperature=0.5)
        return plan
    
    def break_down_query(self, query: str) -> list:
        """Break down complex query into sub-queries"""
        prompt = f"""Break down this complex research query into 3-5 specific sub-queries that together will comprehensively answer the main question.

Main Query: {query}

List each sub-query clearly and explain why it's important for answering the main question.
Format as numbered list."""
        
        response = self.llm.generate(prompt, temperature=0.5)
        return response.split('\n')
