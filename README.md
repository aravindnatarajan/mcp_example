# Model Contect Protocol (MCP) example.  

Uses a local LLM and Ollama.  

DuckDuckGo's free API is used to get web links given a query, and text is scraped using BeautifulSoup.  
The API is converted to an MCP server, and exposed to the LLM as a tool. The tool is only called if necessary.  

 
# 🔌 MCP Python Implementation Example (`mcp_example`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/framework-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-mcp__example.ipynb-orange.svg)](./mcp_example.ipynb)

This repository provides an in-memory, self-contained demonstration of building an MCP server and driving an MCP client session entirely within Python (`mcp_example.ipynb`).

---

## 🛠️ How MCP is Implemented in This Repo

Instead of running separate server and client processes over STDIO or WebSockets, this repository uses **`FastMCP`** and the `fastmcp.Client` context manager to instantiate and interact with an MCP server **in-process**.

### Architecture Overview

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 mcp_example.ipynb                           │
  │                                                             │
  │  ┌──────────────────────┐      in-memory async connection   │
  │  │  FastMCP Server      │ <──────────────────────────────┐  │
  │  │  ("Math & Utility")  │                                │  │
  │  └──────────┬───────────┘                                │  │
  │             │                                            │  │
  │             ├── @mcp.tool() ──> add_numbers()            │  │
  │             ├── @mcp.tool() ──> calculate_bmi()          │  │
  │             └── @mcp.resource() ──> config://app-settings│  │
  │                                                          │  │
  │  ┌────────────────────────────────────────────────────┐  │  │
  │  │ Client(mcp) Async Context Manager                  │ ─┴──┘  │
  │  │  • Discover: await client.list_tools()            │        │
  │  │  • Execute:  await client.call_tool(...)           │        │
  │  └────────────────────────────────────────────────────┘        │
  └─────────────────────────────────────────────────────────────┘

