from typing import Any

from anthropic import Anthropic

from llm_clients.client_abc import LlmClient


class AnthropicClient(LlmClient):
    def __init__(
        self, model_name: str = "claude-3-5-sonnet-20241022", max_tokens: int = 8000
    ):
        self.anthropic = Anthropic()
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.available_tools = None
        self.call_tool_closure = None
        self.message_history = []

    def set_available_tools(self, tools):
        self.available_tools = tools

    def set_call_tool_closure(self, call_tool_closure):
        self.call_tool_closure = call_tool_closure

    def _add_user_message(self, content: str) -> None:
        self.message_history.append({"role": "user", "content": content})

    def _add_assistant_message(self, response) -> None:
        self.message_history.append({"role": "assistant", "content": response.content})

    async def _call_llm(self, tools, messages=None) -> Any:
        if messages is None:
            messages = []
        return self.anthropic.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=messages,
            tools=tools,
        )

    def _construct_tool_llm_message(self, tool_id: str, content: str) -> dict:
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": content,
                }
            ],
        }

    def _extract_tool_name_args_id_from_response(self, response: Any) -> Any:
        for content in response.content:
            if content.type == "tool_use":
                return content.name, content.input, content.id  # type: ignore
        return None, None, None

    def _extract_text_from_llm_response(self, response) -> list[str]:
        text_content = []
        for content in response.content:
            if content.type == "text":
                text_content.append(content.text)
        return text_content

    async def process_user_query(self, query: str) -> str:
        human_readable_message_history = []

        self._add_user_message(query)
        response = await self._call_llm(self.available_tools, self.message_history)
        self._add_assistant_message(response)
        human_readable_message_history.extend(
            self._extract_text_from_llm_response(response)
        )

        (
            tool_name,
            tool_args,
            tool_id,
        ) = self._extract_tool_name_args_id_from_response(response)
        if tool_name is not None:
            tool_call_result = await self.call_tool_closure(tool_name, tool_args)  # type: ignore
            self.message_history.append(
                self._construct_tool_llm_message(tool_id, tool_call_result.content)
            )
            self._add_user_message("extract text from tool call result")
            response = await self._call_llm(
                tools=self.available_tools,
                messages=self.message_history,
            )
            human_readable_message_history.append(response.content[0].text)
            human_readable_message_history.append(
                f"[Called tool {tool_name} with args {tool_args}]"
            )
        return "\n".join(human_readable_message_history)
