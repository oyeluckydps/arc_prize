from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.pattern import Pattern
from ..object_type.cell import Cell

class patternContraction(functionRepo):
    """
    Class for pattern contraction functions.

    Attributes:
        input_type (Pattern): The type of input the function takes (Pattern).
        output_type (Cell): The type of output the function returns (Cell).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the patternContraction with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Pattern, output_type=Cell, method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        """
        Executes the pattern contraction function with the given arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")

