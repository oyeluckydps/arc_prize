from .pattern import Pattern
from .supergroup import SuperGroup

class Group:
    def __init__(self, patterns, probability=0.0):
        self.patterns = set(patterns)
        self.probability = probability
        self.properties = [self.get_pattern_count]

    def __repr__(self):
        return f"Group(patterns={list(self.patterns)}, probability={self.probability})"

    def to_higher_order(self):
        return SuperGroup([self], self.probability)

    def reduce(self):
        if len(self.patterns) == 1:
            pattern = next(iter(self.patterns))
            return pattern.reduce()
        return self


    