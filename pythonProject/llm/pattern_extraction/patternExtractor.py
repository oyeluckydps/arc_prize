import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
import datetime

from ..connectors.dspy import DSPy
import dspy
from ..connectors.dspy_LMs.claude_chat import ClaudeChat
from pattern_description_signature import PatternSignature

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

dspy_pattern_descriptor = DSPy(strategy_method='chat', system_info='', model=claude, chat_model=claude_chat, io_signature=PatternSignature)


@dataclass
class PatternNode:
    pattern: List[List[Optional[int]]]
    description: Dict[str, Any]
    children: List['PatternNode'] = None

class PatternTree:
    def __init__(self, grid: List[List[int]]):
        self.root = PatternNode(grid, {"description": "Original Grid"})

class SchemaOfDecomposition:
    def __init__(self):
        self.root = PatternNode(None, {"description": "Schema Root"})

class GridPatternExtractor:
    def __init__(self, grids: List[List[List[int]]]):
        """
        Initialize the GridPatternExtractor with a list of grids.
        
        Args:
            grids (List[List[List[int]]]): A list of grids, where each grid is a list of lists with numerical entries between 0 and 9.
        """
        self.grids = grids
        self.pattern_trees: List[PatternTree] = [PatternTree(grid) for grid in grids]
        self.schema = SchemaOfDecomposition()
        self.log_file = f"pattern_extraction_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"

    def log_interaction(self, prompt: str, response: str):
        """
        Log the interaction with the LLM to a file.
        
        Args:
            prompt (str): The prompt sent to the LLM.
            response (str): The response received from the LLM.
        """
        with open(self.log_file, 'a') as f:
            f.write(f"Prompt: {prompt}\n\n")
            f.write(f"Response: {response}\n\n")
            f.write("-" * 80 + "\n\n")

    def find_patterns(self) -> Dict[str, Any]:
        """
        Find patterns in the grids by making a call to an LLM.
        
        Returns:
            Dict[str, Any]: JSON response containing the identified patterns.
        """
        grids_str = ""
        for i, grid in enumerate(self.grids, 1):
            grids_str += f"Grid {i}:\n{json.dumps(grid, indent=2)}\n\n"

        prompt = f"""
        Please identify non-overlapping and distinct common patterns or features across the given input matrices. List any unique patterns or exceptions that do not conform to these common patterns. Ensure that the patterns are exhaustive such that if one were to remove the patterns one by one from a matrix, nothing should remain.

        In this list of patterns:

        Focus only on describing the physical patterns or features you observe in the matrices.
        Ensure that the patterns identified are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.

        Examples:

        If you see a background across all the input matrices, mention "background" as a single pattern.
        If you see square shapes of different sizes that can be generalized, mention "squares."
        If you observe random patterns at the same location in the matrices, mention "random pattern at the particular corner of matrix."

        Here are the input matrices:
        """
        matrices={f"Matrix {i+1}": grid for i, grid in enumerate(self.grids)}
        response = dspy_pattern_descriptor.send_message(question=prompt, matrices=matrices)
        self.log_interaction(prompt, response)
        return json.loads(response)

    def extract_pattern(self, grid: List[List[int]], pattern_description: Dict[str, Any]) -> List[List[List[Optional[int]]]]:
        """
        Extract a specific pattern from a grid based on the pattern description.
        
        Args:
            grid (List[List[int]]): The input grid.
            pattern_description (Dict[str, Any]): The description of the pattern to extract.
        
        Returns:
            List[List[List[Optional[int]]]]: A list of extracted patterns as matrices.
        """
        prompt = f"""
        Given the following pattern description in JSON format:

        {json.dumps(pattern_description, indent=2)}

        Your task is to identify this pattern in the input matrix that will be provided. Extract the pattern from the matrix, preserving its digits and positions. Replace all other entries in the matrix with ".".
        Present your result as a list of lists, with each inner list on a new line, like this:
        [
        [0, ".", ".", 0],
        [".", 0, 0, "."],
        [0, ".", ".", 0]
        ]

        Here's the input matrix:

        {json.dumps(grid)}

        Please process this matrix and output the result showing only the identified pattern.

        If there are multiple patterns to be found in the matrix that satisfy the description for the pattern then output all of these matrices as a list.
        """
        
        response = self.chat(prompt)
        self.log_interaction(prompt, response)
        return json.loads(response)

    def validate_decomposition(self, original_grid: List[List[int]], extracted_patterns: List[List[List[Optional[int]]]], pattern_descriptions: List[Dict[str, Any]]) -> List[str]:
        """
        Validate the pattern decomposition based on the given rules.
        
        Args:
            original_grid (List[List[int]]): The original grid.
            extracted_patterns (List[List[List[Optional[int]]]]): The list of extracted patterns.
            pattern_descriptions (List[Dict[str, Any]]): The descriptions of the patterns.
        
        Returns:
            List[str]: A list of failure reports, if any.
        """
        failure_reports = []
        
        # Check if patterns are present in the original grid
        for i, pattern in enumerate(extracted_patterns):
            if not self._is_pattern_in_grid(pattern, original_grid):
                failure_reports.append(f"Pattern not present in the original grid.\n"
                                       f"Pattern description: {json.dumps(pattern_descriptions[i], indent=2)}\n"
                                       f"Extracted pattern: {json.dumps(pattern, indent=2)}\n"
                                       f"Original grid: {json.dumps(original_grid, indent=2)}\n"
                                       f"The extracted pattern does not match any part of the original grid.")
        
        # Check if patterns combine to form the original grid
        if not self._do_patterns_form_grid(extracted_patterns, original_grid):
            failure_reports.append(f"Extracted patterns do not combine to form the complete original grid.\n"
                                   f"Original grid: {json.dumps(original_grid, indent=2)}\n"
                                   f"Extracted patterns: {json.dumps(extracted_patterns, indent=2)}\n"
                                   f"The combination of all extracted patterns does not recreate the original grid exactly.")
        
        # Check if patterns are non-overlapping
        overlapping_patterns = self._are_patterns_non_overlapping(extracted_patterns)
        if overlapping_patterns:
            overlap_report = f"Extracted patterns are overlapping in the following grid:\n"
            overlap_report += f"Original grid: {json.dumps(original_grid, indent=2)}\n\n"
            overlap_report += "Overlapping patterns:\n"
            for i, j in overlapping_patterns:
                overlap_report += f"Pattern 1:\n"
                overlap_report += f"Description: {json.dumps(pattern_descriptions[i], indent=2)}\n"
                overlap_report += f"Extracted pattern: {json.dumps(extracted_patterns[i], indent=2)}\n\n"
                overlap_report += f"Pattern 2:\n"
                overlap_report += f"Description: {json.dumps(pattern_descriptions[j], indent=2)}\n"
                overlap_report += f"Extracted pattern: {json.dumps(extracted_patterns[j], indent=2)}\n\n"
            overlap_report += "These patterns have non-None values in the same position, indicating overlap."
            failure_reports.append(overlap_report)
        
        return failure_reports

    def _is_pattern_in_grid(self, pattern: List[List[Optional[int]]], grid: List[List[int]]) -> bool:
        for i in range(len(grid) - len(pattern) + 1):
            for j in range(len(grid[0]) - len(pattern[0]) + 1):
                if self._match_pattern(pattern, grid, i, j):
                    return True
        return False

    def _match_pattern(self, pattern: List[List[Optional[int]]], grid: List[List[int]], start_i: int, start_j: int) -> bool:
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                if pattern[i][j] is not None and pattern[i][j] != grid[start_i + i][start_j + j]:
                    return False
        return True

    def _do_patterns_form_grid(self, patterns: List[List[List[Optional[int]]]], grid: List[List[int]]) -> bool:
        combined_grid = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]
        for pattern in patterns:
            for i in range(len(pattern)):
                for j in range(len(pattern[0])):
                    if pattern[i][j] is not None:
                        if combined_grid[i][j] is None:
                            combined_grid[i][j] = pattern[i][j]
                        elif combined_grid[i][j] != pattern[i][j]:
                            return False
        return combined_grid == grid

    def _are_patterns_non_overlapping(self, patterns: List[List[List[Optional[int]]]]) -> List[Tuple[int, int]]:
        """
        Check if the given patterns are non-overlapping.
        
        Args:
            patterns (List[List[List[Optional[int]]]]): The list of patterns to check.
        
        Returns:
            List[Tuple[int, int]]: List of pairs of indices of overlapping patterns, empty if no overlap.
        """
        overlapping_patterns = []
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                if self._patterns_overlap(patterns[i], patterns[j]):
                    overlapping_patterns.append((i, j))
        return overlapping_patterns

    def _patterns_overlap(self, pattern1: List[List[Optional[int]]], pattern2: List[List[Optional[int]]]) -> bool:
        """
        Check if two patterns overlap.
        
        Args:
            pattern1 (List[List[Optional[int]]]): First pattern.
            pattern2 (List[List[Optional[int]]]): Second pattern.
        
        Returns:
            bool: True if patterns overlap, False otherwise.
        """
        for i in range(len(pattern1)):
            for j in range(len(pattern1[0])):
                if pattern1[i][j] is not None and pattern2[i][j] is not None:
                    return True
        return False

    def correct_pattern_finding(self, failure_reports: List[str], original_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correct the pattern finding based on failure reports.
        
        Args:
            failure_reports (List[str]): List of failure reports.
            original_patterns (Dict[str, Any]): The original patterns identified.
        
        Returns:
            Dict[str, Any]: Corrected patterns.
        """
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
        """
        Decompose all grids into patterns and build the schema of decomposition.
        """
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
                
                failure_reports = self.validate_decomposition(grid, extracted_patterns, pattern_descriptions)
                all_failure_reports.extend(failure_reports)
            
            if not all_failure_reports:
                break
            
            patterns = self.correct_pattern_finding(all_failure_reports, patterns)
        
        self._build_pattern_trees(patterns)
        self._build_schema_of_decomposition(patterns)

    def _build_pattern_trees(self, patterns: Dict[str, Any]):
        """
        Build pattern trees for all grids.
        
        Args:
            patterns (Dict[str, Any]): The overall pattern descriptions.
        """
        for i, grid in enumerate(self.grids):
            extracted_patterns = []
            for pattern in patterns["list_of_patterns"]:
                pattern_name = list(pattern.keys())[0]
                pattern_desc = pattern[pattern_name]
                if i + 1 in pattern_desc["in which input matrices is it found?"]:
                    extracted = self.extract_pattern(grid, pattern_desc)
                    extracted_patterns.extend(extracted)
            
            self._build_pattern_tree(self.pattern_trees[i], extracted_patterns, patterns)

    def _build_pattern_tree(self, tree: PatternTree, extracted_patterns: List[List[List[Optional[int]]]], patterns: Dict[str, Any]):
        """
        Build the pattern tree for a single grid.
        
        Args:
            tree (PatternTree): The pattern tree to build.
            extracted_patterns (List[List[List[Optional[int]]]]): The extracted patterns for this grid.
            patterns (Dict[str, Any]): The overall pattern descriptions.
        """
        for i, pattern in enumerate(extracted_patterns):
            pattern_desc = patterns["list_of_patterns"][i][list(patterns["list_of_patterns"][i].keys())[0]]
            child = PatternNode(pattern, pattern_desc)
            if tree.root.children is None:
                tree.root.children = []
            tree.root.children.append(child)

    def _build_schema_of_decomposition(self, patterns: Dict[str, Any]):
        """
        Build the schema of decomposition based on the identified patterns.
        
        Args:
            patterns (Dict[str, Any]): The identified patterns.
        """
        for pattern in patterns["list_of_patterns"]:
            pattern_name = list(pattern.keys())[0]
            pattern_desc = pattern[pattern_name]
            child = PatternNode(None, pattern_desc)
            if self.schema.root.children is None:
                self.schema.root.children = []
            self.schema.root.children.append(child)

# Example usage
grids = [
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
    [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
]

extractor = GridPatternExtractor(grids)
extractor.decompose_grids()

# Access the results
for i, tree in enumerate(extractor.pattern_trees):
    print(f"Grid {i + 1} decomposition:")
    print(json.dumps(tree.root.pattern, indent=2))
    for child in tree.root.children:
        print(json.dumps(child.pattern, indent=2))
        print(json.dumps(child.description, indent=2))
    print()

print("Schema of decomposition:")
for child in extractor.schema.root.children:
    print(json.dumps(child.description, indent=2))