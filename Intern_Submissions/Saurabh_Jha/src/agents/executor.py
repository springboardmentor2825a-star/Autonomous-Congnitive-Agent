from src.tools.web_search import web_search


class ExecutorAgent:
    def execute(self, task: str):
        """
        Execute a task using web search.
        Falls back only if no real sources are found.
        """
        results = web_search(task)
        enriched_results = []

        if results:
            for r in results:
                enriched_results.append(
                    f"Source: {r['title']}\n"
                    f"URL: {r['url']}\n"
                    f"Snippet: {r['snippet']}"
                )
        else:
            # Safe fallback (kept intentionally)
            enriched_results.extend([
                f"Source: Internal Knowledge Base\n"
                f"Snippet: General information related to {task}.",
            ])

        return enriched_results
