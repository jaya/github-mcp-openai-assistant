#!/usr/bin/env python3

import os
from typing import Dict, List, Optional, Tuple


class OpenAiLLM:
    """
    OpenAI LLM client abstraction.
    Provides a single public method to interact with OpenAI models.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    def ask(self, system_prompts: List[str], question: str, assistant_prompt: Optional[str] = None) -> Tuple[str, List[Dict]]:
        from openai import (
            OpenAI,  # local import to avoid hard dependency at import time
        )

        client = OpenAI(api_key=self.api_key)

        # Build messages array
        messages = [{"role": "system", "content": prompt} for prompt in system_prompts]
        messages.append({"role": "user", "content": question})

        if assistant_prompt:
            messages.append({"role": "assistant", "content": assistant_prompt})

        print("Asking OpenAI...")
        resp = client.chat.completions.create(
            model="gpt-5",
            messages=messages
        )
        answer = (resp.choices[0].message.content or "").strip()
        return answer, messages
