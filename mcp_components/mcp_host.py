#!/usr/bin/env python3

import json

from mcp_components.github_mcp_client import GithubMCPClient
from mcp_components.mcp_response_formatter import McpResponseFormatter


class MCPHost:
    def __init__(self, github_token: str):
        self.mcp_client = GithubMCPClient(github_token)
        self.formatter = McpResponseFormatter()

    async def execute(self, call_data: dict):
        print(f"Executing MCP request... {call_data}")
        response = await self._execute_request(call_data)
        print(f"MCP response... {response}")
        return response

    def _validate_request(self, call_data: dict) -> tuple[bool, str, dict]:
        if not call_data:
            return False, "No valid JSON request loaded", {}

        method = call_data.get("method", "")
        params = call_data.get("params", {})

        if method == "tools/list":
            return True, "tools/list", {}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if not tool_name:
                return False, "Tool name not specified in request", {}

            return True, tool_name, arguments
        else:
            return (
                False,
                f"Unsupported method: {method}. Only 'tools/call' and 'tools/list' methods are supported",
                {},
            )

    async def _connect(self):
        """Test connection and print success message"""
        if not await self.mcp_client.test_connection():
            return {"error": "Failed to connect to MCP GitHub server!", "isError": True}
        return None

    async def _execute_request(self, call_data: dict) -> dict:
        try:
            is_valid, message, arguments = self._validate_request(call_data)

            if not is_valid:
                return {"error": message, "isError": True}

            # Test connection once for both cases
            connection_error = await self._connect()
            if connection_error:
                return connection_error

            if message == "tools/list":
                result = await self.mcp_client.list_tools()

                return {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                    "isError": False,
                }
            else:
                tool_name = message
                result = await self.mcp_client.execute_tool(tool_name, arguments)
                return result

        except Exception as e:
            return {"error": f"Error executing MCP call: {e}", "isError": True}

    def _print_result(self, result: dict):
        formatted_output = self.formatter.format_mcp_response(result)
        print(formatted_output)
