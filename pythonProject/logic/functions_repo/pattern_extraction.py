from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.grid import Grid
from ..object_type.pattern import Pattern

class patternExtraction(functionRepo):
    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        super().__init__(input_type=Grid, output_type=List[Pattern], method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")

    def iter(self):
        if self.method:
            for pattern in self.method():
                yield pattern
        else:
            raise NotImplementedError("Method not implemented")
