from studybuddy.core.config import settings

try:
    from langchain_tavily import TavilySearch  # type: ignore
except ImportError:
    TavilySearch = None  # type: ignore


def _create_search_tool():
    """
    Create the Tavily search tool if configured.

    Returns None when Tavily is not available or not configured,
    allowing the app to start and endpoints to handle the missing tool gracefully.
    """
    if TavilySearch is None:
        return None

    if not settings.TAVILY_API_KEY:
        # Tavily is optional – return None so features depending on it can handle the absence
        return None

    return TavilySearch(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)


# May be None if Tavily or API key is not configured
search_tool = _create_search_tool()