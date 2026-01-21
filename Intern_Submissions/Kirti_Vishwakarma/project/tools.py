from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults

arxiv = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(
        top_k_results=2,
        doc_content_chars_max=500
    ),
    description="Query arxiv research papers"
)

wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=500
    )
)

tavily = TavilySearchResults()

TOOLS = [arxiv, wiki, tavily]
