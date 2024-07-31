import os, sys
from typing import List, Optional, Dict, Union
import dspy
from pydantic import BaseModel, Field, ConfigDict
from .pattern_description_signature import PatternDetails
from custom_types.matrix import Matrix

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class PatternDescriptionPythonCode(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    question: str = dspy.InputField()
    matrices: Union[List[Matrix], Matrix] = dspy.InputField()
    pattern_description: PatternDetails = dspy.InputField()

    python_code: str = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        Given the following pattern description in JSON format and the sample matrix or matrices, your task is to write a python code that can
        be used to extract the patterns adhering to the pattern description from the matrix or matrices.
        For writing the python code, use the algorithm provided under the extraction field in the pattern description to extract the patterns. 
        Use other fields like description, location, unique_identifier, etc to your advantage to extract the patterns.
        Write your code as a python function that takes one matrix which is a list of lists of ints/None as input and 
        returns a list of patterns in the form of matrices (a list of lists of ints/None) as output.
        In writing the python code, make sure that you put all the assumptions and constraints of the pattern description in the code.
        Try to make all the assumptions in the code as general as possible. Make them dependent on variables and declare them at the top of the function.
        Describe all the constraints as separate functions and call them in the code when needed.
        Replace all other entries that are not a part of the pattern being extracted in the matrix with None.
        Do not use any external libraries or packages. You may use the built-in python libraries like math, random, etc only if required.
        Make sure that the value returned from teh function is a list of list of list of ints/None, which is a list of matrices and not a single matrix.
        If a single matrix is the output, return a list of one matrix.
        Ensure that the dimension of each matric in the output list is the same as the dimension of the input matrix. 
        This is a must and you must write a code in such a way that the elements of output list has the same dimension as the input matrix.

        Do not write anthing else other than the python code in your response. Put appropriate comments and documentation in the code.
        """
        return prompt

pattern_description_python_code = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=PatternDescriptionPythonCode)
