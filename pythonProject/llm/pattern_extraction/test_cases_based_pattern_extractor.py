import datetime
from pathlib import Path
from typing import List
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

class TestCasesBasedPatternExtractor:
    """Class for extracting patterns based on test cases."""

    def __init__(self, training_set: List[InputOutputPair]):
        """
        Initialize the TestCasesBasedPatternExtractor.

        Args:
            training_set (List[InputOutputPair]): List of input-output pairs for training.
        """
        self.training_set: List[InputOutputPair] = training_set
        self.pattern_descriptions: List[PatternDetails] = None
        # self.pattern_trees: List[PatternTree] = [PatternTree(Matrix(matrix=pair['input'])) for pair in training_set]
        # self.schema = SchemaOfDecomposition()
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/pattern_extraction_{self.time}.txt"

    def find_patterns(self, page_number: int, matrix_type: str) -> PatternDetails:
        """Find patterns based on the training set."""

        assert matrix_type in ['input', 'output']

        probable_causation = cached_call(probable_causation_chat.send_message)(f"integrated/probable_causation_{page_number}.pickle", ["causation_description"])
        causation_response = probable_causation(
            challenge_description = challenge_description_obj,
            question = ProbableCausation.sample_prompt(),
            input_ouptut_pairs = self.training_set
        )
        print(causation_response.causation_description)
        
        io_based_pattern = cached_call(io_based_pattern_chat.send_message)(f"integrated/io_based_pattern_description_{page_number}.pickle", ["pattern_description"])
        pattern_description_response = io_based_pattern(
            challenge_description = challenge_description_obj,
            question = IOBasedPatternDescription.sample_prompt(),
            input_ouptut_pairs = self.training_set,
            probable_causation = causation_response.causation_description,
            FOR_MATRIX_TYPE = matrix_type
        )
        print(pattern_description_response.pattern_description)
        
        self.pattern_descriptions = [pattern_description_response.pattern_description]

    def decompose_grids(self, matrix_type: str):
        """Decompose grids into patterns."""
        
        assert matrix_type in ['input', 'output']

        for i, input_output_pair in enumerate(self.training_set):
            grid = input_output_pair.input if matrix_type == 'input' else input_output_pair.output
            extracted_patterns = []
            pattern_descriptions_for_this_grid = []
            
            for j, pattern in enumerate(self.pattern_descriptions):
                print("=" * 80)
                print(f"Extracting patterns in accordance to the pattern description from grid {i+1}.")
                print(f"Pattern description: {pattern}")
                print(f"Grid: ")
                print(grid)
                print("=" * 80)
                extracted = extract_and_validate_patterns(grid, pattern, self.log_file)
                extracted_patterns.extend(extracted)
                pattern_descriptions_for_this_grid.append(pattern)
            
        #     self._build_pattern_tree(self.pattern_trees[i], extracted_patterns, pattern_descriptions_for_this_grid)
        
        # self._build_schema_of_decomposition(pattern_descriptions_for_this_grid)

    def _build_pattern_tree(self, tree: PatternTree, extracted_patterns: List[Matrix], pattern_descriptions: List[PatternDetails]):
        """Build a pattern tree for a single grid."""
        for pattern, description in zip(extracted_patterns, pattern_descriptions):
            child = PatternNode(pattern, description)
            if tree.root.children is None:
                tree.root.children = []
            tree.root.children.append(child)

    def _build_schema_of_decomposition(self, patterns: List[PatternDetails]):
        """Build the schema of decomposition."""
        for pattern in patterns:
            child = PatternNode(Matrix(matrix=[]), pattern)
            if self.schema.root.children is None:
                self.schema.root.children = []
            self.schema.root.children.append(child)