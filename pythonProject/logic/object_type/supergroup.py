from .constellation import Constellation

class SuperGroup:
    def __init__(self, groups, probability=0.0):
        self.groups = set(groups)
        self.probability = probability
        self.properties = [self.get_group_count]

    def __repr__(self):
        return f"SuperGroup(groups={list(self.groups)}, probability={self.probability})"

    def get_group_count(self):
        return len(self.groups)

    def to_higher_order(self):
        return Constellation([self], self.probability)

    def reduce(self):
        if len(self.groups) == 1:
            group = next(iter(self.groups))
            return group.reduce()
        return self


