import datetime
from typing import List, Dict, Any
from pathlib import Path

from preprocess_sample_json import pp

from .models import PatternTree, SchemaOfDecomposition, PatternNode
from ..utils import log_interaction, load_cached_data, save_cached_data, dspy_detailed_pattern_descriptor, dspy_short_pattern_descriptor, dspy_pattern_extractor, dspy_most_relevant_pattern_descriptor
from .pattern_extractor import extract_and_validate_patterns
from .validation import check_completeness
from .signatures.pattern_description_signature import DetailedPatternDescriptionSignature, Matrix, PatternDetails
from .signatures.most_relevant_pattern_description_signature import MostRelevantPatternDescriptionSignature
from .short_pattern_description_signature import ShortPatternDescriptionSignature
from .signatures.pattern_extraction_signature import PatternExtractionSignature
from globals import IS_DEBUG


class GridPatternExtractor:
    """Class for extracting patterns from grids."""

    def __init__(self, grids: List[Matrix], grids_type: str = 'Input'):
        """
        Initialize the GridPatternExtractor.

        Args:
            grids (List[Matrix]): List of input grids.
            grids_type (str, optional): Type of grids. Defaults to 'Input'.
        """
        self.grids = grids
        self.grids_type = grids_type
        self.pattern_trees: List[PatternTree] = [PatternTree(grid) for grid in grids]
        self.schema = SchemaOfDecomposition()
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/pattern_extraction_{self.time}.txt"

    def find_basic_patterns(self) -> List[PatternDetails]:
        """Find patterns in the grids."""
        prompt = ShortPatternDescriptionSignature.sample_prompt()
        matrices = {f"{self.grids_type} Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        
        if IS_DEBUG:
            filename = Path(__file__).parent / "sample_short_pattern_description.pickle"
            cached_data = load_cached_data(filename)
            if cached_data:
                return cached_data
            
        response = dspy_short_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        log_interaction(self.log_file, prompt, response)
        
        if IS_DEBUG:
            save_cached_data(filename, response.patterns_description.list_of_patterns)
        
        return response.patterns_description.list_of_patterns

    def find_most_relevant_pattern(self) -> PatternDetails:
        """Find a single most relevant pattern in the grids."""
        prompt = MostRelevantPatternDescriptionSignature.sample_prompt()
        matrices = {f"{self.grids_type} Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        
        if IS_DEBUG:
            filename = Path(__file__).parent / "sample_most_relevant_pattern_description.pickle"
            cached_data = load_cached_data(filename)
            if cached_data:
                return cached_data
            
        response = dspy_most_relevant_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        log_interaction(self.log_file, prompt, response)
        
        if IS_DEBUG:
            save_cached_data(filename, response.pattern_description)
        
        return response.pattern_description

    def find_patterns(self) -> List[PatternDetails]:
        """Find patterns in the grids."""
        prompt = DetailedPatternDescriptionSignature.sample_prompt()
        matrices = {f"{self.grids_type} Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        
        if IS_DEBUG:
            filename = Path(__file__).parent / "sample_pattern_description.pickle"
            cached_data = load_cached_data(filename)
            if cached_data:
                print("Pattern descriptions loaded from cache")
                return cached_data
            
        response = dspy_detailed_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        log_interaction(self.log_file, prompt, response)
        print(f"A total of {len(response.patterns_description.list_of_patterns)=} pattern descriptions were found in the grid through LLM.")

        if IS_DEBUG:
            save_cached_data(filename, response.patterns_description.list_of_patterns)
            print("Pattern descriptions saved to cache")

        return response.patterns_description.list_of_patterns


    def decompose_grids(self):
        """Decompose grids into patterns."""
        # patterns = self.find_patterns()

        pattern = self.find_most_relevant_pattern()

        patterns = [pattern]
        
        for i, grid in enumerate(self.grids):
            extracted_patterns = []
            pattern_descriptions = []
            
            for j, pattern in enumerate(patterns):
                # if j<2:
                #     continue
                if i + 1 in pattern.matrices:
                    print("=" * 80)
                    print(f"Extracting patterns in accordance to {j+1}th pattern description from grid {i+1}.")
                    print(f"Pattern description: {pattern}")
                    print(f"Grid: ")
                    pp.pprint(grid.matrix)
                    print("=" * 80)
                    extracted = extract_and_validate_patterns(grid, pattern, self.log_file)
                    extracted_patterns.extend(extracted)
                    pattern_descriptions.append(pattern)
            
            # # Check for completeness
            # uncovered_cells = check_completeness(grid, extracted_patterns)
            # if uncovered_cells:
            #     completeness_report = self.validator.report_generator.generate_completeness_report(grid, uncovered_cells)
            #     # Handle the completeness failure (e.g., log it, send it back to LLM, etc.)
            #     log_interaction(self.log_file, "Completeness check failed", completeness_report)
            #     # You might want to add logic here to refine the patterns based on the completeness report
            
            # # Check for overlap among all extracted patterns
            # check_grid = self.validator._calculate_check_grid(grid, extracted_patterns)
            # overlaps = self.validator._check_overlaps(check_grid)
            # if overlaps:
            #     overlap_report = self.validator.report_generator.generate_overlap_report(grid, extracted_patterns, overlaps)
            #     # Handle the overlap failure (e.g., log it, send it back to LLM, etc.)
            #     log_interaction(self.log_file, "Overlap check failed", overlap_report)
            #     # You might want to add logic here to refine the patterns based on the overlap report
            
            self._build_pattern_tree(self.pattern_trees[i], extracted_patterns, pattern_descriptions)
        
        self._build_schema_of_decomposition(patterns)

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

    