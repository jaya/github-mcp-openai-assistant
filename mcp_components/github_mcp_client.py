#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import json
from contextlib import AsyncExitStack


class GithubMCPClient:
    def __init__(self):
        self._stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    def _get_server_params(self):
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
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")},
        )

    async def _ensure_session(self):
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

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        await self._ensure_session()
        result = await self._session.call_tool(tool_name, arguments)
        return result.model_dump()

    async def list_tools(self) -> list:
        await self._ensure_session()
        tools_response = await self._session.list_tools()
        return [tool.model_dump() for tool in tools_response.tools]

    async def execute(self, mcp_request: dict):
        method = mcp_request["method"]
        params = mcp_request["params"]

        if method == "tools/list":
            result = await self.list_tools()
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False,
            }
        elif method == "tools/call":
            tool_name = params["name"]
            arguments = params["arguments"]
            return await self.execute_tool(tool_name, arguments)
        else:
            raise ValueError(f"Unsupported method: {method}")

    async def cleanup(self):
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
            self._session = None
