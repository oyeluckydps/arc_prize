from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict

from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair


class TrainingSetDescription(BaseModel):
    """
    Describes the training set used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the training set")
    example: List[InputOutputPair] = Field(..., description="Example of a training set")

    def __str__(self) -> str:
        return f"""TrainingSetDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
training_set_description_obj = TrainingSetDescription(
    explanation="""To solve a given challenge, the challenger provides multiple training input-output pairs of grids/matrices in a training set. 
    These pairs in the training set act as examples to learn the causation relation that would turn the input grid into the output grid. 
    Generally, 2-10 input output pairs are provided in the training grid. 
    It will be the job of the solver to understand the transformation taking place on the input matrix/grid that leads to the corresponding output matrix/grid. 
    It is expected that the solver would later apply the same transformation on input matrix of the test set to generate the corresponding output grid/matrix.""",
    example=[
            InputOutputPair(
                input=Matrix(matrix=[
                    [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                    [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                    [3, 2, 2, 3, 3, 3, 3, 8, 3, 3, 3, 3],
                    [3, 2, 2, 3, 3, 3, 3, 8, 3, 3, 3, 3],
                    [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                    [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
                    [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0]
                ]),
                output=Matrix(matrix=[[6]])
            ),
            InputOutputPair(
                input=Matrix(matrix=[
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0],
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0],
                    [3, 3, 3, 4, 4, 3, 3, 3, 8, 3, 3],
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0],
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0],
                    [6, 6, 6, 6, 6, 6, 6, 6, 8, 6, 6],
                    [6, 6, 6, 6, 6, 6, 6, 6, 8, 6, 6],
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0],
                    [0, 0, 0, 4, 4, 0, 0, 0, 8, 0, 0]
                ]),
                output=Matrix(matrix=[[8]])
            ),
            InputOutputPair(
                input=Matrix(matrix=[
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0],
                    [1, 2, 2, 1, 6, 1, 1, 8, 8, 1, 1],
                    [1, 2, 2, 1, 6, 1, 1, 8, 8, 1, 1],
                    [1, 2, 2, 1, 6, 1, 1, 8, 8, 1, 1],
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0],
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0],
                    [4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 6, 4, 4, 4, 4, 4, 4],
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0],
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0],
                    [0, 2, 2, 0, 6, 0, 0, 8, 8, 0, 0]
                ]),
                output=Matrix(matrix=[[6]])
            ),
            InputOutputPair(
                input=Matrix(matrix=[
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0],
                    [2, 2, 2, 2, 3, 3, 2, 2, 5, 2, 2, 2],
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0],
                    [4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4],
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0],
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0],
                    [0, 0, 0, 0, 3, 3, 0, 0, 5, 0, 0, 0]
                ]),
                output=Matrix(matrix=[[1]])
            ),
            InputOutputPair(
                input=Matrix(matrix=[
                    [0, 1, 0],
                    [3, 3, 3],
                    [0, 1, 0]
                ]),
                output=Matrix(matrix=[[3]])
            )
        ]
)

