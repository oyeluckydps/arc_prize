from typing import List, Callable, Any

class functionRepo:
    """
    Base class for function repositories.

    Attributes:
        input_type (Any): The type of input the function takes.
        output_type (Any): The type of output the function returns.
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, input_type: Any, output_type: Any, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the functionRepo with the given attributes.

        Args:
            input_type (Any): The type of input the function takes.
            output_type (Any): The type of output the function returns.
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        self.input_type = input_type
        self.output_type = output_type
        self.method = method
        self.description = description
        self.params = params if params is not None else []

    def execute(self, *args, **kwargs):
        """
        Executes the function with the given arguments.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        if self.method:
            return self.method(*args, **kwargs)
        else:
            raise NotImplementedError("Method not implemented")
