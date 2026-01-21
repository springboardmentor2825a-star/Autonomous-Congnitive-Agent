import requests

class BrowserTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://google.serper.dev/search"

    def search(self, query, num_results=5):
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "num": num_results
        }

        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        results = []
        for item in data.get("organic", []):
            results.append(
                f"{item.get('title')} - {item.get('snippet')}"
            )

        return results
