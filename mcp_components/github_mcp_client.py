#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os


class GithubMCPClient:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.server_params = StdioServerParameters(
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
                "GITHUB_PERSONAL_ACCESS_TOKEN": self.github_token
            },  # Pass GitHub token to container
        )
        self._session = None
        self._read = None
        self._write = None
        self._client_context = None

    async def connect(self):
        """Initialize and maintain a persistent MCP session"""
        if self._session is not None:
            return  # Already connected

        try:
            # Create the stdio client context
            self._client_context = stdio_client(self.server_params)
            self._read, self._write = await self._client_context.__aenter__()

            # Create and initialize the session
            self._session = ClientSession(self._read, self._write)
            await self._session.__aenter__()
            await self._session.initialize()
        except Exception as e:
            await self.disconnect()
            raise Exception(f"Failed to connect to MCP server: {e}")

    async def disconnect(self):
        """Close the persistent MCP session"""
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception:
                pass
            self._session = None

        if self._client_context:
            try:
                await self._client_context.__aexit__(None, None, None)
            except Exception:
                pass
            self._client_context = None

        self._read = None
        self._write = None

    async def _ensure_connected(self):
        """Ensure we have an active session"""
        if self._session is None:
            await self.connect()

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool using the persistent session"""
        try:
            await self._ensure_connected()
            result = await self._session.call_tool(tool_name, arguments)
            return result.model_dump()
        except Exception as e:
            return {"error": f"Error executing tool: {e}", "isError": True}

    async def list_tools(self) -> list:
        """List available tools using the persistent session"""
        try:
            await self._ensure_connected()
            tools_response = await self._session.list_tools()
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

    async def __aenter__(self):
        """Context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.disconnect()
