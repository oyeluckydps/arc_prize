from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union

from custom_types.matrix import Matrix


class TestSetDescription(BaseModel):
    """
    Describes the test set used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the test set")
    example: Union[Matrix, List[Matrix]] = Field(..., description="Example of a test set")

    def __str__(self) -> str:
        return f"""TestSetDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
test_set_description_obj = TestSetDescription(
    explanation=\
        """The challenger provides a training and a test set. The input output pair of grids/matrices in the training set creates examples required to solve the puzzle. 
        The test grid has one or two input matrix/grid only. The output grid is not provided and it is the job of the solver to find 
        the output matrix corresponding to the provided input matrix of the training set.""",
    example=\
            Matrix(matrix=[
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

