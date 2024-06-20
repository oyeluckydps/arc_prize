from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.group import Group
from ..object_type.super_group import SuperGroup

class groupExpansion(functionRepo):
    """
    Class for group expansion functions.

    Attributes:
        input_type (Group): The type of input the function takes (Group).
        output_type (SuperGroup): The type of output the function returns (SuperGroup).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the groupExpansion with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Group, output_type=SuperGroup, method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        """
        Executes the group expansion function with the given arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")