from .supergroup import SuperGroup

class Constellation:
    def __init__(self, supergroups, probability=0.0):
        self.supergroups = set(supergroups)
        self.probability = probability

    def __repr__(self):
        return f"Constellation(supergroups={list(self.supergroups)}, probability={self.probability})"

    def get_properties(self):
        return {
            "supergroup_count": len(self.supergroups)
        }

    def reduce(self):
        if len(self.supergroups) == 1:
            supergroup = next(iter(self.supergroups))
            return supergroup.reduce()
        return self

