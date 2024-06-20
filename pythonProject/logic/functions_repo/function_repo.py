from abc import ABC, abstractmethod
from typing import List, Callable, Any

class functionRepo(ABC):
    @abstractmethod
    def __init__(self, input_type: Any, output_type: Any, method: Callable = None, description: str = "", params: List[Any] = None):
        self.input_type = input_type
        self.output_type = output_type
        self.method = method
        self.description = description
        self.params = params if params is not None else []

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
