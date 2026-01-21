class ResearchAgent:
    def __init__(self, llm, memory, browser):
        self.llm = llm
        self.memory = memory
        self.browser = browser

        if self.browser is None:
            raise ValueError("❌ BrowserTool is REQUIRED for ResearchAgent")

    def research(self, step, context=""):
        print("🌐 USING BROWSER FOR THIS STEP...")

        # -------------------------------
        # 1. FORCE WEB SEARCH
        # -------------------------------
        web_results = self.browser.search(step, num_results=5)

        if not web_results:
            web_context = "❌ No web results returned"
        else:
            web_context = "\n".join(
                [f"- {r}" for r in web_results]
            )

        # -------------------------------
        # 2. BUILD RESEARCH PROMPT
        # -------------------------------
        prompt = f"""
You are an autonomous research agent working on a long-horizon research task.

RESEARCH STEP:
{step}

RELEVANT MEMORY CONTEXT:
{context if context else "None"}

WEB EVIDENCE (MANDATORY):
{web_context}

INSTRUCTIONS:
- Ground your answer in the WEB EVIDENCE
- Use your own reasoning to synthesize insights
- Do NOT invent sources
- Be structured and precise
- Think like a research assistant, not a chatbot
"""

        # -------------------------------
        # 3. LLM SYNTHESIS
        # -------------------------------
        result = self.llm.generate(prompt)

        # -------------------------------
        # 4. STORE RESULT
        # -------------------------------
        self.memory.save(step, result)

        return result
