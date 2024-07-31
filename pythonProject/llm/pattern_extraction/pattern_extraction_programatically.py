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
from ..causation.signatures.mapping_function_python_code import MappingFunctionPythonCode, mapping_function_python_code
from .signatures.pattern_count_and_description import PatternCountAndDescription, pattern_count_and_description_chat

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
        self.input_pattern_counts = []
        self.input_pattern_characteristics = []
        self.output_pattern_counts = []
        self.output_pattern_characteristics = []
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
            question = IOBasedPatternDescription.sample_prompt(grid_type),
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


    def count_and_describe_patterns(self, page_number: int, grid_type: str):
        """
        Count and describe pattern characteristics in input or output matrices based on their respective pattern descriptions.
        """
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")

        pattern_description = self.input_pattern_description if grid_type == 'input' else self.output_pattern_description
        
        for idx, io_pair in enumerate(self.training_set):
            matrix = io_pair.input if grid_type == 'input' else io_pair.output
            
            cache_file = f"integrated/{VERSION}/{page_number}/pattern_count_desc_{grid_type}_{idx}.pickle"
            
            result = cached_call(pattern_count_and_description_chat.send_message)(
                cache_file,
                ["pattern_count", "pattern_characteristics"]
            )(
                challenge_description=challenge_description_obj,
                pattern_description=pattern_description,
                matrix=matrix
            )
            
            if grid_type == 'input':
                self.input_pattern_counts.append(result.pattern_count)
                self.input_pattern_characteristics.append(result.pattern_characteristics)
            else:
                self.output_pattern_counts.append(result.pattern_count)
                self.output_pattern_characteristics.append(result.pattern_characteristics)

        print(f"Counted and described pattern characteristics in {grid_type} matrices.")


    def _input_pattern_description_code_validator(self, index:int, param_matrix:Matrix, result: List[Matrix]) -> bool:
        num_of_rows, num_of_cols = len(param_matrix.matrix), len(param_matrix.matrix[0])
        matrices = [Matrix(matrix=matrix) for matrix in result]
        assert len(result) == self.input_pattern_counts[index], \
                    f"""The number of patterns in the result of the function called with input matrix at index {index} 
                    is not the same as mentioned in the pattern_count for the matrix."""
        for index, m in enumerate(matrices):
            assert len(m.matrix) == num_of_rows, \
                    f"The number of rows in the output matrix is not the same as the input matrix for the output matrix at index {index}."
            assert len(m.matrix[0]) == num_of_cols, \
                    f"The number of columns in the output matrix is not the same as the input matrix for the output matrix at index {index}."
    
    def _output_pattern_description_code_validator(self, index:int, param_matrix:Matrix, result: List[Matrix]) -> bool:
        num_of_rows, num_of_cols = len(param_matrix.matrix), len(param_matrix.matrix[0])
        matrices = [Matrix(matrix=matrix) for matrix in result]
        assert len(result) == self.output_pattern_counts[index], \
                    f"""The number of patterns in the result of the function called with output matrix at index {index} 
                    is not the same as mentioned in the pattern_count for the matrix."""
        for index, m in enumerate(matrices):
            assert len(m.matrix) == num_of_rows, \
                    f"The number of rows in the output matrix is not the same as the input matrix for the output matrix at index {index}."
            assert len(m.matrix[0]) == num_of_cols, \
                    f"The number of columns in the output matrix is not the same as the input matrix for the output matrix at index {index}."


    def _find_python_code(self, matrices: List[Matrix], pattern_description: PatternDetails, 
                          pattern_counts: List[int], post_result_validation_function: Callable) -> str:
        """
        Helper method to find python code corresponding to the pattern description and validate it.
        """
        
        code_response = pattern_description_python_code.send_message(
            question=PatternDescriptionPythonCode.sample_prompt(),
            matrices=matrices,
            pattern_description=pattern_description,
            pattern_counts=pattern_counts
        )
        python_code = code_response.python_code
        
        pattern = r"```python\n(.*?)```"
        match = re.search(pattern, python_code, re.DOTALL)
        if match:
            python_code = match.group(1).strip()
        
        validation_result = self._validate_python_code(python_code, matrices, post_result_validation_function)
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


    def _validate_python_code(self, python_code: str, matrices: List[Matrix], post_result_validation_function: Callable) -> Union[bool, str]:
        """
        Validate the generated Python code by executing it with sample matrices.
        Returns True if validation passes, or an error message as a string if it fails.
        """
        try:
            func = self._get_python_function(python_code)

            # Test the function with each matrix
            for index, matrix in enumerate(matrices):
                res = func(matrix.matrix)
                post_result_validation_function(index, matrix, res)

            return True
        except Exception as e:
            return str(e)
        

    def find_python_code(self, page_number: int) -> None:
        """Find python code corresponding to the input and output pattern descriptions."""
        pattern_description_python_code = cached_call(self._find_python_code)
        
        # For input
        input_python_code = pattern_description_python_code\
            (f"integrated/{VERSION}/{page_number}/input_pattern_extraction_code.pickle")\
            ([io_pair.input for io_pair in self.training_set], self.input_pattern_description, 
             self.input_pattern_counts, self._input_pattern_description_code_validator)
        self.input_extraction_python_code = input_python_code

        # For output
        output_python_code = pattern_description_python_code\
            (f"integrated/{VERSION}/{page_number}/output_pattern_extraction_code.pickle")\
            ([io_pair.output for io_pair in self.training_set], self.output_pattern_description, 
             self.output_pattern_counts, self._output_pattern_description_code_validator)
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


    def find_mapping_python_code(self, page_number: int):
        """
        Generate, validate, and store Python code for each mapping in self.relevant_input_patterns_map.
        """
        self.mapping_python_codes = []

        for io_pair_index, output_pattern_maps in enumerate(self.relevant_input_patterns_map):
            io_pair_codes = []

            for output_pattern_index, relevant_input_pattern_map in enumerate(output_pattern_maps):
                cache_file = f"integrated/{VERSION}/{page_number}/mapping_function_python_code_{io_pair_index}_{output_pattern_index}.pickle"
                
                mapping_function_result = cached_call(mapping_function_python_code.send_message)(
                    cache_file,
                    ["python_code"]
                )

                result = mapping_function_result(
                    question=MappingFunctionPythonCode.sample_prompt(),
                    relevant_input_pattern_map=relevant_input_pattern_map
                )

                python_code = result.python_code

                # Extract code from markdown if necessary
                pattern = r"```python\n(.*?)```"
                match = re.search(pattern, python_code, re.DOTALL)
                if match:
                    python_code = match.group(1).strip()

                # Validate the generated Python code
                validation_result = self._validate_mapping_python_code(python_code, relevant_input_pattern_map)
                if validation_result is True:
                    print(f"Python code validation successful for mapping {io_pair_index}_{output_pattern_index}.")
                    io_pair_codes.append(python_code)
                else:
                    print(f"Python code validation failed for mapping {io_pair_index}_{output_pattern_index}: {validation_result}")
                    raise ValueError(f"Invalid validation result for mapping {io_pair_index}_{output_pattern_index}: {validation_result}")

            self.mapping_python_codes.append(io_pair_codes)
        return self.mapping_python_codes
    

    print("Generated and validated Python code for each mapping.")

    def _validate_mapping_python_code(self, python_code: str, relevant_input_pattern_map: RelevantInputPatternMap) -> Union[bool, str]:
        """
        Validate the generated Python code for mapping function.
        Returns True if validation passes, or an error message as a string if it fails.
        """
        try:
            func = self._get_python_function(python_code)

            # Create input dictionary using actual matrices from AnnotatedPattern objects
            input_dict = {}
            for annotated_pattern in relevant_input_pattern_map.annotated_input_patterns:
                tag = annotated_pattern.annotations.tag
                matrix = annotated_pattern.matrix.matrix  # Get the actual matrix (List[List[Union[int, None]]])
                input_dict[tag] = matrix

            # Test the function with the actual input
            result = func(input_dict)

            # Basic checks on the result
            assert isinstance(result, list), "Output is not a list"
            assert all(isinstance(row, list) for row in result), "Output is not a list of lists"
            assert all(all(isinstance(item, (int, type(None))) for item in row) for row in result), "Output contains non-int and non-None values"

            # You might want to add more specific checks based on your requirements

            return True
        except Exception as e:
            return str(e)
    
