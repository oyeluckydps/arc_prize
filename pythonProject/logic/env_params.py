from .object_type.grid import Grid
class ArenaParams:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.height, self.width = grid.get_dimensions()

ARENA_PARAMS = None

def init_ARENA_PARAMS(grid: Grid):
    global ARENA_PARAMS
    ARENA_PARAMS = ArenaParams(grid)

    