import datetime
from pathlib import Path
from typing import List, Dict, Union, Callable
import ast
import re

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
from ..integrated.signatures.input_patterns_based_output_pattern_description import input_based_output_pattern_chat, InputPatternsBasedOutputPatternDescription
from ..integrated.signatures.annotate_input_patterns import annotate_patterns_chat, AnnotatePatterns
from .signatures.pattern_description_python_code import PatternDescriptionPythonCode, pattern_description_python_code


class TrainingCasesBasedPatternExtractor:
    """Class for extracting patterns based on test cases."""

    def __init__(self, training_set: List[InputOutputPair]):
        """
        Initialize the TestCasesBasedPatternExtractor.

        Args:
            training_set (List[InputOutputPair]): List of input-output pairs for training.
        """
        self.training_set: List[InputOutputPair] = training_set
        self.input_pattern_description: PatternDetails = None
        self.output_pattern_descriptions: List[PatternDetails] = []
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/pattern_extraction_{self.time}.txt"

    
    def find_probable_causation(self, page_number: int) -> ProbableCausation:
        """Find probable causation."""
        probable_causation = cached_call(probable_causation_chat.send_message)(f"integrated/probable_causation_{page_number}.pickle", ["causation_description"])
        causation_response = probable_causation(
            challenge_description = challenge_description_obj,
            question = ProbableCausation.sample_prompt(),
            input_ouptut_pairs = self.training_set
        )
        print(causation_response.causation_description)
        self.probable_causation = causation_response.causation_description
        return causation_response.causation_description
    

    def find_input_patterns(self, page_number: int) -> PatternDetails:
        """Find patterns based on the training set."""
        matrix_type = 'input'

        probable_causation = self.probable_causation
        io_based_pattern = cached_call(io_based_pattern_chat.send_message)(f"integrated/io_based_pattern_description_{page_number}.pickle", ["pattern_description"])
        pattern_description_response = io_based_pattern(
            challenge_description = challenge_description_obj,
            question = IOBasedPatternDescription.sample_prompt(),
            input_ouptut_pairs = self.training_set,
            probable_causation = self.probable_causation,
            FOR_MATRIX_TYPE = matrix_type
        )
        print(pattern_description_response.pattern_description)
        
        self.input_pattern_description = pattern_description_response.pattern_description
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
                    assert (len(m.matrix) == num_of_rows, 
                            f"The number of rows in the output matrix is not the same as the input matrix for the output matrix at index {index}.")
                    assert (len(m.matrix[0]) == num_of_cols, 
                            f"The number of columns in the output matrix is not the same as the input matrix for the output matrix at index {index}.")

            return True
        except Exception as e:
            return str(e)
        

    def find_python_code(self, page_number: int, grid_type: str) -> List[PatternDetails]:
        """Find python code corresponding to the input or output pattern description."""
        pattern_description_python_code = cached_call(self._find_python_code)
        if grid_type == 'input':
            python_code = pattern_description_python_code\
                (f"integrated/pattern_description_python_code_{page_number}_{grid_type}.pickle")\
                ([io_pair.input for io_pair in self.training_set], self.input_pattern_description)
            self.input_extraction_python_code = python_code
            return self.input_extraction_python_code
        elif grid_type == 'output':
            self.output_extraction_python_codes = []
            for i, (input_output_pair, output_pattern_description) in enumerate(zip(self.training_set, self.output_pattern_descriptions)):
                python_code = pattern_description_python_code\
                    (f"integrated/pattern_description_python_code_{page_number}_{grid_type}_{i}.pickle")\
                    ([input_output_pair.output], output_pattern_description)
                self.output_extraction_python_codes.append(python_code)
            return self.output_extraction_python_codes
        else:
            raise ValueError(f"Invalid grid type: {grid_type}")


    def patterns_extractor(self, grid_type: str):
        """
        Extract patterns from input or output matrices using the corresponding Python functions.
        
        Args:
        grid_type (str): Either 'input' or 'output'.
        """
        if grid_type not in ['input', 'output']:
            raise ValueError(f"Invalid grid type: {grid_type}")
        
        if grid_type == 'input':
            self.input_extracted_patterns_programatically = []
            for io_pair in self.training_set:
                func = self._get_python_function(self.input_extraction_python_code)
                patterns = func(io_pair.input.matrix)
                self.input_extracted_patterns_programatically.append([Matrix(matrix=pattern) for pattern in patterns])
        else:  # output
            self.output_extracted_patterns_programatically = []
            for i, io_pair in enumerate(self.training_set):
                func = self._get_python_function(self.output_extraction_python_codes[i])
                patterns = func(io_pair.output.matrix)
                self.output_extracted_patterns_programatically.append([Matrix(matrix=pattern) for pattern in patterns])
        
        print(f"Extracted {grid_type} patterns programmatically.")


    def decompose_input_grids(self):
        """Decompose grids into patterns."""
        
        matrix_type = 'input'

        extracted_input_patterns = []  # New dictionary to store the results

        for i, input_output_pair in enumerate(self.training_set):
            grid = input_output_pair.input if matrix_type == 'input' else input_output_pair.output
            
            
            print("=" * 80)
            print(f"Extracting patterns in accordance to the pattern description from grid {i+1}.")
            print(f"Pattern description: {self.input_pattern_description}")
            print(f"Grid: ")
            print(grid)
            print("=" * 80)
            extracted = extract_and_validate_patterns(grid, self.input_pattern_description, self.log_file)
            # Store the results in the nested dictionary
            extracted_input_patterns.append(extracted)

        self.input_extracted_patterns = extracted_input_patterns
        return extracted_input_patterns
    

    def find_output_patterns(self, page_number: int) -> List[PatternDetails]:
        """Find patterns based on the training set."""
        matrix_type = 'output'

        all_patterns_for_an_input_matrix = self.input_extracted_patterns

        all_pattern_descriptions = []
        for i, input_extracted_patterns in enumerate(self.input_extracted_patterns):
            input_based_ouptut_pattern = cached_call(input_based_output_pattern_chat.send_message)\
                                    (f"integrated/input_based_output_pattern_description_{page_number}_{i}.pickle", ["pattern_description"])
            pattern_description = input_based_ouptut_pattern(
                challenge_description = challenge_description_obj,
                question = InputPatternsBasedOutputPatternDescription.sample_prompt(),
                input_ouptut_pairs = self.training_set,
                probable_causation = self.probable_causation,
                input_matrix = self.training_set[i].input,
                extracted_input_patterns = all_patterns_for_an_input_matrix[i],
                output_matrix = self.training_set[i].output
            )
            all_pattern_descriptions.append(pattern_description.pattern_description)
        
        self.output_pattern_descriptions = all_pattern_descriptions


    def decompose_output_grids(self):
        """Decompose grids into patterns."""
        
        matrix_type = 'ouput'
        all_extracted_output_patterns = []
        for i, output_pattern_description in enumerate(self.output_pattern_descriptions):
                print("=" * 80)
                print(f"Extracting output patterns in accordance to the pattern description from grid {i+1}.")
                print(f"Pattern description: {output_pattern_description}")
                print(f"Grid: ")
                print(self.training_set[i].output)
                print("=" * 80)

                extracted_patterns = extract_and_validate_patterns(self.training_set[i].output, output_pattern_description)
                all_extracted_output_patterns.append(extracted_patterns)
        self.output_extracted_patterns = all_extracted_output_patterns


    def annotate_patterns(self, page_number: int):
        """Annotate input and output patterns and find detailed causation."""
        annotate_patterns = cached_call(annotate_patterns_chat.send_message)
        
        self.detailed_causation = []
        self.annotated_input_patterns = []
        self.annotated_output_patterns = []

        for i, (input_patterns, output_patterns) in enumerate(zip(self.input_extracted_patterns, self.output_extracted_patterns)):
            annotation_response = annotate_patterns(
            f"integrated/annotate_patterns_io_{i}_page_{page_number}.pickle", 
            ["detailed_causation", "annotated_input_patterns", "annotated_output_patterns"]
            )\
            (
                challenge_description=challenge_description_obj,
                question=AnnotatePatterns.sample_prompt(),
                input_ouptut_pairs=self.training_set,
                probable_causation=self.probable_causation,
                input_matrix=self.training_set[i].input,
                extracted_input_patterns=input_patterns,
                output_matrix=self.training_set[i].output,
                extracted_output_patterns=output_patterns
            )
            
            # Store the results
            self.detailed_causation.append(annotation_response.detailed_causation)
            self.annotated_input_patterns.append(annotation_response.annotated_input_patterns)
            self.annotated_output_patterns.append(annotation_response.annotated_output_patterns)
            
            print("=" * 80)
            print(f"Detailed causation for grid pair {i+1}:")
            print(self.detailed_causation[-1])
            print("\nAnnotated input patterns:")
            for pattern in self.annotated_input_patterns[-1]:
                print(f"Matrix: {pattern.matrix}")
                print(f"Annotations: {pattern.annotations}")
            print("\nAnnotated output patterns:")
            for pattern in self.annotated_output_patterns[-1]:
                print(f"Matrix: {pattern.matrix}")
                print(f"Annotations: {pattern.annotations}")
            print("=" * 80)

