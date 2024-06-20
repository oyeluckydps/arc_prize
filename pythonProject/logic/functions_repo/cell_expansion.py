from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.cell import Cell
from ..object_type.pattern import Pattern

class cellExpansion(functionRepo):
    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        super().__init__(input_type=Cell, output_type=Pattern, method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")
