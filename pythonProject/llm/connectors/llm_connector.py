from abc import ABC, abstractmethod
from typing import Dict, List, Callable

class LLMConnector(ABC):
    def __init__(self, strategy_method: str, system_info: str = "") -> None:
        self.strategy_method: str = strategy_method if strategy_method is not None else 'one_shot'
        self.system_info: str = system_info
        self.one_shot_history: List[Dict[str, str]] = []

        # Initialize strategies
        self.strategies: Dict[str, Callable[[str], str]] = {
            'one_shot': self.one_shot,
            'chat': self.chat
        }        
        self.current_strategy: Callable[[str], str] = self.strategies[strategy_method] if strategy_method in self.strategies else None

    @abstractmethod
    def chat_history(self, message: str) -> str:
        pass

    @abstractmethod
    def clear_chat(self, message: str) -> str:
        pass

    def send_message(self, *args, **kwargs) -> str:
        response = self.current_strategy(*args, **kwargs)
        if self.current_strategy == self.one_shot:
            self.one_shot_history.append({"role": "user", "content": args})
            self.one_shot_history.append({"role": "user", "content": kwargs})
            self.one_shot_history.append({"role": "assistant", "content": response})
        return response

    @abstractmethod
    def one_shot(self, message: str) -> str:
        pass

    @abstractmethod
    def chat(self, message: str) -> str:
        pass

    def change_strategy(self, new_strategy_method: str) -> None:
        if new_strategy_method in self.strategies:
            self.current_strategy = self.strategies[new_strategy_method]
        else:
            raise ValueError("Unsupported strategy")