from .function_repo import functionRepo
from typing import Any, Callable, List
from ..object_type.grid import Grid
from ..object_type.group import Group

class groupExtraction(functionRepo):
    """
    Class for group extraction functions.

    Attributes:
        input_type (Grid): The type of input the function takes (Grid).
        output_type (List[Group]): The type of output the function returns (List[Group]).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the groupExtraction with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Grid, output_type=List[Group], method=method, description=description, params=params)

    def execute(self, *args, **kwargs):
        """
        Executes the group extraction function with the given arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")

    def iter(self):
        """
        Iterates over the extracted groups.

        Yields:
            Group: The next group in the list.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.method:
            for group in self.method():
                yield group
        else:
            raise NotImplementedError("Method not implemented")