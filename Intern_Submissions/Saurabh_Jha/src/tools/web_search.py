import requests
from bs4 import BeautifulSoup


def web_search(query: str):
    """
    Perform a lightweight web search and return multiple independent snippets.
    """
    url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    snippets = []

    results = soup.select(".result")[:5]
    for r in results:
        title = r.select_one(".result__a")
        snippet = r.select_one(".result__snippet")

        if title and snippet:
            snippets.append(
                f"Source: {title.get_text(strip=True)} | "
                f"Insight: {snippet.get_text(strip=True)}"
            )

    return snippets
