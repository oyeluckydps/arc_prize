import ast
from typing import List, Tuple, Dict, Callable, Any, Union
from .error_handling import ErrorHandler
import re

class PythonCodeGenerationClass:
    def __init__(self, 
                 llm_call_function: Callable,
                 validation_function: Callable[[Any, Tuple, Dict], Union[bool, str]],
                 argument_tuples: List[Tuple],
                 keyword_argument_dicts: List[Dict]):
        self.validation_function = validation_function
        self.argument_tuples = argument_tuples
        self.keyword_argument_dicts = keyword_argument_dicts
        self.llm_call_function = llm_call_function
        self.generated_code = None
        self.func = None
        self.max_retries = 3

    def generate_code(self, **kwargs):
        """
        Generate Python code using the provided signature class and arguments.
        """
        code_response = self.llm_call_function(**kwargs)
        python_code = code_response.python_code
        pattern = r"```python\n(.*?)```"
        match = re.search(pattern, python_code, re.DOTALL)
        if match:
            python_code = match.group(1).strip()
        self.generated_code = python_code
        self.func = self._get_python_function(self.generated_code)
        return self.generated_code

    def validate_code(self):
        """
        Validate the generated Python code using the provided validation function.
        """
        if not self.func:
            raise ValueError("No function has been generated yet. Call generate_code() first.")
        
        for index, (args, kwargs) in enumerate(zip(self.argument_tuples, self.keyword_argument_dicts)):
            try:
                result = self.func(*args, **kwargs)
            except Exception as e:
                return ErrorHandler.handle_execution_error(str(e), args, kwargs, index)
            
            try:
                validation_result = self.validation_function(index,result, args, kwargs)
                if isinstance(validation_result, str):
                    return ErrorHandler.handle_validation_error(validation_result, result, args, kwargs, index)
            except Exception as e:
                return ErrorHandler.handle_validation_error(str(e), result, args, kwargs, index)
        
        return True

    def _execute_code(self, *args, **kwargs):
        """
        Call the python function generated from the output of the LLM>
        """
        if not self.func:
            raise ValueError("No function has been generated yet. Call generate_code() first.")
        return self.func(*args, **kwargs)
    


    def execute_code(self):
        """
        Execute the generated and validated Python code with the provided arguments.
        """
        if not self.func:
            raise ValueError("No function has been generated yet. Call generate_code() first.")
        
        results = []

        for args, kwargs in zip(self.argument_tuples, self.keyword_argument_dicts):
            result = self._execute_code(*args, **kwargs)
            results.append(result)

        return results

    @staticmethod
    def _get_python_function(python_code: str) -> Callable:
        """
        Get the Python function from the generated Python code.
        """
        tree = ast.parse(python_code)
        function_name = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)][0].name
        exec(python_code, globals())
        func = globals()[function_name]
        return func

    def generate_until_success(self, max_retries: int = None, **kwargs):
        """
        Generate, validate, and execute the code with retries.
        """
        for attempt in range(self.max_retries if max_retries is None else max_retries):
            self.generate_code(**kwargs)
            validation_result = self.validate_code()
            
            if validation_result is True:
                return self.execute_code()
            else:
                # If validation_result is not True, it's an error prompt
                kwargs['question'] += f"\n\nAdditional instructions:\n{validation_result}"
        
        raise ValueError(f"Maximum retries ({self.max_retries}) exceeded. Unable to generate valid code.")
    
