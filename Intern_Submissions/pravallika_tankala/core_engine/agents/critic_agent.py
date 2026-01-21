class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def critique(self, step, research_output):
        prompt = f"""
You are a critic agent.

Evaluate the research output for the step below.

Step:
{step}

Research Output:
{research_output}

Identify:
- Missing points
- Weak explanations
- Suggestions for improvement
"""
        return self.llm.generate(prompt)
