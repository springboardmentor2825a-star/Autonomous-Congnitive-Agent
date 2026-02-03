class ReflectionAgent:
    def reflect(self, memory):
        """
        Evaluate whether the gathered evidence is sufficient and diverse.
        """

        if not memory or len(memory) < 5:
            return False, "Insufficient total evidence collected"

        unique_sources = set()

        for item in memory:
            if "Source:" in item:
                src = item.split("Source:")[1].split("|")[0].strip()
                unique_sources.add(src)

        if len(unique_sources) < 3:
            return False, "Not enough independent evidence sources"

        return True, "Evidence sufficiently grounded and diverse"
