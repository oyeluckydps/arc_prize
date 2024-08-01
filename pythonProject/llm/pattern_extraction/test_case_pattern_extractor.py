import datetime
from pathlib import Path
from typing import List, Dict
from llm.pattern_extraction.signatures.io_based_pattern_description import IOBasedPatternDescription, io_based_pattern_chat
from llm.causation.signatures.probable_causation import ProbableCausation, probable_causation_chat
from llm.challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from utils.cacher import cached_call
from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair
from .models import PatternTree, PatternNode, SchemaOfDecomposition
from .signatures.pattern_description_signature import PatternDescription
from utils.logger import log_interaction
from .pattern_extractor import extract_and_validate_patterns
from ..integrated.signatures.input_patterns_based_output_pattern_description import input_based_output_pattern_chat, InputPatternsBasedOutputPatternDescription

class TestCasePatternExtractor:
    """Class for extracting patterns based on test cases."""

    def __init__(self, test_input_matrix: Matrix, input_pattern_description: PatternDescription):
        """
        Initialize the TestCasesBasedPatternExtractor.

        Args:
            training_set (List[InputOutputPair]): List of input-output pairs for training.
        """
        self.input_matrix: Matrix = test_input_matrix
        self.input_pattern_description: PatternDescription = input_pattern_description
        self.output_pattern_descriptions: List[PatternDescription] = []
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/test_pattern_extraction_{self.time}.txt"


    def decompose_input_grids(self):
        """Decompose grids into patterns."""
        
        grid = self.input_matrix
                    
        print("=" * 80)
        print(f"Extracting patterns in accordance to the pattern description from grid {i+1}.")
        print(f"Pattern description: {self.input_pattern_description}")
        print(f"Grid: ")
        print(grid)
        print("=" * 80)
        extracted = extract_and_validate_patterns(grid, self.input_pattern_description, self.log_file)

        self.input_extracted_patterns = extracted
        return extracted


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
