from collections.abc import Callable
from typing import ClassVar


class ConversationLoop:
    EXIT_COMMANDS: ClassVar[set[str]] = {"exit", "quit", "bye", "q"}

    async def run(self, on_ask: Callable[[str], str], on_cleanup: Callable[[], None]) -> None:
        print("🤖 GitHub Code Assistant - Interactive Mode")
        print("Type 'exit', 'quit', or 'bye' to end the conversation")
        print("=" * 50)

        try:
            while True:
                if not await self._handle_user_input(on_ask):
                    break
        finally:
            await on_cleanup()

    async def _handle_user_input(self, on_ask: Callable[[str], str]) -> bool:
        try:
            question = input("\nUser: ").strip()
            if question.lower() in self.EXIT_COMMANDS:
                print("👋 Goodbye!")
                return False
            if question:
                print("Assistant: Thinking ...")
                result = await on_ask(question)
                print("Assistant: ", result)
            return True
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return False
