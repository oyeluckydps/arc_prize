from typing import List, Tuple, Optional
from .signatures.pattern_description_signature import Matrix
from .failure_reports import FailureReportGenerator

def validate_patterns(original_grid: Matrix, extracted_patterns: List[Matrix]) -> Optional[str]:
    """
    Validate the extracted patterns against the original grid.

    Args:
        original_grid (Matrix): The original grid.
        extracted_patterns (List[Matrix]): The extracted patterns.

    Returns:
        Optional[str]: Failure report if any, None otherwise.
    """
    report_generator = FailureReportGenerator()

    # Check dimensions
    if not _check_dimensions(original_grid, extracted_patterns):
        return report_generator.generate_dimension_mismatch_report(original_grid, extracted_patterns)

    # Check if patterns are present in the grid
    if not _are_patterns_in_grid(extracted_patterns, original_grid):
        return report_generator.generate_pattern_not_present_report(original_grid, extracted_patterns)

    # Check for overlaps
    check_grid = _calculate_check_grid(original_grid, extracted_patterns)
    overlaps = _check_overlaps(check_grid)
    if overlaps:
        return report_generator.generate_overlap_report(original_grid, extracted_patterns, overlaps)

    return None

def _check_dimensions(original_grid: Matrix, extracted_patterns: List[Matrix]) -> bool:
    """Check if all extracted patterns have the same dimensions as the original grid."""
    original_dims = (len(original_grid.matrix), len(original_grid.matrix[0]))
    return all((len(pattern.matrix), len(pattern.matrix[0])) == original_dims for pattern in extracted_patterns)

def _are_patterns_in_grid(patterns: List[Matrix], grid: Matrix) -> bool:
    """Check if all extracted patterns are present in the original grid."""
    return all(_is_pattern_in_grid(pattern, grid) for pattern in patterns)

def _is_pattern_in_grid(pattern: Matrix, grid: Matrix) -> bool:
    """Check if a single pattern is present in the grid."""
    return all(
        pattern.matrix[i][j] is None or pattern.matrix[i][j] == grid.matrix[i][j]
        for i in range(len(grid.matrix))
        for j in range(len(grid.matrix[0]))
    )

def _calculate_check_grid(original_grid: Matrix, extracted_patterns: List[Matrix]) -> List[List[List[int]]]:
    """Calculate the check grid for overlap checks."""
    check_grid = [[[] for _ in range(len(original_grid.matrix[0]))] for _ in range(len(original_grid.matrix))]
    for pattern_id, pattern in enumerate(extracted_patterns):
        for i in range(len(pattern.matrix)):
            for j in range(len(pattern.matrix[0])):
                if pattern.matrix[i][j] is not None:
                    check_grid[i][j].append(pattern_id)
    return check_grid

def _check_overlaps(check_grid: List[List[List[int]]]) -> List[Tuple[int, int, List[int]]]:
    """Check for overlapping patterns in the extracted patterns."""
    return [(i, j, cell) for i, row in enumerate(check_grid) for j, cell in enumerate(row) if len(cell) > 1]

def check_completeness(original_grid: Matrix, extracted_patterns: List[Matrix]) -> List[Tuple[int, int]]:
    """Check if all cells in the original grid are covered by the extracted patterns."""
    covered_grid = [[False for _ in range(len(original_grid.matrix[0]))] for _ in range(len(original_grid.matrix))]
    
    for pattern in extracted_patterns:
        for i in range(len(pattern.matrix)):
            for j in range(len(pattern.matrix[0])):
                if pattern.matrix[i][j] is not None:
                    covered_grid[i][j] = True
    
    uncovered_cells = [(i, j) for i in range(len(covered_grid)) for j in range(len(covered_grid[0])) if not covered_grid[i][j]]
    return uncovered_cells