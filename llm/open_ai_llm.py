#!/usr/bin/env python3

import os


class OpenAiSession:
    """
    OpenAI session that maintains conversation context.
    Encapsulates system prompts and conversation history.
    """

    def __init__(self):
        self._load_system_prompts()
        self.conversation_messages = []

    def _load_system_prompts(self) -> None:
        from llm.prompt_loader import PromptLoader
        import json

        self.system_prompt = PromptLoader.load_prompt("natural-github.txt")
        self.tools_prompt = PromptLoader.load_prompt("tools.json")
        self.identity_msg = {
            "type": "identity",
            "github_login": os.getenv("GITHUB_LOGIN"),
        }

        self.system_prompts = [
            self.system_prompt,
            json.dumps(self.tools_prompt),
            json.dumps(self.identity_msg),
        ]

    def ask(self, question: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        if not self.conversation_messages:
            messages = [
                {"role": "system", "content": prompt} for prompt in self.system_prompts
            ]
        else:
            messages = self.conversation_messages.copy()

        messages.append({"role": "user", "content": question})

        resp = client.chat.completions.create(model="gpt-5", messages=messages)
        answer = (resp.choices[0].message.content or "").strip()

        messages.append({"role": "assistant", "content": answer})
        self.conversation_messages = messages

        return answer
