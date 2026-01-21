from llm import GeminiLLM

class WriterAgent:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.name = "Writer"
    
    def write_comprehensive_answer(self, query: str, research_findings: str, analysis: str) -> str:
        """Write a comprehensive, well-structured answer"""
        prompt = f"""You are an expert technical writer. Create a comprehensive, well-structured answer based on the research.

Original Query: {query}

Research Findings:
{research_findings}

Analysis:
{analysis}

Write a detailed answer that includes:
1. Executive Summary (brief overview)
2. Introduction (context and importance)
3. Main Content (detailed explanation with multiple sections)
4. Key Points (bulleted summary)
5. Conclusion (synthesis and takeaways)
6. Related Considerations (additional relevant information)

Make it informative, engaging, and easy to understand. Use clear sections and formatting."""
        
        answer = self.llm.generate(prompt, temperature=0.7)
        return answer
    
    def write_summary(self, content: str, length: str = "medium") -> str:
        """Write a summary of content"""
        word_count = {"short": 100, "medium": 300, "long": 500}
        target_length = word_count.get(length, 300)
        
        prompt = f"""Summarize the following content in approximately {target_length} words. Keep it clear and informative.

Content:
{content}

Provide a well-organized summary that captures the main points."""
        
        summary = self.llm.generate(prompt, temperature=0.6)
        return summary
    
    def format_for_presentation(self, content: str) -> str:
        """Format content for better presentation"""
        prompt = f"""Format the following content for clear presentation. Use:
- Clear headings
- Bullet points where appropriate
- Logical flow
- Key metrics or numbers highlighted
- Proper spacing and structure

Content:
{content}

Return the well-formatted version."""
        
        formatted = self.llm.generate(prompt, temperature=0.5)
        return formatted
