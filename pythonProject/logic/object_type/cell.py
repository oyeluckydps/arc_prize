from .pattern import Pattern

class Cell:
    def __init__(self, x, y, color, probability=0.0):
        self.x = x
        self.y = y
        self.color = color
        self.probability = probability
        self.properties = [self.get_x, self.get_y, self.get_color]

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, color={self.color}, probability={self.probability})"

    def to_pattern(self):
        return Pattern([self], self.probability)

