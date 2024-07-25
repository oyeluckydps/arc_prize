from pydantic import BaseModel, Field, ConfigDict

from custom_types.matrix import Matrix


class OutputGridDescription(BaseModel):
    """
    Describes an output grid used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the output grid")
    example: Matrix = Field(..., description="Example of an output grid")

    def __str__(self) -> str:
        return f"""OutputGridDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
output_grid_description_obj = OutputGridDescription(
    explanation="""An output grid is a matrix representing the desired result or solution in the ARC challenge. 
    In the training set, it is provided alongside its corresponding input grid as part of an input-output pair. 
    The output grid demonstrates the result of applying the transformation rule to the input grid. Like the input grid, 
    it is represented as a list of lists of integers between 0 and 9, each representing a color. 
    In the test set, the solver must generate the output grid based on the learned transformation rules. 
    The output grid can vary in size and complexity, from a single-element matrix to a complex pattern, depending on the specific puzzle and transformation rule.""",
    example=Matrix(matrix=[[6]])
)

