from typing import List, Tuple
from .signatures.pattern_description_signature import Matrix
from preprocess_sample_json import pp

class FailureReportGenerator:
    """A class for generating failure reports for pattern extraction validation."""

    def generate_dimension_mismatch_report(self, original_grid: Matrix, extracted_patterns: List[Matrix]) -> str:
        """Generate a report for dimension mismatch, including passing patterns."""
        original_dims = (len(original_grid.matrix), len(original_grid.matrix[0]))
        report = f"Dimension check report:\n\n"
        report += f"Original grid dimensions: {original_dims}\n\n"
        
        passing_patterns = []
        failing_patterns = []
        
        for i, pattern in enumerate(extracted_patterns):
            pattern_dims = (len(pattern.matrix), len(pattern.matrix[0]))
            if pattern_dims == original_dims:
                passing_patterns.append((i, pattern))
            else:
                failing_patterns.append((i, pattern_dims))
        
        if failing_patterns:
            report += \
            """
            FAIL: Dimension mismatch detected for the following patterns.
            The dimensions of the matrix on which pattern was extracted does not match the dimensions of the original grid.
            Rectify this error by first finding the correct pattern that asheres to the pattern description and then extracting the pattern
            from the original grid by keeping its digits, positions, and shape intact. 
            Of course make sure that the matrix use to report the extracted pattern has the same dimensions as the original grid.
            """
            for i, dims in failing_patterns:
                report += f"Pattern {i+1}: {dims}\n"
            report += "\nAll extracted patterns must have the same dimensions as the original grid.\n\n"
        
        if passing_patterns:
            report += "PASS: The following patterns have correct dimensions:\n"
        for i, pattern in passing_patterns:
            report += f"Pattern {i+1}:\n{pp.pformat(pattern.matrix)}\n\n"
        
        report += "\nPlease recheck the passing patterns and only modify them if they are redundant or if there is a very good reason to assume they do not belong in the list of extracted patterns."
        return report

    def generate_pattern_not_present_report(self, original_grid: Matrix, extracted_patterns: List[Matrix]) -> str:
        """Generate a report for patterns not present in the original grid, including passing patterns."""
        report = "Pattern presence check report:\n\n"
        report += f"Original grid:\n{pp.pformat(original_grid.matrix)}\n\n"
        report += \
