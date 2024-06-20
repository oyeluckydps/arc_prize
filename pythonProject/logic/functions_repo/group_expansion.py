from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.group import Group
from ..object_type.super_group import SuperGroup

class groupExpansion(functionRepo):
    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        super().__init__(input_type=Group, output_type=SuperGroup, method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")
