#!/usr/bin/env python3

import json
from typing import List


class McpResponseFormatter:
    """
    Only AI can understand this code :-)
    Formats MCP (Model Context Protocol) responses for readable display.
    
    This class processes JSON responses from the GitHub MCP server and formats
    them in an organized and readable way, including:
    - Parsing nested JSON within strings
    - Data summary (total, items, etc.)
    - Item list formatting
    - Error handling and empty responses
    
    Attributes:
        max_items_preview (int): Maximum number of items for preview (default: 3)
    """

    # Constants
    HEADER = "📄 MCP RESPONSE:"
    SEPARATOR = "=" * 80
    ERROR_HEADER = "❌ ERROR RESPONSE:"
    SUCCESS_HEADER = "✅ SUCCESS RESPONSE:"

    def __init__(self):
        self.max_items_preview = 3

    def format_mcp_response(self, mcp_response: dict) -> str:
        if mcp_response.get("isError", False):
            return self._format_error(mcp_response)
        else:
            return self._format_success(mcp_response)

    def _format_error(self, mcp_response: dict) -> str:
        """Format error response"""
        output = [
            f"\n{self.HEADER}",
            self.SEPARATOR,
            self.ERROR_HEADER,
            json.dumps(mcp_response, indent=2, ensure_ascii=False),
            self.SEPARATOR
        ]
        return "\n".join(output)

    def _format_success(self, mcp_response: dict) -> str:
        """Format success response"""
        output = [
            f"\n{self.HEADER}",
            self.SEPARATOR,
            self.SUCCESS_HEADER
        ]

        content = mcp_response.get("content", [])
        if not content:
            output.extend(self._format_full(mcp_response))
        else:
            output.extend(self._format_content(content))

        output.append(self.SEPARATOR)
        return "\n".join(output)

    def _format_content(self, content: List[dict]) -> List[str]:
        """Format content response"""
        if not content or not content[0].get("text"):
            return ["📝 CONTENT:", json.dumps(content, indent=2, ensure_ascii=False)]

        text_content = content[0]["text"]
        try:
            parsed_data = json.loads(text_content)
            return self._format_data(parsed_data)
        except json.JSONDecodeError:
            return ["📝 TEXT RESPONSE:", text_content]
        except Exception:
            return ["📝 RAW RESPONSE:", text_content]

    def _format_data(self, data: dict) -> List[str]:
        """Format parsed JSON data"""
        output = [
            "📊 PARSED DATA:",
            json.dumps(data, indent=2, ensure_ascii=False)
        ]

        if isinstance(data, dict):
            summary = self._extract_summary(data)
            if summary:
                output.extend(self._format_summary(summary))

        return output

    def _format_summary(self, summary: dict) -> List[str]:
        """Format summary information"""
        output = [
            "\n📈 SUMMARY:",
            f"   Total found: {summary['total_count']}",
            f"   Items returned: {summary['items_count']}"
        ]

        if summary['items']:
            output.extend(self._format_items(summary['items']))

        return output

    def _format_items(self, items: List[dict]) -> List[str]:
        """Format items list"""
        output = ["\n📋 ITEMS:"]

        for i, item in enumerate(items[:self.max_items_preview], 1):
            output.extend([
                f"   {i}. #{item['number']} - {item['title']}",
                f"      State: {item['state']} | Repo: {item['repo']}"
            ])

        if len(items) > self.max_items_preview:
            remaining = len(items) - self.max_items_preview
            output.append(f"   ... and {remaining} more items")

        return output

    def _format_full(self, mcp_response: dict) -> List[str]:
        """Format full response when no content"""
        return [
            "📝 FULL RESPONSE:",
            json.dumps(mcp_response, indent=2, ensure_ascii=False)
        ]

    def _extract_summary(self, data: dict) -> dict:
        """Extract summary information from parsed data"""
        total_count = data.get("total_count", 0)
        items = data.get("items", [])

        if not items:
            return None

        formatted_items = []
        for item in items:
            repo_url = item.get("repository_url", "")
            repo_name = repo_url.split("/repos/")[-1] if "/repos/" in repo_url else "unknown"

            formatted_items.append({
                "title": item.get("title", "No title"),
                "state": item.get("state", "unknown"),
                "number": item.get("number", "?"),
                "repo": repo_name
            })

        return {"total_count": total_count, "items_count": len(items), "items": formatted_items}

    def _format_simple(self, mcp_response: dict) -> str:
        """Simple format for basic responses"""
        if mcp_response.get("isError", False):
            return f"❌ Error: {mcp_response.get('error', 'Unknown error')}"
        else:
            return f"✅ Success: {mcp_response.get('message', 'Operation completed')}"

    def _format_json(self, mcp_response: dict) -> str:
        """Format only the JSON data without extra formatting"""
        return json.dumps(mcp_response, indent=2, ensure_ascii=False)
