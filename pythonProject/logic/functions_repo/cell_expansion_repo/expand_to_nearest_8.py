"""
This module contains the function expand_to_nearest_8 which returns a Pattern
composed of the nearest 8 cells to the given cell.
"""

from typing import List
from ...object_type.cell import Cell
from ...object_type.pattern import Pattern
from ..cell_expansion import cellExpansion

def expand_to_nearest_8(cell: Cell) -> Pattern:
    """
    Returns a Pattern composed of the nearest 8 cells to the given cell.

    Args:
        cell (Cell): The cell for which to find the nearest 8 neighbors.

    Returns:
        Pattern: A pattern composed of the nearest 8 cells to the given cell.
    """
    x = cell.x
    y = cell.y
    color = cell.color
    neighbors = [
        (x-1, y-1), (x-1, y), (x-1, y+1),
        (x, y-1),           (x, y+1),
        (x+1, y-1), (x+1, y), (x+1, y+1)
    ]
    # Create a pattern with the nearest 8 neighbors
    return Pattern([Cell(i, j, color) for i, j in neighbors])

fun_obj = cellExpansion(expand_to_nearest_8, 
                        description= "Returns a Pattern composed of the nearest 8 cells to the given cell.")
