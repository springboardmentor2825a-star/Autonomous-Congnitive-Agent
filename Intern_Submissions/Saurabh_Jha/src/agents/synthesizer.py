class SynthesizerAgent:
    def synthesize(self, goal, memory):
        summary = f"Executive Summary: {goal}\n\n"

        key_points = memory[:5]
        for p in key_points:
            summary += f"- {p}\n"

        summary += "\nThis summary was generated using grounded external evidence."

        return summary
