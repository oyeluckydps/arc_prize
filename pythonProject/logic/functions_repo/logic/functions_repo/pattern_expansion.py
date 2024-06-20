class patternExpansion(functionRepo):
    """
    Class for pattern expansion functions.

    Attributes:
        input_type (Pattern): The type of input the function takes (Pattern).
        output_type (Group): The type of output the function returns (Group).
        method (Callable): The function to be executed.
        description (str): A description of the function.
        params (List[Any]): A list of parameters for the function.
    """

    def __init__(self, method: Callable = None, description: str = "", params: List[Any] = None):
        """
        Initializes the patternExpansion with the given attributes.

        Args:
            method (Callable, optional): The function to be executed. Defaults to None.
            description (str, optional): A description of the function. Defaults to "".
            params (List[Any], optional): A list of parameters for the function. Defaults to None.
        """
        super().__init__(input_type=Pattern, output_type=Group, method=method, description=description, params=params)

    def expand_pattern_to_group(pattern, repetitions=3, translation=(1, 1)):
        """
        Expands a pattern into a group by replicating and translating it multiple times.

        Args:
            pattern (Pattern): The pattern to be expanded.
            repetitions (int): Number of times the pattern is to be replicated. Default is 3.
            translation (tuple): The x and y translation offsets for each replication. Default is (1, 1).

        Returns:
            Group: A group consisting of the replicated and translated patterns.
        """
        group = Group()
        for i in range(repetitions):
            translated_pattern = translate_pattern(pattern, (translation[0]*i, translation[1]*i))
            group.add(translated_pattern)
        return group
