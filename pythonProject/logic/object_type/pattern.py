from .cell import Cell

class Pattern:
    def __init__(self, cells, probability=0.0):
        self.cells = set(cells)
        self.probability = probability
        self.properties = [self.get_cell_count]

    def __repr__(self):
        return f"Pattern(cells={list(self.cells)}, probability={self.probability})"

    def get_cell_count(self):
        return len(self.cells)

    def to_group(self):
        return Group([self], self.probability)

    def reduce(self):
        if len(self.cells) == 1:
            cell = next(iter(self.cells))
            return Cell(cell.x, cell.y, cell.color, self.probability)
        return self


