import requests
from bs4 import BeautifulSoup


def web_search(query: str):
    """
    Perform a web search and return real titles, URLs, and snippets.
    """
    search_url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(
        search_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for r in soup.select(".result")[:5]:
        title_tag = r.select_one(".result__a")
        snippet_tag = r.select_one(".result__snippet")

        if title_tag:
            results.append({
                "title": title_tag.get_text(strip=True),
                "url": title_tag.get("href"),
                "snippet": snippet_tag.get_text(strip=True) if snippet_tag else ""
            })

    return results
