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

    def reduce_to_single_cell(pattern):
        """
        Reduces a pattern to a single cell by selecting the top-most left cell.

        Args:
            pattern (Pattern): The pattern to be reduced.

        Returns:
            Cell: The top-most left cell of the pattern.
        """
        # Assuming the Pattern class has a method to get cells and that cells are stored in a list of lists
        return pattern.cells[0][0]  # Returning the top-most left cell
