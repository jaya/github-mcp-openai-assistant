#!/usr/bin/env python3

import json

from mcp_components.github_mcp_client import GithubMCPClient


class MCPHost:
    def __init__(self):
        self.mcp_client = GithubMCPClient()

    async def cleanup(self):
        """Cleanup MCP client resources"""
        await self.mcp_client.cleanup()

    async def execute(self, call_data: dict):
        method = call_data["method"]
        params = call_data["params"]

        if method == "tools/list":
            result = await self.mcp_client.list_tools()
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False,
            }
        elif method == "tools/call":
            tool_name = params["name"]
            arguments = params["arguments"]
            return await self.mcp_client.execute_tool(tool_name, arguments)
        else:
            raise ValueError(f"Unsupported method: {method}")
