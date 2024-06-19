from .pattern import Pattern

class Group:
    def __init__(self, patterns, probability=0.0):
        self.patterns = set(patterns)
        self.probability = probability

    def __repr__(self):
        return f"Group(patterns={list(self.patterns)}, probability={self.probability})"

    def get_properties(self):
        return {
            "pattern_count": len(self.patterns)
        }

    def to_supergroup(self):
        return SuperGroup([self], self.probability)

    def reduce(self):
        if len(self.patterns) == 1:
            pattern = next(iter(self.patterns))
            return pattern.reduce()
        return self

