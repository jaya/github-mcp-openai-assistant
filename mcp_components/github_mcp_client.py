#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os


class GithubMCPClient:
    def __init__(self):
        self._connection = None  # Stores (client_context, session) tuple

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
            ],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")
            },  # Pass GitHub token to container
        )

    async def connect(self):
        """Initialize and maintain a persistent MCP session"""
        if self._connection is not None:
            return  # Already connected

        try:
            client_context = stdio_client(self._get_server_params())
            read, write = await client_context.__aenter__()
            session = ClientSession(read, write)
            await session.initialize()

            self._connection = (client_context, session)
        except Exception as e:
            await self.disconnect()
            raise Exception(f"Failed to connect to MCP server: {e}")

    async def disconnect(self):
        """Close the persistent MCP session"""
        if self._connection:
            client_context, _ = self._connection

            try:
                await client_context.__aexit__(None, None, None)
            except Exception:
                pass

            self._connection = None

    async def _ensure_connected(self):
        if self._connection is None:
            await self.connect()

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        try:
            await self._ensure_connected()
            _, session = self._connection
            result = await session.call_tool(tool_name, arguments)
            return result.model_dump()
        except Exception as e:
            return {"error": f"Error executing tool: {e}", "isError": True}

    async def list_tools(self) -> list:
        try:
            await self._ensure_connected()
            _, session = self._connection
            tools_response = await session.list_tools()
            return [tool.model_dump() for tool in tools_response.tools]
        except Exception:
            return []

    async def test_connection(self) -> bool:
        """Test the MCP connection"""
        try:
            await self._ensure_connected()
            return True
        except Exception:
            return False
