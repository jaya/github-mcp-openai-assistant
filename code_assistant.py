import json

from conversation_loop import ConversationLoop
from llm.open_ai_llm import OpenAiSession
from mcp_components.github_mcp import GitHubMCP
from mcp_components.stdio_mcp_client import StdioMCPClient


class CodeAssistant:
    def __init__(self) -> None:
        self.llm_session = OpenAiSession()
        self.mcp_client = StdioMCPClient(GitHubMCP.get_params())

    async def start_conversation(self) -> None:
        loop = ConversationLoop()
        await loop.run(self.ask, self.mcp_client.cleanup)

    async def ask(self, question: str) -> str:
        answer = self.llm_session.ask(question)
        result = await self._process(answer)
        return result

    async def _process(self, answer: str) -> str:
        answer_json = json.loads(answer)
        if answer_json.get("type") == "final_answer":
            return answer_json.get("answer_markdown")

        method = answer_json.get("method")
        tool_name = answer_json.get("tool_name")
        arguments = answer_json.get("arguments")
        print(f"MCP request: method={method}, tool={tool_name}, args={arguments}")

        response = await self.mcp_client.execute(method, tool_name, arguments)
        mcp_response = json.dumps(response)

        answer = self.llm_session.ask(mcp_response)
        return await self._process(answer)
