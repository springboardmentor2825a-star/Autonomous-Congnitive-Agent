from llm import GeminiLLM

class CriticAgent:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.name = "Critic"
    
    def evaluate_response(self, query: str, response: str) -> str:
        """Critically evaluate the response for quality and completeness"""
        prompt = f"""You are a critical evaluator. Assess the quality and completeness of the response to the query.

Original Query: {query}

Response:
{response}

Evaluate the response on:
1. Completeness (Does it fully address the query?)
2. Accuracy (Are the facts likely correct?)
3. Clarity (Is it well-explained and easy to understand?)
4. Depth (Is it sufficiently detailed?)
5. Relevance (Is all information relevant to the query?)
6. Organization (Is it well-structured?)
7. Missing Elements (What could be added?)
8. Potential Issues (Any problematic aspects?)

Provide constructive feedback."""
        
        evaluation = self.llm.generate(prompt, temperature=0.5)
        return evaluation
    
    def identify_gaps(self, query: str, response: str) -> str:
        """Identify gaps in the response"""
        prompt = f"""Identify gaps or missing information in the response to the query.

Original Query: {query}

Response:
{response}

Identify:
1. Missing Information (what else should be addressed)
2. Unexplored Angles (different perspectives not covered)
3. Depth Issues (areas that need more detail)
4. Examples Needed (areas that would benefit from examples)
5. Validation Issues (claims that need verification)
6. Context Missing (background information that would help)

Be specific and actionable."""
        
        gaps = self.llm.generate(prompt, temperature=0.5)
        return gaps
    
    def suggest_improvements(self, query: str, response: str) -> str:
        """Suggest specific improvements to the response"""
        prompt = f"""Suggest specific, actionable improvements to enhance the response.

Original Query: {query}

Current Response:
{response}

Provide:
1. Content Improvements (what to add or modify)
2. Structure Improvements (how to organize better)
3. Clarity Improvements (how to explain better)
4. Depth Improvements (areas to explore more)
5. Specific Recommendations (concrete changes to make)

Format as actionable suggestions."""
        
        suggestions = self.llm.generate(prompt, temperature=0.6)
        return suggestions