"""
The following mentioned extracted patterns are not present in the original grid.
This can happend due to the following sources of error:
1. The extracted shape is found in the original grid but the digit is different. 
        For example during the extraction some digits of the pattern were changed leading to errors.
        You can rectify this type of error by changing the digit of the pattern to the digit found in the original grid.
2. The extracted shape is located in the original grid but the position is different. 
        For example during the extraction the shape was shifted to a different position.
        You can rectify this type of error by shifting the pattern to the position found in the original grid.
3. The extracted pattern has a different shape than in the original grid.
        For example during the extraction some dimension or aspect of the shape was changed leading to errors.
        e.g. A rectangle of 2*3 cells was extracted but the original grid has a square of 3*3 cells.
        You can rectify this error by first correctly identifying the shape corresponding to the extracted pattern in the original grid
        and then extracting the correct pattern with correct shape from the original grid.
4. The extracted pattern is not found in the original grid
        This is highly unlikely to happen but in some cases it might happen that the pattern was extracted incorrectly and is not present in the original grid.
        In this case you can rectify this error by extracting only the patterns that adhere to the description of the pattern.
        Do not extract patterns that are not present in the original grid.
5. It is also possible that the reason for the pattern not being found in the original grid is not mentioned above.
        In this case use your best judgement to determine the reason for the pattern not being found in the original grid 
        given the original grid and the pattern description and try to rectify the error by extracting the correct pattern adhering to the description.
"""
        
        passing_patterns = []
        failing_patterns = []
        
        for i, pattern in enumerate(extracted_patterns):
            if self._is_pattern_in_grid(pattern, original_grid):
                passing_patterns.append((i, pattern))
            else:
                failing_patterns.append((i, pattern))
        
        if failing_patterns:
            report += "FAIL: The following extracted patterns are not present in the original grid:\n"
            for i, pattern in failing_patterns:
                report += f"Pattern {i+1}:\n{pp.pformat(pattern.matrix)}\n\n"
        
        if passing_patterns:
            report += "PASS: The following patterns are present in the original grid:\n"
        for i, pattern in passing_patterns:
            report += f"Pattern {i+1}:\n{pp.pformat(pattern.matrix)}\n\n"
        
        report += "\nPlease recheck the passing patterns and only modify them if they are redundant or if there is a very good reason to assume they do not belong in the list of extracted patterns."
        report += """ \n\n
        Based on the above mentioned failing patterns and the possible reasons for the failure please rectify the error and generate a new set of patterns
        adhering to the description of the pattern. Follow the instructed given below to generate the new set of patterns. Accoutn for the failures and PASSing
        cases mentioned above while generating the new set of patterns following the instructions below.
        """
        return report

    def generate_overlap_report(self, original_grid: Matrix, extracted_patterns: List[Matrix], overlaps: List[Tuple[int, int, List[int]]]) -> str:
        """Generate a report for overlapping patterns, including non-overlapping patterns."""
        report = "Overlap check report:\n\n"
        report += f"Original grid:\n{pp.pformat(original_grid.matrix)}\n\n"
        
        overlapping_patterns = set()
        for _, _, pattern_ids in overlaps:
            overlapping_patterns.update(pattern_ids)
        
        non_overlapping_patterns = set(range(len(extracted_patterns))) - overlapping_patterns
        
        if overlaps:
            report += "FAIL: Overlapping patterns detected:\n"
            for i, j, pattern_ids in overlaps:
                report += f"Cell ({i}, {j}) is covered by multiple patterns: {pattern_ids}\n"
            report += "\nPlease refine the pattern extraction to ensure no overlapping patterns (each cell should belong to only one pattern).\n\n"
        
        if non_overlapping_patterns:
            report += "PASS: The following patterns do not overlap with any other patterns:\n"
        for i in non_overlapping_patterns:
            report += f"Pattern {i}:\n{pp.pformat(extracted_patterns[i].matrix)}\n\n"
        
        report += "\nPlease recheck the non-overlapping patterns and only modify them if they are redundant or if there is a very good reason to assume they do not belong in the list of extracted patterns."
        return report

    def generate_completeness_report(self, original_grid: Matrix, uncovered_cells: List[Tuple[int, int]], extracted_patterns: List[Matrix]) -> str:
        """Generate a report for incomplete coverage, including patterns that contribute to coverage."""
        report = "Coverage check report:\n\n"
        report += f"Original grid:\n{pp.pformat(original_grid.matrix)}\n\n"
        
        if uncovered_cells:
            report += "FAIL: Incomplete coverage detected:\n"
            for i, j in uncovered_cells:
                report += f"Cell ({i}, {j}) is not covered by any pattern\n"
            report += "\nPlease refine the pattern extraction to ensure complete coverage of the original grid.\n\n"
        
        if extracted_patterns:
            report += "PASS: The following patterns contribute to the grid coverage:\n"
        for i, pattern in enumerate(extracted_patterns):
            if any(pattern.matrix[i][j] is not None for i in range(len(pattern.matrix)) for j in range(len(pattern.matrix[0]))):
                report += f"Pattern {i}:\n{pp.pformat(pattern.matrix)}\n\n"
        
        report += "\nPlease recheck the patterns contributing to coverage and only modify them if they are redundant or if there is a very good reason to assume they do not belong in the list of extracted patterns."
        return report

    def _is_pattern_in_grid(self, pattern: Matrix, grid: Matrix) -> bool:
        """Check if a single pattern is present in the grid."""
        return all(
            pattern.matrix[i][j] is None or pattern.matrix[i][j] == grid.matrix[i][j]
            for i in range(len(grid.matrix))
            for j in range(len(grid.matrix[0]))
        )
    
