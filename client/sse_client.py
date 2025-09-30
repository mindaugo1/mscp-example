from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

from client.client import ChatClient
from llm_clients.openai_client import OpenAIClient
from llm_clients.anthropic_client import AnthropicClient


class SSEChatClient(ChatClient):
    def __init__(self, sse_url, llm_client):
        super().__init__(llm_client=llm_client)
        self.exit_stack = AsyncExitStack()
        self.sse_url = sse_url

    async def connect_to_server(self):
        self.read, self.write = await self.exit_stack.enter_async_context(
            sse_client(self.sse_url)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
        await self.session.initialize()
        print(f"Connected to SSE server at {self.sse_url}")

    async def cleanup(self):
        await self.exit_stack.aclose()


if __name__ == "__main__":
    """Test scripts for SSEChatClient"""
    import asyncio

    async def main():
        client = SSEChatClient(
            llm_client=AnthropicClient(), sse_url="http://localhost:8080/sse"
        )
        try:
            await client.connect_to_server()
            await client.chat_loop()
        finally:
            await client.cleanup()

    async def test_query():
        client = SSEChatClient(
            llm_client=AnthropicClient(), sse_url="http://localhost:8080/sse"
        )
        try:
            await client.connect_to_server()
            response = await client._process_user_query("generate 2 domains for cars")
            print(response)
        finally:
            await client.cleanup()

    # asyncio.run(test_query())
    asyncio.run(main())
