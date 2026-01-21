from llm import GeminiLLM

class ResearcherAgent:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.name = "Researcher"
    
    def research_topic(self, topic: str, context: str = "") -> str:
        """Conduct deep research on a specific topic"""
        prompt = f"""You are an expert researcher. Conduct thorough research on the following topic and provide detailed, accurate information.

Topic: {topic}
{f'Additional Context: {context}' if context else ''}

Provide:
1. Key Findings (main discoveries and facts)
2. Current State of Knowledge (what is known)
3. Important Nuances (edge cases, exceptions, controversies)
4. Supporting Evidence (facts, statistics, examples)
5. Limitations and Uncertainties

Be thorough, accurate, and cite general knowledge sources where applicable."""
        
        research = self.llm.generate(prompt, temperature=0.6)
        return research
    
    def analyze_findings(self, findings: str, query: str) -> str:
        """Analyze research findings in context of original query"""
        prompt = f"""Analyze the following research findings and synthesize them to answer the original query.

Original Query: {query}

Research Findings:
{findings}

Provide:
1. Key Insights (most important takeaways)
2. Connections (how different findings relate)
3. Answers to the Query (directly address the original question)
4. Evidence Quality (reliability of findings)
5. Further Questions (what else might be worth exploring)"""
        
        analysis = self.llm.generate(prompt, temperature=0.6)
        return analysis
    
    def fact_check(self, claim: str) -> str:
        """Fact-check a claim"""
        prompt = f"""Fact-check the following claim. Evaluate its accuracy based on your knowledge.

Claim: {claim}

Provide:
1. Verification Status (True/False/Partially True/Unclear)
2. Supporting Facts
3. Potential Issues
4. Context and Nuances"""
        
        verification = self.llm.generate(prompt, temperature=0.5)
        return verification
