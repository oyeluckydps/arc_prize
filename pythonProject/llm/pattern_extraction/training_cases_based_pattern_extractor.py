import datetime
from pathlib import Path
from typing import List, Dict
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
