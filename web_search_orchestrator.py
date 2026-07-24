import asyncio
import warnings
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

class MCPAgentOrchestrator:
    """Manages the lifecycle of an MCP client connection and coordinates the

    compilation and invocation of a LangGraph ReAct agent loop.
    """

    def __init__(
        self,
        model_name: str = "gemma4:12b-mlx",
        temperature: float = 0.7,
        mcp_servers: Dict[str, Any] = None,
    ):
        # 1. Initialize LLM Configuration
        self.llm = ChatOllama(
            model=model_name, temperature=temperature, use_responses_api=True
        )

        # 2. Setup the MCP client configuration pointing to your search utility
        self.mcp_config = mcp_servers or {
            "web_search_tool": {
                "command": "python3",
                "args": ["web_search_mcp.py"],
                "transport": "stdio",
            }
        }

        # 3. Dynamic Length & Formatting Guidelines System Prompt
        self.system_prompt = """You are a precise knowledge assistant. You answer questions from the user based on real-time facts or your foundational knowledge.

CRITICAL RULES:
1. For any events, statistics, or updates from 2025 or 2026, you MUST call the web_search_tool__fetch_web_knowledge tool to gather accurate, live information.
2. Do not state that an event has not happened yet without executing the search tool first.

RESPONSE LENGTH & FORMATTING GUIDELINES:
- For Factual / Finitary Lookups (e.g., "Who won...", "What is the capital of...", "When did..."): Provide a sharp, direct, ONE-SENTENCE answer. Do not include unnecessary conversational filler.
- For Conceptual / Process Descriptions (e.g., "Describe the carbon cycle", "How does an engine work", "Explain..."): Provide a concise, cohesive SINGLE PARAGRAPH (maximum 4-5 sentences) summarizing the core components or stages.
"""
        # Placeholders for components initialized during the async bootstrap
        self.mcp_client = None
        self.agent_executor = None

    async def initialize(self):
        """Asynchronously maps schemas from the standard I/O channel and compiles

        the LangGraph topology.
        """
        # Instantiate the adapter connection context
        self.mcp_client = MultiServerMCPClient(self.mcp_config)

        # Dynamically ingest schemas from standard I/O channels
        tools = await self.mcp_client.get_tools()

        # Compile the graph architecture using state_modifier for system prompt injection
        self.agent_executor = create_react_agent(
            model=self.llm, tools=tools, prompt=self.system_prompt
        )

    async def answer_query(self, query: str) -> Dict[str, Any]:
        """Invokes the compiled agent graph loop with the structured query state."""
        if not self.agent_executor:
            raise RuntimeError(
                "Orchestrator has not been initialized. Please run `await orchestrator.initialize()` first."
            )

        state = {"messages": [HumanMessage(content=query)]}
        return await self.agent_executor.ainvoke(state)

    @staticmethod
    def get_tool_list(result: Dict[str, Any]) -> List[str]:
        """Highly optimized extraction utility using optimized dict.fromkeys to

        isolate unique tools called during execution steps.
        """
        tool_names = []
        for msg in result.get("messages", []):
            tool_calls = getattr(msg, "tool_calls", None) or []
            for tool in tool_calls:
                tool_names.append(tool["name"])
        return list(dict.fromkeys(tool_names))

    async def close(self):
        """Clean up and close down running client transport subprocess streams."""
        if self.mcp_client:
            await self.mcp_client.__aexit__(None, None, None)



