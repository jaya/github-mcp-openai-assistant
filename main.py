#!/usr/bin/env python3

import asyncio
import sys

from code_assistant import CodeAssistant


async def main() -> None:
    """Asks the question or uses the input from the terminal"""
    question = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else input("Pergunta: ").strip()

    assistant = CodeAssistant()
    result = await assistant.ask(question)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())


