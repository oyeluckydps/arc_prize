"""
This module contains the function chromatic_segregation which extracts patterns
from a grid based on the specified color or all colors from 0 to 9.
"""

from typing import List, Optional
from ...object_type.grid import Grid
from ...object_type.pattern import Pattern

def chromatic_segregation(grid: Grid, color: Optional[int] = None) -> List[Pattern]:
    """
    Extracts patterns from the grid based on the specified color or all colors from 0 to 9.

    Args:
        grid (Grid): The grid from which to extract patterns.
        color (Optional[int]): The color to filter cells by. If None, patterns for all colors from 0 to 9 are extracted.

    Returns:
        List[Pattern]: A list of patterns extracted from the grid.
    """
    patterns = []
    if color is not None:
        cells = [cell for cell in grid.cells if cell.color == color]
        patterns.append(Pattern(cells))
    else:
        for col in range(10):
            cells = [cell for cell in grid.cells if cell.color == col]
            patterns.append(Pattern(cells))
    return patterns