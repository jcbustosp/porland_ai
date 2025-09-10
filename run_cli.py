import asyncio

from contextlib import AsyncExitStack
from pydantic_ai.messages import (
    ModelResponse,
    TextPart,
)

from src.toolfront.db_agent import agent

class DatabaseAgent():
    def __init__(self):
        self._exit_stack = AsyncExitStack()
        self.agent = agent

    def run(self):
        """Runs the main interaction loop with the agent."""
        print("🤖 Agent ready. Type a query or 'exit' to quit.")

        # Need to run the interaction loop within an async context to properly manage the exit stack
        asyncio.run(self._run_async())
    
    async def _run_async(self):
        """Asynchronous part of the interaction loop."""
        message_history = []
        async with self._exit_stack:
            while True:
                user_input = input("🧑 You: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("👋 Goodbye!")
                    break

                try:
                    async with agent.run_stream(user_input,
                                     message_history=message_history
                    ) as result:
                        
                        partial_text = ""

                        async for chunk in result.stream_text(delta=True):
                            partial_text += chunk
                            
                        message_history.append(ModelResponse(parts=[TextPart(content=partial_text)]))
                        print(f"🤖 Agent: {partial_text}\n")

                except KeyboardInterrupt:
                    print("\n👋 Interrupted. Exiting chat.")
                    break
                
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    import traceback
                    traceback.print_exc()

    def __del__(self):
        """Ensures the exit stack is closed when the app is deleted."""
        # The AsyncExitStack should be closed by the async with statement in _run_async
        # This __del__ is just a fallback, but the primary cleanup happens in _run_async
        pass


if __name__ == "__main__":
    app = DatabaseAgent()
    app.run()