from typing import Dict, List, Callable, Union
from .llm_connector import LLMConnector
import anthropic

class Claude(LLMConnector):
    def __init__(self, strategy_method: str, system_info: str = "", model: str = "claude-3-sonnet-20240229") -> None:
        super().__init__(strategy_method, system_info)
        self.model = model
        self.__chat_history = []
        self.initialize_claude()

    def initialize_claude(self) -> None:
        import os
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        print("Initialized Claude LLM")

    def chat_history(self) -> List[Dict[str, str]]:
        return self.__chat_history

    def clear_chat(self) -> None:
        self.__chat_history = []
        print("Chat history cleared")

    def _one_shot(self, message: Union[str, List[str]]) -> str:
        if isinstance(message, str):
            messages = [{"role": "user", "content": message}]
        elif isinstance(message, list):
            messages = [{"role": "user", "content": m} for m in message]
        else:
            raise ValueError("Message must be a string or a list of strings")

        if self.system_info:
            messages.insert(0, {"role": "system", "content": self.system_info})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages
        )

        return response.content[0].text

    def _chat(self, message: Union[str, List[str]]) -> str:
        if isinstance(message, str):
            new_messages = [{"role": "user", "content": message}]
        elif isinstance(message, list):
            new_messages = [{"role": "user", "content": m} for m in message]
        else:
            raise ValueError("Message must be a string or a list of strings")

        messages = self.__chat_history + new_messages

        if self.system_info and not self.__chat_history:
            messages.insert(0, {"role": "system", "content": self.system_info})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages
        )

        self.__chat_history.extend(new_messages)
        self.__chat_history.append({"role": "assistant", "content": response.content[0].text})

        return response.content[0].text

    # Alias methods for compatibility
    def one_shot(self, message: Union[str, List[str]]) -> str:
        return self._one_shot(message)

    def chat(self, message: Union[str, List[str]]) -> str:
        return self._chat(message)

