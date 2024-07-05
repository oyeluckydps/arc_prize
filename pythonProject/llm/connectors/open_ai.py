from typing import Dict, List, Callable
from .llm_connector import LLMConnector

class OpenAI(LLMConnector):
    def __init__(self, strategy_method: str, system_info: str = "") -> None:
        super().__init__(strategy_method, system_info)
        self.initialize_open_ai()

    def initialize_open_ai(self) -> None:
        # Placeholder function for Open AI LLM initialization
        print("Initialized Open AI LLM")

    def chat_history(self, message: str) -> str:
        raise NotImplementedError("OpenAI's chat_history is not implemented.")

    def clear_chat(self, message: str) -> str:
        raise NotImplementedError("OpenAI's chat_history is not implemented.")

    def one_shot(self, message: str) -> str:
        raise NotImplementedError("OpenAI's one_shot strategy not provided")

    def chat(self, message: str) -> str:
        raise NotImplementedError("OpenAI's chat strategy not provided")


