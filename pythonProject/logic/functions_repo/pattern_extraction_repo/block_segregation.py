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

    if mould is None:
        from ..cell_expansion_repo.expand_to_nearest_8 import fun_obj as expand_to_nearest_8
        from ..pattern_transformation_repo.trim_to_arena import fun_obj as trim_to_arena
        mould = expand_to_nearest_8
    
    expand_and_trim = lambda cell: trim_to_arena.method(expand_to_nearest_8.method(cell), height = None, width = None)
    compose_fun_obj = cellExpansion(expand_and_trim, 
                                    description= "Returns a Pattern composed of the nearest 8 cells to the given cell avoiding the borders of the arena.")

    while unexplored_cells:
        to_explore = [unexplored_cells.pop()]
        explored_cells = set()

        while to_explore:
            current_cell = to_explore.pop()
            explored_cells.add(current_cell)

            neighbours = compose_fun_obj.method(current_cell)

            for neighbour in neighbours:
                # This step is a workaround till we have programmed all the abstraction functions. Ideally, we would
                # like to turn a cell into an abstraction such that it matches any other cell's location without taking
                # into account the color.
                for cell in unexplored_cells:
                    if (neighbour.x, neighbour.y) == (cell.x, cell.y):
                        unexplored_cells.remove(cell)
                        to_explore.append(cell)

        explored_patterns.append(Pattern(explored_cells))

    return explored_patterns
