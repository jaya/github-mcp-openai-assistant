#!/usr/bin/env python3

import os
import json
from typing import List, Dict
from mcp_components.mcp_host import MCPHost
from llm.prompt_loader import PromptLoader
from llm.open_ai_llm import OpenAiLLM


class CodeAssistant:

    def __init__(self, github_login: str = "michelhdoumit"):
        self.github_login = github_login
        self.llm = OpenAiLLM()
        self._load_system_prompts()
    
    def _load_system_prompts(self):
        """Load system prompts and identity configuration."""
        self.system_prompt = PromptLoader.load_prompt("natural-github.txt")
        self.tools_prompt = PromptLoader.load_prompt("tools.json")
        self.identity_msg = {"type": "identity", "github_login": self.github_login}
        
        self.system_prompts = [
            self.system_prompt,
            json.dumps(self.tools_prompt),
            json.dumps(self.identity_msg)
        ]
    
    async def ask(self, question: str) -> str:
        answer, messages = self.llm.ask(self.system_prompts, question)
        result = await self._process(answer, messages)
        return result
    
    async def _process(self, answer: str, messages: List[Dict]) -> str:        
        answer_json = json.loads(answer)
        
        if answer_json.get("type") == "final_answer":
            return answer_json.get("answer_markdown")
                    
        mcp_request = answer_json.get("rpc")
        mcp_response = await self._execute_mcp_request(mcp_request)
                    
        observation = {
            "type": "observation", 
            "mcp_request": json.dumps(mcp_request), 
            "mcp_response": json.dumps(mcp_response)
        }
        messages = messages + [{"role": "assistant", "content": json.dumps(observation)}]
                    
        system_prompts = [msg["content"] for msg in messages if msg["role"] == "system"]
        answer, messages = self.llm.ask(system_prompts, mcp_response, json.dumps(observation))
        
        return await self._process(answer, messages)
    
    async def _execute_mcp_request(self, mcp_request: Dict) -> str:

        github_token = os.getenv("GITHUB_TOKEN")
        mcp_host = MCPHost(github_token)
        mcp_response = await mcp_host.execute(mcp_request)
        return json.dumps(mcp_response)
    
    def _is_json(self, answer: str) -> bool:
        try:
            json.loads(answer)
            return True
        except:
            return False
