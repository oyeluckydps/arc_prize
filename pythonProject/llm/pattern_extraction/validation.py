from typing import List, Tuple
from .pattern_description_signature import Matrix, PatternDetails
from .failure_reports import FailureReportGenerator

class Validator:
    """
    A class for validating pattern extractions from grids.
    """

    def __init__(self):
        self.report_generator = FailureReportGenerator()

    def validate_decomposition(self, original_grid: Matrix, extracted_patterns: List[List[Matrix]], pattern_descriptions: List[PatternDetails]) -> List[str]:
        """
        Validate the decomposition of a grid into patterns.

        Args:
            original_grid (Matrix): The original grid to be decomposed.
            extracted_patterns (List[List[Matrix]]): A list where each entry corresponds to a pattern description and contains one or more extracted matrices.
            pattern_descriptions (List[PatternDetails]): A list of pattern descriptions.

        Returns:
            List[str]: A list of failure reports, if any.
        """
        failure_reports = []

        # Check if all extracted patterns have the same dimensions as the original grid
        if not self._check_dimensions(original_grid, extracted_patterns):
            return [self.report_generator.generate_dimension_mismatch_report(original_grid, extracted_patterns)]

        # Check if patterns are present in the original grid
        if not self._are_patterns_in_grid(extracted_patterns, original_grid):
            return [self.report_generator.generate_pattern_not_present_report(original_grid, extracted_patterns, pattern_descriptions)]

        # Calculate the check grid
        check_grid = self._calculate_check_grid(original_grid, extracted_patterns)

        # Check for overlaps
        overlaps = self._check_overlaps(check_grid)
        if overlaps:
            failure_reports.append(self.report_generator.generate_overlap_report(original_grid, pattern_descriptions, overlaps))

        # Check for completeness
        incomplete_cells = self._check_completeness(check_grid)
        if incomplete_cells:
            failure_reports.append(self.report_generator.generate_completeness_report(original_grid, incomplete_cells))

        return failure_reports

    def _check_dimensions(self, original_grid: Matrix, extracted_patterns: List[List[Matrix]]) -> bool:
        """
        Check if all extracted patterns have the same dimensions as the original grid.

        Args:
            original_grid (Matrix): The original grid.
            extracted_patterns (List[List[Matrix]]): The extracted patterns.

        Returns:
            bool: True if all dimensions match, False otherwise.
        """
        original_dims = (len(original_grid.matrix), len(original_grid.matrix[0]))
        return all(
            (len(pattern.matrix), len(pattern.matrix[0])) == original_dims
            for pattern_list in extracted_patterns
            for pattern in pattern_list
        )

    def _are_patterns_in_grid(self, patterns: List[List[Matrix]], grid: Matrix) -> bool:
        """
        Check if all extracted patterns are present in the original grid.

        Args:
            patterns (List[List[Matrix]]): The extracted patterns.
            grid (Matrix): The original grid.

        Returns:
            bool: True if all patterns are present, False otherwise.
        """
        return all(
            self._is_pattern_in_grid(pattern, grid)
            for pattern_list in patterns
            for pattern in pattern_list
        )

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

    def _calculate_check_grid(self, original_grid: Matrix, extracted_patterns: List[List[Matrix]]) -> List[List[List[int]]]:
        """
        Calculate the check grid for overlap and completeness checks.

        Args:
            original_grid (Matrix): The original grid.
            extracted_patterns (List[List[Matrix]]): The extracted patterns.

        Returns:
            List[List[List[int]]]: The check grid with pattern IDs for each cell.
        """
        check_grid = [[[] for _ in range(len(original_grid.matrix[0]))] for _ in range(len(original_grid.matrix))]

        for pattern_id, pattern_list in enumerate(extracted_patterns):
            for pattern in pattern_list:
                for i in range(len(pattern.matrix)):
                    for j in range(len(pattern.matrix[0])):
                        if pattern.matrix[i][j] is not None:
                            check_grid[i][j].append(pattern_id)

        return check_grid

    def _check_overlaps(self, check_grid: List[List[List[int]]]) -> List[Tuple[int, int, List[int]]]:
        """
        Check for overlapping patterns in the extracted patterns.

        Args:
            check_grid (List[List[List[int]]]): The check grid with pattern IDs for each cell.

        Returns:
            List[Tuple[int, int, List[int]]]: List of overlapping cells with their pattern IDs.
        """
        return [(i, j, cell) for i, row in enumerate(check_grid) for j, cell in enumerate(row) if len(cell) > 1]

    def _check_completeness(self, check_grid: List[List[List[int]]]) -> List[Tuple[int, int]]:
        """
        Check for completeness of coverage in the extracted patterns.

        Args:
            check_grid (List[List[List[int]]]): The check grid with pattern IDs for each cell.

        Returns:
            List[Tuple[int, int]]: List of cells not covered by any pattern.
        """
        return [(i, j) for i, row in enumerate(check_grid) for j, cell in enumerate(row) if not cell]
    
    