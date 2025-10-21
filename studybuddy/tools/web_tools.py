from langchain_tavily import TavilySearch
from studybuddy.core.config import settings

if not settings.TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

# Use the new class name 'TavilySearch'
search_tool = TavilySearch(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)