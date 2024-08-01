class ErrorHandler:
    @staticmethod
    def handle_execution_error(error: str, args: Tuple, kwargs: Dict, index: int) -> str:
        prompt = f"""
        There was a problem executing the Python code with the following input:
        Arguments: {args}
        Keyword Arguments: {kwargs}
        Index: {index}
        
        The error encountered during execution was:
        {error}
        
        The Python code you've written is likely incorrect or incompatible with the provided arguments.
        Please rewrite the Python code, ensuring it can execute successfully with these inputs.
        """
        return prompt

    @staticmethod
    def handle_validation_error(error: str, result: Any, args: Tuple, kwargs: Dict, index: int) -> str:
        prompt = f"""
        The Python code executed successfully, but the result failed the validation criteria.
        
        Input:
        Arguments: {args}
        Keyword Arguments: {kwargs}
        Index: {index}
        
        Generated Result: {result}
        
        Validation Error: {error}
        
        The generated result does not meet the expected criteria. Please rewrite the code,
        keeping in mind that this was the result generated, and it does not follow the
        validation criteria that were previously described.
        """
        return prompt
    
    