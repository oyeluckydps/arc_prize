from .group import Group

class SuperGroup:
    def __init__(self, groups, probability=0.0):
        self.groups = set(groups)
        self.probability = probability

    def __repr__(self):
        return f"SuperGroup(groups={list(self.groups)}, probability={self.probability})"

    def get_properties(self):
        return {
            "group_count": len(self.groups)
        }

    def to_constellation(self):
        return Constellation([self], self.probability)

    def reduce(self):
        if len(self.groups) == 1:
            group = next(iter(self.groups))
            return group.reduce()
        return self

