from typing import List, Tuple
from .pattern_description_signature import Matrix
import json
from preprocess_sample_json import pp

class FailureReportGenerator:
    """A class for generating failure reports for pattern extraction validation."""

    def generate_dimension_mismatch_report(self, original_grid: Matrix, extracted_patterns: List[Matrix]) -> str:
        """Generate a report for dimension mismatch."""
        original_dims = (len(original_grid.matrix), len(original_grid.matrix[0]))
        mismatch_report = f"Dimension mismatch detected:\n"
        mismatch_report += f"Original grid dimensions: {original_dims}\n"
        mismatch_report += "Extracted pattern dimensions:\n"
        for i, pattern in enumerate(extracted_patterns):
            pattern_dims = (len(pattern.matrix), len(pattern.matrix[0]))
            if pattern_dims != original_dims:
                mismatch_report += f"Pattern {i+1}: {pattern_dims}\n"
        mismatch_report += "All extracted patterns must have the same dimensions as the original grid."
        return mismatch_report

    def generate_pattern_not_present_report(self, original_grid: Matrix, extracted_patterns: List[Matrix]) -> str:
        """Generate a report for patterns not present in the original grid."""
        report = "One or more extracted patterns are not present in the original grid:\n\n"
        report += f"Original grid:\n{original_grid.matrix}\n\n"
        for i, pattern in enumerate(extracted_patterns):
            if not self._is_pattern_in_grid(pattern, original_grid):
                report += f"Pattern {i+1}:\n"
                report += f"Extracted pattern:\n{pattern.matrix}\n\n"
        report += "Please review the pattern extraction process to ensure all extracted patterns are subsets of the original grid."
        return report

    def generate_overlap_report(self, original_grid: Matrix, extracted_patterns: List[Matrix], overlaps: List[Tuple[int, int, List[int]]]) -> str:
        """Generate a report for overlapping patterns."""
        report = "Overlapping patterns detected:\n\n"
        report += f"Original grid:\n{json.dumps(original_grid.matrix, indent=2)}\n\n"
        report += "Extracted patterns:\n"
        for i, pattern in enumerate(extracted_patterns):
            report += f"Pattern {i}:\n{json.dumps(pattern.matrix, indent=2)}\n\n"
        report += "Overlapping patterns:\n"
        for i, j, pattern_ids in overlaps:
            report += f"Cell ({i}, {j}) is covered by multiple patterns: {pattern_ids}\n"
        report += "\nPlease refine the pattern extraction to ensure no overlapping patterns (each cell should belong to only one pattern)."
        return report

    def generate_completeness_report(self, original_grid: Matrix, uncovered_cells: List[Tuple[int, int]]) -> str:
        """Generate a report for incomplete coverage."""
        report = "Incomplete coverage detected:\n\n"
        report += f"Original grid:\n{json.dumps(original_grid.matrix, indent=2)}\n\n"
        report += "Uncovered cells:\n"
        for i, j in uncovered_cells:
            report += f"Cell ({i}, {j}) is not covered by any pattern\n"
        report += "\nPlease refine the pattern extraction to ensure complete coverage of the original grid."
        return report

    def _is_pattern_in_grid(self, pattern: Matrix, grid: Matrix) -> bool:
        """Check if a single pattern is present in the grid."""
        return all(
            pattern.matrix[i][j] is None or pattern.matrix[i][j] == grid.matrix[i][j]
            for i in range(len(grid.matrix))
            for j in range(len(grid.matrix[0]))
        )
    
