import json
import datetime
from typing import List, Dict, Any
from .models import PatternTree, SchemaOfDecomposition, PatternNode
from .utils import dspy_pattern_descriptor, dspy_pattern_extractor
from .validation import Validator
from .pattern_description_signature import PatternDescriptionSignature, Matrix
from .pattern_extraction_signature import PatternExtractionSignature

class GridPatternExtractor:
    def __init__(self, grids: List[Matrix]):
        self.grids = grids
        self.pattern_trees: List[PatternTree] = [PatternTree(grid) for grid in grids]
        self.schema = SchemaOfDecomposition()
        self.log_file = f"pattern_extraction_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"
        self.validator = Validator()

    def log_interaction(self, prompt: str, response: str):
        with open(self.log_file, 'a') as f:
            f.write(f"Prompt: {prompt}\n\n")
            f.write(f"Response: {response}\n\n")
            f.write("-" * 80 + "\n\n")

    def find_patterns(self) -> Dict[str, Any]:
        prompt = PatternDescriptionSignature.sample_prompt()
        matrices = {f"Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        response = dspy_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        self.log_interaction(prompt, response)
        return response.patterns_description.list_of_patterns

    def extract_pattern(self, grid: Matrix, pattern_description: Dict[str, Any]) -> List[Matrix]:
        prompt = PatternExtractionSignature.sample_prompt(grid, pattern_description)
        response = dspy_pattern_extractor.send_message(query=prompt, matrix=grid, pattern_description=pattern_description)
        self.log_interaction(prompt, response)
        return list(response.output_pattern)

    def correct_pattern_finding(self, failure_reports: List[str], original_patterns: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        The following patterns were originally identified:
        {json.dumps(original_patterns, indent=2)}

        However, the following validation failures were reported:
        {json.dumps(failure_reports, indent=2)}

        Please correct the pattern finding to address these failures. Ensure that the corrected patterns are non-overlapping, distinct, and exhaustive.

        Provide your corrected findings in the same JSON format as before.
        """
        
        response = self.chat(prompt)
        self.log_interaction(prompt, response)
        return json.loads(response)

    def decompose_grids(self):
        while True:
            patterns = self.find_patterns()
            all_failure_reports = []

            for i, grid in enumerate(self.grids):
                extracted_patterns = []
                pattern_descriptions = []
                for pattern in patterns["list_of_patterns"]:
                    pattern_name = list(pattern.keys())[0]
                    pattern_desc = pattern[pattern_name]
                    if i + 1 in pattern_desc["in which input matrices is it found?"]:
                        extracted = self.extract_pattern(grid, pattern_desc)
                        extracted_patterns.extend(extracted)
                        pattern_descriptions.extend([pattern_desc] * len(extracted))
                
                failure_reports = self.validator.validate_decomposition(grid, extracted_patterns, pattern_descriptions)
                all_failure_reports.extend(failure_reports)
            
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