import os
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Iterator
from pattern_description_signature import PatternDetails, Matrix
import dspy

# Define the Pydantic model for the output result (which can be a single matrix or a list of matrices)
class CollectionOfMatrices(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    result: Union[Matrix, List[Matrix]] = Field(description="The output matrix/matrices, either a single matrix or multiple matrices")
    
    def __iter__(self) -> Iterator[Matrix]:
        if isinstance(self.result, list):
            for matrix in self.result:
                yield matrix
        else:
            yield self.result

class PatternExtractionSignature(dspy.Signature):
    query: str = dspy.InputField()
    pattern_description: PatternDetails = dspy.InputField()
    matrix: Matrix = dspy.InputField()
    output_pattern: CollectionOfMatrices = dspy.OutputField()
    
    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        Given the following pattern description in JSON format:
        Your task is to identify this pattern in the provided matrix. Extract the pattern from the matrix, preserving its digits and positions. Replace all other entries that are not a part of the pattern in the matrix with None.
        Present your result as a list of lists like this:
        [
        [0, None, None, 0],
        [None, 0, 0, None],
        [0, None, None, 0]
        ]
        Please process this matrix and output the result showing only the identified pattern.
        If there are multiple patterns to be found in the matrix that satisfy the description for the pattern then output all of these matrices as a list of matrices.
        """
        return prompt

