import os, sys
from typing import List, Optional, Dict, Union
import dspy
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix
from .causal_input_patterns import RelevantInputPatternMap

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class MappingFunctionPythonCode(dspy.Signature):
    """
    Defines the input and output fields for the mapping function description task.
    """
    relevant_input_pattern_map: RelevantInputPatternMap = dspy.InputField()
    question: str = dspy.InputField()

    python_code: str = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        You are given a RelevantInputPatternMap object containing:
        1. annotated_input_patterns: A list of annotated input patterns
        2. annotated_output_pattern: An annotated output pattern
        3. relevant_input_pattern_tags: A list of tags for relevant input patterns
        4. detailed_causation: A detailed description of the transformation process

        Your task is to write a Python function that implements the transformation described in the detailed_causation. The function should:

        1. Input: A dictionary where
           - Keys are the tags of the relevant input patterns
           - Values are matrices (list of lists of ints or None) representing those patterns

        2. Output: A single matrix (list of lists of ints or None) representing the output pattern

        Requirements:
        - Write a single main function named 'transform_patterns' that contains all the logic.
        - You can include helper functions inside the main function if needed.
        - Clearly state all assumptions and constraints as comments at the beginning of the function.
        - Use only built-in Python libraries if absolutely necessary.
        - Ensure the output matrix has the same dimensions as the input matrices.
        - Include appropriate comments explaining the transformation steps.
        - Only use the input patterns specified in the relevant_input_pattern_tags list.
        - Implement the transformation exactly as described in the detailed_causation.

        Function signature:
        def transform_patterns(input_patterns: Dict[str, List[List[Union[int, None]]]) -> List[List[Union[int, None]]]:

        Your response should contain only the Python code for this function, nothing else.
        """
        return prompt

mapping_function_python_code = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=MappingFunctionPythonCode)


