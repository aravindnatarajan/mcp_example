import re
from typing import Dict, List
from fastmcp import FastMCP
from bs4 import BeautifulSoup
import requests
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Initialize FastMCP server
mcp = FastMCP("web-search-server")

class WebSearch:
    def __init__(self, num_results: int = 3, timeout: int = 10):
        self._timeout = timeout
        self._num_results = num_results
        self._headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AnonymizedWebScraper/1.0'
            ),
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.ddg_search = DuckDuckGoSearchAPIWrapper()
        
    def _get_links(self, web_query: str) -> List[str]:
        """Fetch links safely using the DuckDuckGo wrapper."""
        try:
            results = self.ddg_search.results(web_query, max_results=self._num_results)
            return [res.get('link', '') for res in results if 'http' in res.get('link', '')]
        except Exception:
            return []

    def get_results(self, web_query: str) -> List[Dict[str, str]]:
        """Performs search, fetches raw web text, and cleans it up using BeautifulSoup."""
        links = self._get_links(web_query)
        final_results = []
        
        for link in links:
            try:
                response = requests.get(link, headers=self._headers, timeout=self._timeout)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Proactively drop boilerplate layout code/scripts
                    for element in soup(["script", "style", "nav", "footer", "header"]):
                        element.decompose()
                        
                    # Extract text with a clean separator, avoiding dense block runs
                    text_content = soup.get_text(separator=' ', strip=True)
                    # Normalize white-spaces
                    clean_text = re.sub(r'\s+', ' ', text_content)
                    
                    final_results.append({
                        'query': web_query,
                        'source': link,
                        'content': clean_text
                    })
            except requests.RequestException:
                # Silently skip transient request errors or timeouts for individual links
                continue
                
        return final_results

# Expose the utility function as an MCP Tool
@mcp.tool(description="Search the web for a given query and extract structural text data from matching top web results.")
def fetch_web_knowledge(query: str, num_results: int = 3) -> List[Dict[str, str]]:
    """
    Search the live web for a query and return clean textual content extracted from the pages.
    """
    searcher = WebSearch(num_results=num_results)
    return searcher.get_results(query)

if __name__ == "__main__":
    # Run over stdio transport layer for standard local agent execution contexts
    mcp.run(transport="stdio")
