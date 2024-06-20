"""
This module contains the function block_segregation which segregates blocks of cells
from a given pattern using a pattern mould.
"""

from typing import List, Optional
from ...object_type.pattern import Pattern
from ...object_type.cell import Cell
from ..cell_expansion import cellExpansion

def block_segregation(pattern: Pattern, mould: Optional[cellExpansion] = None) -> List[Pattern]:
    """
    Segregates blocks of cells from the given pattern using the provided pattern mould.

    Args:
        pattern (Pattern): The pattern from which to segregate blocks.
        mould (Optional[cellExpansion]): The pattern mould to use for determining neighboring cells.

    Returns:
        List[Pattern]: A list of segregated patterns.
    """
    unexplored_cells = set(pattern.cells)
    explored_patterns = []

    def nearest_8_neighbors(cell: Cell) -> Pattern:
        x = cell.x
        y = cell.y
        color = cell.color
        neighbors = [
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1),           (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)
        ]
        # Filter out neighbors that are out of bounds
        return Pattern([Cell(i, j, color) for i, j in neighbors])

    if mould is None:
        from ..cell_expansion_repo.expand_to_nearest_8 import expand_to_nearest_8
        mould = expand_to_nearest_8()

    while unexplored_cells:
        to_explore = [unexplored_cells.pop()]
        explored_cells = set()

        while to_explore:
            current_cell = to_explore.pop()
            explored_cells.add(current_cell)

            if mould:
                neighbours = mould.method(current_cell)
            else:
                neighbours = [Cell(current_cell.x + dx, current_cell.y + dy, current_cell.color)
                              for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for neighbour in neighbours:
                if neighbour in unexplored_cells:
                    unexplored_cells.remove(neighbour)
                    to_explore.append(neighbour)

        explored_patterns.append(Pattern(explored_cells))

    return explored_patterns
