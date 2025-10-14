#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from contextlib import AsyncExitStack


class GithubMCPClient:
    def __init__(self):
        self._tools_cache = None  # Cache for tools list
        self._stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    def _get_server_params(self):
        """Build server parameters for Docker MCP connection"""
        return StdioServerParameters(
            command="docker",
            args=[
                "run",  # Run a new Docker container
                "-i",  # Interactive mode - keeps STDIN open
                "--rm",  # Automatically remove container after execution
                "-e",  # Set environment variable in container
                "GITHUB_PERSONAL_ACCESS_TOKEN",  # Environment variable name
                "ghcr.io/github/github-mcp-server",  # GitHub MCP server Docker image
                "stdio",  # Explicit stdio command
            ],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")
            },  # Pass GitHub token to container
        )

    async def _ensure_session(self) -> None:
        """Ensure a single reusable MCP session is available (AsyncExitStack-based)."""
        if self._session is not None:
            return
        self._stack = AsyncExitStack()
        read, write = await self._stack.enter_async_context(
            stdio_client(self._get_server_params())
        )
        self._session = await self._stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._session.initialize()

    async def _execute_operation(self, operation):
        """Execute an operation using a persistent session."""
        try:
            await self._ensure_session()
            result = await operation(self._session)
            return result
        except Exception as e:
            return {"error": f"Error executing MCP call: {e}", "isError": True}

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool using a fresh session"""

        async def _call_tool(session):
            result = await session.call_tool(tool_name, arguments)
            return result.model_dump()

        return await self._execute_operation(_call_tool)

    async def list_tools(self) -> list:
        """List available tools using cached result or fresh session"""
        # Return cached tools if available
        if self._tools_cache is not None:
            return self._tools_cache

        async def _list_tools(session):
            tools_response = await session.list_tools()
            return [tool.model_dump() for tool in tools_response.tools]

        result = await self._execute_operation(_list_tools)
        if isinstance(result, list):
            # Cache the tools list for future calls
            self._tools_cache = result
            return result
        return []

    async def test_connection(self) -> bool:
        """Test the MCP connection"""

        async def _test_connection(session):
            return True

        result = await self._execute_operation(_test_connection)
        if isinstance(result, dict) and result.get("isError"):
            return False
        return True

    async def cleanup(self):
        """Cleanup resources (close persistent session and clear cache)."""
        self._tools_cache = None
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
            self._session = None
