#!/usr/bin/env python3

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class GithubMCPClient:
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.server_params = StdioServerParameters(
            command="docker",
            args=[
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server",
            ],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": self.github_token},
        )

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        async def _call_tool(session):
            result = await session.call_tool(tool_name, arguments)
            return result.model_dump()

        return await self._execute_operation(_call_tool)

    async def list_tools(self) -> list:
        async def _list_tools(session):
            tools_response = await session.list_tools()
            return [tool.model_dump() for tool in tools_response.tools]

        result = await self._execute_operation(_list_tools)
        return result if isinstance(result, list) else []

    async def test_connection(self) -> bool:
        async def _test_connection(session):
            return True

        result = await self._execute_operation(_test_connection)
        if isinstance(result, dict) and result.get("isError"):
            return False
        return True

    async def _execute_operation(self, operation):
        """Execute an operation with MCP session"""
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    return await operation(session)
        except Exception as e:
            return {"error": f"Error executing MCP call: {e}", "isError": True}
