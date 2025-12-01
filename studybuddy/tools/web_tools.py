from langchain_community.tools.tavily_search import TavilySearchResults
from studybuddy.core.config import settings

if not settings.TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

# Use the correct class name 'TavilySearchResults'
search_tool = TavilySearchResults(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)