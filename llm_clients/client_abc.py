from typing import Any

from abc import ABC, abstractmethod


class LlmClient(ABC):
    @abstractmethod
    async def _call_llm(self, tools, messages=None) -> Any:
        pass

    @abstractmethod
    def set_available_tools(self, tools):
        pass

    @abstractmethod
    def set_call_tool_closure(self, call_tool_closure):
        pass
