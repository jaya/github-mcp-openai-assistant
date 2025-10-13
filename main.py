#!/usr/bin/env python3

import asyncio
from dotenv import load_dotenv
from code_assistant import CodeAssistant

# Load environment variables from .env file
load_dotenv()


async def main() -> None:
    """Start the GitHub Code Assistant in interactive mode"""
    assistant = CodeAssistant()

    # Start interactive conversation
    await assistant.start_conversation()


if __name__ == "__main__":
    asyncio.run(main())
