from .cell import Cell

class Grid:
    def __init__(self, cells, probability=0.0):
        self.cells = set(cells)
        self.probability = probability
        self.properties = [self.get_cell_count]
        self.validate_grid()

    def validate_grid(self):
        max_x = max(cell.x for cell in self.cells)
        max_y = max(cell.y for cell in self.cells)
        positions = {(cell.x, cell.y) for cell in self.cells}

        for i in range(max_x + 1):
            for j in range(max_y + 1):
                if (i, j) not in positions:
                    raise ValueError(f"Missing cell at position ({i}, {j})")
                if sum(1 for cell in self.cells if cell.x == i and cell.y == j) > 1:
                    raise ValueError(f"Multiple cells found at position ({i}, {j})")

    def __repr__(self):
        return f"Grid(cells={list(self.cells)}, probability={self.probability})"

    def get_cell_count(self):
        return len(self.cells)

    def get_properties(self):
        return {
            "cell_count": len(self.cells)
        }