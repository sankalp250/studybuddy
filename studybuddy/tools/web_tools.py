# In studybuddy/tools/web_tools.py

from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def search_and_browse(query: str, max_results: int = 3):
    """
    Performs a web search for the given query, browses the top results,
    and returns a consolidated summary of their content.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of search results to browse.
    """
    # This is a placeholder for a real search API call.
    # In a real app, you would use Google Search API, DuckDuckGo, etc.
    print(f"--- Searching for: {query} ---")
    
    # We will simulate a search by returning a few placeholder URLs for now.
    # TODO: Replace with a real search API.
    if "ai news" in query.lower():
        urls = [
            "https://www.wired.com/tag/artificial-intelligence/",
            "https://techcrunch.com/category/artificial-intelligence/",
            "https://www.theverge.com/ai-artificial-intelligence"
        ]
    else:
        urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    print(f"--- Found {len(urls)} URLs ---")
    
    summaries = []
    for url in urls[:max_results]:
        try:
            print(f"--- Browsing URL: {url} ---")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main content, or just get the first few paragraphs
            paragraphs = soup.find_all('p', limit=4)
            text_content = " ".join([p.get_text() for p in paragraphs])
            
            if text_content:
                summaries.append(f"Content from {url}:\n{text_content}\n")

        except requests.RequestException as e:
            summaries.append(f"Could not browse {url}: {e}\n")

    if not summaries:
        return "No content found from browsing the search results."
        
    return "\n".join(summaries)