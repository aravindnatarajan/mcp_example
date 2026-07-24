# Example showing the use of Agents with Model Contect Protocol (MCP).  

Uses a local LLM and Ollama.  

DuckDuckGo's free API is used to get web links given a query, and text is scraped using BeautifulSoup.  
The API is converted to an MCP server, and exposed to the ReAct agent as a tool. The tool is only called if necessary.  

 
# 🔌 MCP Python Implementation Example (`mcp_example`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/framework-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-mcp__example.ipynb-orange.svg)](./mcp_example.ipynb)

This repository provides an in-memory, self-contained demonstration of building an MCP server and driving an MCP client session entirely within Python (`mcp_example.ipynb`).

--- Examples showing that the tool is only called when necessary ---

Query: Winner of the 2026 Scripps National Spelling Bee?
Answer: Shrey Parikh won the 2026 Scripps National Spelling Bee.
Tools Called: ['fetch_web_knowledge']
----------------------------------------

Query: Distance from the earth to the moon
Answer: The average distance from the Earth to the Moon is approximately 238,855 miles (384,400 kilometers).
Tools Called: []
----------------------------------------

Query: When is Taylor Swift's birthday?
Answer: Taylor Swift was born on December 13, 1989.
Tools Called: []
----------------------------------------

Query: In which city was the first match of the 2026 Fifa world cup played?
Answer: The first match of the 2026 FIFA World Cup was played in Mexico City at the Estadio Azteca.
Tools Called: ['fetch_web_knowledge']
----------------------------------------

Query: Describe the carbon cycle
Answer: The carbon cycle is a biogeochemical process where carbon atoms circulate between the atmosphere, biosphere, hydrosphere, and geosphere. Plants and algae sequester carbon dioxide from the air through photosynthesis, while respiration by animals and microbes releases it back into the environment. Decomposition of organic matter further contributes to atmospheric carbon levels, while oceans act as significant reservoirs by absorbing dissolved gases. Finally, geological processes such as volcanic eruptions and fossil fuel combustion facilitate the long-term storage and release of carbon over millions of years.
Tools Called: []
