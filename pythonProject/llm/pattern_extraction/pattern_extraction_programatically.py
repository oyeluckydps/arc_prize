import datetime
from pathlib import Path
from typing import List, Dict, Union, Callable
import ast
import re

from globals import VERSION
from llm.integrated.signatures.io_based_pattern_description import IOBasedPatternDescription, io_based_pattern_chat
from llm.causation.signatures.probable_causation import ProbableCausation, probable_causation_chat
from llm.challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from utils.cacher import cached_call
from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair
from .models import PatternTree, PatternNode, SchemaOfDecomposition
from .signatures.pattern_description_signature import PatternDetails
from utils.logger import log_interaction
from .pattern_extractor import extract_and_validate_patterns
from .signatures.pattern_description_python_code import PatternDescriptionPythonCode, pattern_description_python_code
from ..causation.signatures.causal_input_patterns import RelevantInputPatternMap, CausalInputPatterns, causal_input_patterns_chat

class PatternExtractionProgramatically:
    """Class for extracting patterns programmatically."""

    def __init__(self, training_set: List[InputOutputPair]):
        """
        Initialize the PatternExtractionProgramatically.

        Args:
            training_set (List[InputOutputPair]): List of input-output pairs for training.
        """
        self.training_set: List[InputOutputPair] = training_set
        self.input_pattern_description: PatternDetails = None
        self.output_pattern_description: PatternDetails = None
        self.relevant_input_patterns_map: List[List[RelevantInputPatternMap]] = []
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/pattern_extraction_{self.time}.txt"


    def find_probable_causation(self, page_number: int) -> ProbableCausation:
        """Find probable causation."""
        probable_causation = cached_call(probable_causation_chat.send_message)(f"integrated/{VERSION}/{page_number}/probable_causation.pickle", ["causation_description"])
        causation_response = probable_causation(
            challenge_description = challenge_description_obj,
            question = ProbableCausation.sample_prompt(),
            input_ouptut_pairs = self.training_set
        )
        print(causation_response.causation_description)
        self.probable_causation = causation_response.causation_description
        return causation_response.causation_description
    

    def find_pattern_description(self, page_number: int, grid_type: str) -> PatternDetails:
        """Find patterns based on the training set."""
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")

        io_based_pattern = cached_call(io_based_pattern_chat.send_message)\
                            (f"integrated/{VERSION}/{page_number}/pattern_description_{grid_type}.pickle", ["pattern_description"])
        pattern_description_response = io_based_pattern(
            challenge_description = challenge_description_obj,
            question = IOBasedPatternDescription.sample_prompt(),
            input_ouptut_pairs = self.training_set,
            probable_causation = self.probable_causation,
            FOR_MATRIX_TYPE = grid_type
        )
        print(pattern_description_response.pattern_description)
        
        if grid_type == 'input':
            self.input_pattern_description = pattern_description_response.pattern_description
        else:
            self.output_pattern_description = pattern_description_response.pattern_description
        
        return pattern_description_response.pattern_description


    def _find_python_code(self, matrices: List[Matrix], pattern_description: PatternDetails) -> str:
        """
        Helper method to find python code corresponding to the pattern description and validate it.
        """
        
        code_response = pattern_description_python_code.send_message(
            question=PatternDescriptionPythonCode.sample_prompt(),
            matrices=matrices,
            pattern_description=pattern_description
        )
        python_code = code_response.python_code
        
        pattern = r"```python\n(.*?)```"
        match = re.search(pattern, python_code, re.DOTALL)
        if match:
            python_code = match.group(1).strip()
        
        validation_result = self._validate_python_code(python_code, matrices)
        if validation_result:
            print("Python code validation successful.")
            return python_code
        else:
            print(f"Python code validation failed: {validation_result}")
            raise ValueError(f"Invalid validation result: {validation_result}")


    def _get_python_function(self, python_code: str) -> Callable:
        """
        Get the Python function from the generated Python code.
        """
        tree = ast.parse(python_code)
        function_name = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)][0].name
        exec(python_code, globals())
        func = globals()[function_name]
        return func


    def _validate_python_code(self, python_code: str, matrices: List[Matrix]) -> Union[bool, str]:
        """
        Validate the generated Python code by executing it with sample matrices.
        Returns True if validation passes, or an error message as a string if it fails.
        """
        try:
            func = self._get_python_function(python_code)

            # Test the function with each matrix
            for matrix in matrices:
                res = func(matrix.matrix)
                num_of_rows, num_of_cols = len(matrix.matrix), len(matrix.matrix[0])
                matrices = [Matrix(matrix=matrix) for matrix in res]
                for index, m in enumerate(matrices):
                    assert len(m.matrix) == num_of_rows, \
                            f"The number of rows in the output matrix is not the same as the input matrix for the output matrix at index {index}."
                    assert len(m.matrix[0]) == num_of_cols, \
                            f"The number of columns in the output matrix is not the same as the input matrix for the output matrix at index {index}."

            return True
        except Exception as e:
            return str(e)
        

    def find_python_code(self, page_number: int) -> None:
        """Find python code corresponding to the input and output pattern descriptions."""
        pattern_description_python_code = cached_call(self._find_python_code)
        
        # For input
        input_python_code = pattern_description_python_code\
            (f"integrated/{VERSION}/{page_number}/input_pattern_extraction_code.pickle")\
            ([io_pair.input for io_pair in self.training_set], self.input_pattern_description)
        self.input_extraction_python_code = input_python_code

        # For output
        output_python_code = pattern_description_python_code\
            (f"integrated/{VERSION}/{page_number}/output_pattern_extraction_code.pickle")\
            ([io_pair.output for io_pair in self.training_set], self.output_pattern_description)
        self.output_extraction_python_code = output_python_code


    def patterns_extractor(self):
        """
        Extract patterns from input and output matrices using the corresponding Python functions.
        """
        self.input_extracted_patterns = []
        self.output_extracted_patterns = []

        input_func = self._get_python_function(self.input_extraction_python_code)
        output_func = self._get_python_function(self.output_extraction_python_code)

        for io_pair in self.training_set:
            # Extract input patterns
            input_patterns = input_func(io_pair.input.matrix)
            self.input_extracted_patterns.append([Matrix(matrix=pattern) for pattern in input_patterns])

            # Extract output patterns
            output_patterns = output_func(io_pair.output.matrix)
            self.output_extracted_patterns.append([Matrix(matrix=pattern) for pattern in output_patterns])
        
        print("Extracted input and output patterns programmatically.")


    def map_relevant_input_patterns(self, page_number: int):
        """
        Map relevant input patterns to output patterns for each input-output pair.
        """
        self.relevant_input_patterns_map = []

        for io_pair_index, (io_pair, input_patterns, output_patterns) in enumerate(zip(self.training_set, self.input_extracted_patterns, self.output_extracted_patterns)):
            output_pattern_maps = []

            for output_pattern_index, output_pattern in enumerate(output_patterns):
                cache_file = f"integrated/{VERSION}/{page_number}/relevant_input_pattern_map_{io_pair_index}_{output_pattern_index}.pickle"
                
                causal_input_patterns_result = cached_call(causal_input_patterns_chat.send_message)(
                    cache_file,
                    ["relevant_input_pattern_map"]
                )

                result = causal_input_patterns_result(
                    challenge_description=challenge_description_obj,
                    question=CausalInputPatterns.sample_prompt(),
                    probable_causation=self.probable_causation,
                    input_matrix=io_pair.input,
                    output_matrix=io_pair.output,
                    input_patterns=input_patterns,
                    output_pattern=output_pattern
                )

                output_pattern_maps.append(result.relevant_input_pattern_map)

            self.relevant_input_patterns_map.append(output_pattern_maps)

        print("Mapped relevant input patterns to output patterns.")

