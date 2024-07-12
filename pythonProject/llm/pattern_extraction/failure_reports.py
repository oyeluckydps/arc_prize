from typing import List, Tuple
from .pattern_description_signature import Matrix, PatternDetails
import json

class FailureReportGenerator:
    """
    A class for generating failure reports for pattern extraction validation.
    """

    def generate_dimension_mismatch_report(self, original_grid: Matrix, extracted_patterns: List[List[Matrix]]) -> str:
        """
        Generate a report for dimension mismatch.

        Args:
            original_grid (Matrix): The original grid.
            extracted_patterns (List[List[Matrix]]): The extracted patterns.

        Returns:
            str: A failure report describing the dimension mismatch.
        """
        original_dims = (len(original_grid.matrix), len(original_grid.matrix[0]))
        mismatch_report = f"Dimension mismatch detected:\n"
        mismatch_report += f"Original grid dimensions: {original_dims}\n"
        mismatch_report += "Extracted pattern dimensions:\n"
        for i, pattern_list in enumerate(extracted_patterns):
            for j, pattern in enumerate(pattern_list):
                pattern_dims = (len(pattern.matrix), len(pattern.matrix[0]))
                if pattern_dims != original_dims:
                    mismatch_report += f"Pattern {i+1}.{j+1}: {pattern_dims}\n"
        mismatch_report += "All extracted patterns must have the same dimensions as the original grid."
        return mismatch_report

    def generate_pattern_not_present_report(self, original_grid: Matrix, extracted_patterns: List[List[Matrix]], pattern_descriptions: List[PatternDetails]) -> str:
        """
        Generate a report for patterns not present in the original grid.

        Args:
            original_grid (Matrix): The original grid.
            extracted_patterns (List[List[Matrix]]): The extracted patterns.
            pattern_descriptions (List[PatternDetails]): The pattern descriptions.

        Returns:
            str: A failure report describing patterns not present in the original grid.
        """
        report = "One or more extracted patterns are not present in the original grid:\n\n"
        report += f"Original grid:\n{json.dumps(original_grid.matrix, indent=2)}\n\n"
        for i, (pattern_list, description) in enumerate(zip(extracted_patterns, pattern_descriptions)):
            for j, pattern in enumerate(pattern_list):
                if not self._is_pattern_in_grid(pattern, original_grid):
                    report += f"Pattern {i+1}.{j+1}:\n"
                    report += f"Description: {json.dumps(description.__dict__, indent=2)}\n"
                    report += f"Extracted pattern:\n{json.dumps(pattern.matrix, indent=2)}\n\n"
        report += "Please review the pattern extraction process to ensure all extracted patterns are subsets of the original grid."
        return report

    def generate_overlap_report(self, original_grid: Matrix, pattern_descriptions: List[PatternDetails], overlaps: List[Tuple[int, int, List[int]]]) -> str:
        """
        Generate a report for overlapping patterns.

        Args:
            original_grid (Matrix): The original grid.
            pattern_descriptions (List[PatternDetails]): The pattern descriptions.
            overlaps (List[Tuple[int, int, List[int]]]): List of overlapping cells with their pattern IDs.

        Returns:
            str: A failure report describing overlaps.
        """
        report = "Overlapping patterns detected:\n\n"
        report += f"Original grid:\n{json.dumps(original_grid.matrix, indent=2)}\n\n"
        report += "Overlapping patterns:\n"
        for i, j, pattern_ids in overlaps:
            report += f"Cell ({i}, {j}) is covered by multiple patterns:\n"
            for pattern_id in pattern_ids:
                report += f"Pattern {pattern_id + 1}: {json.dumps(pattern_descriptions[pattern_id].__dict__, indent=2)}\n"
            report += "\n"
        report += "Please refine the pattern extraction to ensure no overlapping patterns (each cell should belong to only one pattern)."
        return report

    def generate_completeness_report(self, original_grid: Matrix, incomplete_cells: List[Tuple[int, int]]) -> str:
        """
        Generate a report for incomplete coverage.

        Args:
            original_grid (Matrix): The original grid.
            incomplete_cells (List[Tuple[int, int]]): List of cells not covered by any pattern.

        Returns:
            str: A failure report describing incomplete coverage.
        """
        report = "Incomplete coverage detected:\n\n"
        report += f"Original grid:\n{json.dumps(original_grid.matrix, indent=2)}\n\n"
        report += "Incomplete coverage:\n"
        report += f"The following cells are not covered by any pattern: {incomplete_cells}\n\n"
        report += "Please refine the pattern extraction to ensure complete coverage (every cell in the original grid should be part of a pattern)."
        return report

    def _is_pattern_in_grid(self, pattern: Matrix, grid: Matrix) -> bool:
        """
        Check if a single pattern is present in the grid.

        Args:
            pattern (Matrix): The pattern to check.
            grid (Matrix): The original grid.

        Returns:
            bool: True if the pattern is present, False otherwise.
        """
        for i in range(len(grid.matrix)):
            for j in range(len(grid.matrix[0])):
                if pattern.matrix[i][j] is not None and pattern.matrix[i][j] != grid.matrix[i][j]:
                    return False
        return True
    
    