class groupContraction(functionRepo):
    """
    Class for group contraction functions.

    Attributes:
        input_type (Group): The type of input the function takes (Group).
        output_type (Pattern): The type of output the function returns (Pattern).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the groupContraction with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Group, output_type=Pattern, method=method, description=description, params=params)

    def extract_pattern_from_group(group, selection_criteria='most_occurrences'):
        """
        Extracts a specific pattern from a group based on a given selection criteria.

        Args:
            group (Group): The group from which the pattern is to be extracted.
            selection_criteria (str): Criteria for selecting the pattern ('most_occurrences', 'left_top', etc.). Default is 'most_occurrences'.

        Returns:
            Pattern: The extracted pattern based on the selection criteria.
        """
        if selection_criteria == 'most_occurrences':
            # Assuming a method to find the pattern with the most occurrences
            return find_most_occurrences(group)
        elif selection_criteria == 'left_top':
            # Assuming a method to find the left-top occurring pattern
            return find_left_top_pattern(group)
        return None