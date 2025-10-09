#!/usr/bin/env python3

import json
from typing import Dict

from llm.open_ai_llm import OpenAiSession
from mcp_components.mcp_host import MCPHost


class CodeAssistant:
    def __init__(self):
        self.session = OpenAiSession()
        self.mcp_host = MCPHost()

    async def start_conversation(self) -> None:
        print("🤖 GitHub Code Assistant - Interactive Mode")
        print("Type 'exit', 'quit', or 'bye' to end the conversation")
        print("=" * 50)

        try:
            while True:
                try:
                    question = input("\nUser: ").strip()
                    if question.lower() in ["exit", "quit", "bye", "q"]:
                        print("👋 Goodbye!")
                        break

                    if not question:
                        continue

                    print("Assistant: Thinking ...")
                    result = await self.ask(question)
                    print("Assistant: ", result)

                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
        finally:
            # Cleanup MCP resources
            await self.mcp_host.cleanup()

    async def ask(self, question: str) -> str:
        answer = self.session.ask(question)
        result = await self._process(answer)
        return result

    async def _process(self, answer: str) -> str:
        answer_json = json.loads(answer)

        if answer_json.get("type") == "final_answer":
            return answer_json.get("answer_markdown")

        mcp_request = answer_json.get("rpc")
        mcp_response = await self._execute_mcp_request(mcp_request)

        answer = self.session.ask(mcp_response)
        return await self._process(answer)

    async def _execute_mcp_request(self, mcp_request: Dict) -> str:
        mcp_response = await self.mcp_host.execute(mcp_request)
        return json.dumps(mcp_response)
