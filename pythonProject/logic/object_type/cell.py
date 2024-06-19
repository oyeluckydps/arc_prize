class Cell:
    def __init__(self, x, y, color, probability=0.0):
        self.x = x
        self.y = y
        self.color = color
        self.probability = probability

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, color={self.color}, probability={self.probability})"

    def get_properties(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color
        }

    def to_pattern(self):
        return Pattern([self], self.probability)


