#!/usr/bin/env python3

import asyncio

from code_assistant import CodeAssistant


async def main() -> None:
    """Start the GitHub Code Assistant in interactive mode"""
    assistant = CodeAssistant()

    # Start interactive conversation
    await assistant.start_conversation()


if __name__ == "__main__":
    asyncio.run(main())
