class Cell:
    def __init__(self, x, y, color, probability=0.0):
        self.x = x
        self.y = y
        self.color = color
        self.probability = probability
        self.properties = [self.get_x, self.get_y, self.get_color]

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, color={self.color}, probability={self.probability})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def to_pattern(self):
        return Pattern([self], self.probability)

    def get_properties(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color
        }