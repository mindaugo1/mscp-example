from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from client.client import ChatClient
from llm_clients.anthropic_client import AnthropicClient


class StdioChatClient(ChatClient):
    def __init__(self, llm_client):
        super().__init__(llm_client=llm_client)
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command="uv", args=["run", "-m", "server.server_script"], env=None
        )
        self.stdio, self.write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        await self.session.initialize()
        print("Connected to server")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = StdioChatClient(llm_client=AnthropicClient())
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
