import json
from typing import Any

from openai import OpenAI

from llm_clients.client_abc import LlmClient


class OpenAIClient(LlmClient):
    def __init__(self, model_name: str = "gpt-4.1", max_tokens: int = 8000):
        self.openai = OpenAI()
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.awailable_tools = None
        self.call_tool_closure = None
        self.message_history = []

    def set_available_tools(self, tools):
        self.available_tools = self._construct_tools_for_llm(tools)

    def set_call_tool_closure(self, call_tool_closure):
        self.call_tool_closure = call_tool_closure

    def _add_user_message(self, content: str) -> None:
        self.message_history.append({"role": "user", "content": content})

    def _add_assistant_message(self, response) -> None:
        self.message_history.append(
            {"role": "assistant", "content": response.output[0].content[0].text}
        )

    async def _call_llm(self, tools, messages=None) -> Any:
        if messages is None:
            messages = []
        return self.openai.responses.create(
            model=self.model_name,
            max_output_tokens=self.max_tokens,
            input=messages,
            tools=tools,
        )

    def _construct_tool_llm_message(self, tool_call_id: str, tool_call_result) -> dict:
        content = (
            tool_call_result[0].text
            if hasattr(tool_call_result[0], "text")
            else str(tool_call_result)
        )
        return {
            "role": "user",
            "content": f"Tool call result for {tool_call_id}: {content}",
        }

    def _extract_tool_name_args_id_from_response(self, response: Any) -> Any:
        if hasattr(response, "output") and response.output:
            if hasattr(response.output[0], "name") and hasattr(
                response.output[0], "arguments"
            ):
                return (
                    response.output[0].name,
                    json.loads(response.output[0].arguments),
                    response.output[0].call_id,
                )
        return (None, None, None)

    def _extract_text_from_llm_response(self, response) -> list[str]:
        if hasattr(response.output[0], "content"):
            return [content.text for content in response.output[0].content]
        return []

    def _construct_tools_for_llm(self, tools) -> Any:
        out = []
        for t in tools:
            tool_obj = {
                "type": "function",
                "name": t["name"],
                "description": t.get("description", "") or "",
                "parameters": {
                    "type": t["input_schema"]["type"],
                    "properties": t["input_schema"]["properties"],
                },
                "required": t["input_schema"]["required"],
            }
            out.append(tool_obj)
        return out

    async def process_user_query(self, query: str) -> str:
        human_readable_message_history = []

        self.message_history.append({"role": "user", "content": query})
        response = await self._call_llm(self.available_tools, self.message_history)
        self.message_history += response.output
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
                {
                    "type": "function_call_output",
                    "call_id": tool_id,
                    "output": tool_call_result.content[0].text,
                }
            )
            self.message_history.append(
                self._construct_tool_llm_message(tool_id, tool_call_result.content)
            )
            self.message_history.append(
                {"role": "user", "content": "extract text from tool call result"}
            )
            response = await self._call_llm(
                tools=self.available_tools,
                messages=self.message_history,
            )
            human_readable_message_history.append(response.output[0].content[0].text)
            human_readable_message_history.append(
                f"[Called tool {tool_name} with args {tool_args}]"
            )
        return "\n".join(human_readable_message_history)
