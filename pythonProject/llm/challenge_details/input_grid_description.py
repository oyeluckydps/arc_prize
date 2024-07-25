from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix

class InputGridDescription(BaseModel):
    """
    Describes an input grid used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the input grid")
    example: Matrix = Field(..., description="Example of an input grid")

    def __str__(self) -> str:
        return f"""InputGridDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
input_grid_description_obj = InputGridDescription(
    explanation="""An input grid is a matrix representing the initial state or problem in the ARC challenge. 
    It is provided as part of an input-output pair in the training set or as a standalone grid in the test set. The input grid is represented as a list of lists, 
     where each inner list represents a row in the grid, and each element in these lists is an integer between 0 and 9, representing different colors. 
     The solver's task is to analyze these input grids, identify patterns, and understand the transformation rules that lead to the corresponding output grids.""",
    example=Matrix(matrix=[
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [1, 1, 1, 3, 3, 1, 1, 1, 1, 7, 1, 1, 1],
        [1, 1, 1, 3, 3, 1, 1, 1, 1, 7, 1, 1, 1],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0, 0, 7, 0, 0, 0]
    ])
)

