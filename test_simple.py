#!/usr/bin/env python3

import asyncio
from dotenv import load_dotenv
from mcp_components.mcp_host import MCPHost

# Load environment variables
load_dotenv()


async def test_simple():
    """Simple test to check MCP functionality"""
    print("🧪 Testing MCP with simple request...")

    mcp_host = MCPHost()

    # Test 1: List tools
    print("\n1️⃣ Testing tools/list...")
    call_data = {"method": "tools/list", "params": {}}

    result = await mcp_host.execute(call_data)
    print(f"Result: {result}")

    # Test 2: Search repositories
    print("\n2️⃣ Testing repository search...")
    call_data = {
        "method": "tools/call",
        "params": {
            "name": "search_repositories",
            "arguments": {"query": "user:michelhdoumit"},
        },
    }

    result = await mcp_host.execute(call_data)
    print(f"Result: {result}")

    # Cleanup persistent MCP resources
    await mcp_host.cleanup()


if __name__ == "__main__":
    asyncio.run(test_simple())
