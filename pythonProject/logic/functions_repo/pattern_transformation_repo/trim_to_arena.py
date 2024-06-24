"""
This module contains the function trim_to_arena which trims cells outside the arena from a given pattern.
"""

from typing import Optional
from ...object_type.pattern import Pattern
from ...object_type.cell import Cell
from ..pattern_transformation import patternTransformation

def trim_to_arena(pattern: Pattern, width: Optional[int] = None, height: Optional[int] = None) -> Pattern:
    """
    Trims cells outside the arena from the given pattern.

    Args:
        pattern (Pattern): The pattern to be trimmed.
        width (Optional[int]): The width of the arena. If not provided, it will be imported from ENV_PARAMS.
        height (Optional[int]): The height of the arena. If not provided, it will be imported from ENV_PARAMS.

    Returns:
        Pattern: The trimmed pattern.
    """
    if width is None or height is None:
        from ....logic.env_params import ArenaParams as arena
        width = width or arena.width
        height = height or arena.height

    trimmed_cells = [cell for cell in pattern.cells if 0 <= cell.x < width and 0 <= cell.y < height]
    return Pattern(trimmed_cells)

fun_obj = patternTransformation(trim_to_arena, 
                        description= "Trims cells outside the arena from the given pattern.")
