#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os


class GithubMCPClient:
    def __init__(self):
        pass

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

    async def _execute_operation(self, operation):
        """Execute an operation with a fresh MCP session for each call"""
        try:
            async with stdio_client(self._get_server_params()) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await operation(session)
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
        """List available tools using a fresh session"""

        async def _list_tools(session):
            tools_response = await session.list_tools()
            return [tool.model_dump() for tool in tools_response.tools]

        result = await self._execute_operation(_list_tools)
        return result if isinstance(result, list) else []

    async def test_connection(self) -> bool:
        """Test the MCP connection"""

        async def _test_connection(session):
            return True

        result = await self._execute_operation(_test_connection)
        if isinstance(result, dict) and result.get("isError"):
            return False
        return True
