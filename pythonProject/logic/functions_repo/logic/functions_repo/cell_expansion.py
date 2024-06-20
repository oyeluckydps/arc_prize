class cellExpansion(functionRepo):
    """
    Class for cell expansion functions.

    Attributes:
        input_type (Cell): The type of input the function takes (Cell).
        output_type (Pattern): The type of output the function returns (Pattern).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the cellExpansion with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Cell, output_type=Pattern, method=method, description=description, params=params)

    def expand_to_square(cell, side_length=3):
        """
        Expands a single cell into a square pattern.

        Args:
            cell (Cell): The cell to replicate.
            side_length (int): The length of the sides of the square. Default is 3.

        Returns:
            Pattern: A pattern object representing a square made of the input cell.
        """
        pattern = Pattern()
        for _ in range(side_length):
            for _ in range(side_length):
                pattern.add(cell.copy())  # Assuming a copy method exists in Cell class
        return pattern
