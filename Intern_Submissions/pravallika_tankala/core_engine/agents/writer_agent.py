class WriterAgent:
    def __init__(self, llm):
        self.llm = llm

    def write_report(self, memory):
        combined = "\n\n".join(
            f"{m['step']}\n{m['result']}" for m in memory
        )

        prompt = f"""
Generate a structured research report from the content below.

{combined}
"""
        return self.llm.generate(prompt)
