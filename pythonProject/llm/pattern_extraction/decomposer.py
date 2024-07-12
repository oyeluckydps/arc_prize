import json
import datetime
from typing import List, Dict, Any
from .models import PatternTree, SchemaOfDecomposition, PatternNode
from .utils import dspy_pattern_descriptor, dspy_pattern_extractor, pp
from .validation import Validator
from .pattern_description_signature import PatternDescriptionSignature, Matrix, PatternDetails
from .pattern_extraction_signature import PatternExtractionSignature

class GridPatternExtractor:
    def __init__(self, grids: List[Matrix], grids_type: str = 'Input'):
        self.grids = grids
        self.grids_type = grids_type
        self.pattern_trees: List[PatternTree] = [PatternTree(grid) for grid in grids]
        self.schema = SchemaOfDecomposition()
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"pattern_extraction_{self.time}.txt"
        self.validator = Validator()

    def log_interaction(self, prompt: str, response: str):
        with open(self.log_file, 'a') as f:
            f.write(f"Prompt: {prompt}\n\n")
            f.write(f"Response: {response}\n\n")
            f.write("-" * 80 + "\n\n")

    def find_patterns(self) -> List[PatternDetails]:
        prompt = PatternDescriptionSignature.sample_prompt()
        matrices = {f"{self.grids_type} Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        response = dspy_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        self.log_interaction(prompt, response)
        return response.patterns_description.list_of_patterns

    def extract_pattern(self, grid: Matrix, pattern_description: PatternDetails) -> List[Matrix]:
        prompt = PatternExtractionSignature.sample_prompt(grid, pattern_description)
        response = dspy_pattern_extractor.send_message(query=prompt, matrix=grid, pattern_description=pattern_description)
        self.log_interaction(prompt, response)
        return list(response.output_pattern)

    def correct_pattern_finding(self, failure_reports: List[str]) -> List[PatternDetails]:
        prompt = f"""
        Based on the pattern descriptions, patterns were identified for each grid. However, the following validation failures were reported:
        
        {json.dumps(failure_reports, indent=2)}

        Please correct the pattern descriptions that you found so that it addresses these failures. Ensure that the corrected patterns are non-overlapping, distinct, and exhaustive.
        """
        matrices = {f"{self.grids_type} Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        response = dspy_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        self.log_interaction(prompt, response)
        return response.patterns_description.list_of_patterns

    def decompose_grids(self):
        while True:
            patterns = self.find_patterns()
            all_failure_reports = []

            for i, grid in enumerate(self.grids):
                extracted_patterns = []
                pattern_descriptions = []
                for pattern in patterns:
                    pattern_name = pattern.name
                    pattern_desc = pattern
                    if i + 1 in pattern_desc.matrices:
                        extracted = self.extract_pattern(grid, pattern_desc)
                        extracted_patterns.append(extracted)
                        pattern_descriptions.append(pattern_desc)
                
                failure_reports = self.validator.validate_decomposition(grid, extracted_patterns, pattern_descriptions)
                all_failure_reports.extend(failure_reports)
            
            pp.pprint(all_failure_reports)

            if not all_failure_reports:
                break
            
            patterns = self.correct_pattern_finding(all_failure_reports, patterns)
        
        self._build_pattern_trees(patterns)
        self._build_schema_of_decomposition(patterns)

    def _build_pattern_trees(self, patterns: Dict[str, Any]):
        for i, grid in enumerate(self.grids):
            extracted_patterns = []
            for pattern in patterns["list_of_patterns"]:
                pattern_name = list(pattern.keys())[0]
                pattern_desc = pattern[pattern_name]
                if i + 1 in pattern_desc["in which input matrices is it found?"]:
                    extracted = self.extract_pattern(grid, pattern_desc)
                    extracted_patterns.extend(extracted)
            
            self._build_pattern_tree(self.pattern_trees[i], extracted_patterns, patterns)

    def _build_pattern_tree(self, tree: PatternTree, extracted_patterns: List[Matrix], patterns: Dict[str, Any]):
        for i, pattern in enumerate(extracted_patterns):
            pattern_desc = patterns["list_of_patterns"][i][list(patterns["list_of_patterns"][i].keys())[0]]
            child = PatternNode(pattern, pattern_desc)
            if tree.root.children is None:
                tree.root.children = []
            tree.root.children.append(child)

    def _build_schema_of_decomposition(self, patterns: Dict[str, Any]):
        for pattern in patterns["list_of_patterns"]:
            pattern_name = list(pattern.keys())[0]
            pattern_desc = pattern[pattern_name]
            child = PatternNode(Matrix(matrix=[]), pattern_desc)
            if self.schema.root.children is None:
                self.schema.root.children = []
            self.schema.root.children.append(child)
    
    