from pydantic import BaseModel, Field, ConfigDict
from typing import Dict

from custom_types.matrix import Matrix


class InputOutputPairDescription(BaseModel):
    """
    Describes an input-output pair used in the ARC challenge.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    explanation: str = Field(..., description="Explanation of the input-output pair")
    example: Dict[str, Matrix] = Field(..., description="Example of an input-output pair")

    def __str__(self) -> str:
        return f"""InputOutputPairDescription:
Explanation: {self.explanation}
Example: {self.example}"""

# Sample object
input_output_pair_description_obj = InputOutputPairDescription(
    explanation="""An input-output pair consists of two matrices: an input matrix and its corresponding output matrix. 
    These pairs are used in the training set to demonstrate the transformation rule that needs to be learned and applied to solve the puzzle. 
    It is the job of the solver to identify the underlying causation or the transformations taking place on the pair. 
    Later, the solver is expected to apply the same causation/transformation learnt from these input-output pairs and 
    apply them on input matrix of test set to form the corresponding output matrix. 
    An input-output pair may be formed by the solver after it has solved the test set too. 
    This input output pair is generally the output from the challenge for a given puzzle.""",
    example={
        "input": Matrix(matrix=[
            [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
            [3, 2, 2, 3, 3, 3, 3, 8, 3, 3, 3, 3],
            [3, 2, 2, 3, 3, 3, 3, 8, 3, 3, 3, 3],
            [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 2, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0]
        ]),
        "output": Matrix(matrix=[[6]])
    }
)