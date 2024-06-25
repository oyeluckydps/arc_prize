from typing import Dict, List, Callable
from .llm_connector import LLMConnector

class OpenAI(LLMConnector):
    def __init__(self, strategy_method: str, system_info: str = "") -> None:
        super().__init__(strategy_method, system_info)
        self.initialize_open_ai()

    def initialize_open_ai(self) -> None:
        # Placeholder function for Open AI LLM initialization
        print("Initialized Open AI LLM")

    def send_message(self, message: str) -> str:
        raise NotImplementedError("OpenAI's send_message implementation not provided")

    def zero_shot(self, message: str) -> str:
        raise NotImplementedError("OpenAI's zero_shot strategy not provided")

    def chain_of_thought(self, message: str) -> str:
        raise NotImplementedError("OpenAI's CoT strategy not provided")

    def loop(self, message: str) -> str:
        raise NotImplementedError("OpenAI's loop strategy not provided")
    
    