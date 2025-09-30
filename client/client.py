from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class ChatClient(ABC):
    def __init__(self, llm_client):
        self.session = None
        self.llm_client = llm_client
        self.message_history = []
        self.human_readable_message_history = []

    @abstractmethod
    async def connect_to_server(self):
        pass

    @abstractmethod
    async def cleanup(self):
        pass

    async def _get_available_tools(self):
        if not self.session:
            return []

        response = await self.session.list_tools()  # type: ignore
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]
        return available_tools

    async def call_tool_closure(self):
        async def call_tool(tool_name, tool_args):
            if tool_name is not None:
                tool_call_result = await self.session.call_tool(  # type: ignore
                    name=tool_name, arguments=tool_args
                )
                return tool_call_result
            else:
                return "No tool was called. Missing tool name."

        return call_tool

    async def _process_user_query(self, query: str) -> str:
        self.llm_client.set_available_tools(await self._get_available_tools())
        self.llm_client.set_call_tool_closure(await self.call_tool_closure())
        return await self.llm_client.process_user_query(query)

    async def chat_loop(self):
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("Query: ").strip()

                if query.lower() == "quit":
                    break

                response = await self._process_user_query(query)
                print(response)
                print(self.message_history)

            except Exception as e:
                print(f"Error: {str(e)}")
