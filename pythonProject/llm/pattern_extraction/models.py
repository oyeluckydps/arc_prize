from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field, ConfigDict
from .pattern_description_signature import Matrix

@dataclass
class PatternNode:
    pattern: Matrix
    description: Dict[str, Any]
    children: List['PatternNode'] = None

class PatternTree:
    def __init__(self, grid: Matrix):
        self.root = PatternNode(grid, {"description": "Original Grid"})

class SchemaOfDecomposition:
    def __init__(self):
        self.root = PatternNode(Matrix(matrix=[]), {"description": "Schema Root"})

        