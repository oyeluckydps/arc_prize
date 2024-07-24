import os
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Iterator

from .pattern_description_signature import PatternDetails, Matrix

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
        Your task is to identify one or more patterns from the provided matrix. Extract the patterns from the matrix, preserving their digits and positions.
        Use the algorithm provided under the extraction field in the pattern description to extract the patterns. 
        Use other fields like description, location, unique_identifier, etc to your advantage to extract the patterns.
        Replace all other entries that are not a part of the pattern being extracted in the matrix with null.
        Present your result as a list of lists like this:
        [
        [0, null, null, 0],
        [null, 0, 0, null],
        [0, null, null, 0]
        ]
        If there are multiple patterns to be found in the matrix that satisfy the description for the pattern then output all of these matrices as a list of matrices.
        
        Make sure that all the not null entries in your output matrix representing a pattern is has same digit and is at the same position as in the original matrix.
        For example, if you were to extract a square formed by digit 7 on the following input matrix:
        [
        [2, 2, 2, 0, 0], 
        [2, 2, 2, 0, 0], 
        [2, 2, 2, 0, 0], 
        [0, 0, 0, 7, 7], 
        [0, 0, 0, 7, 7]
        ]
        then your output should be:
        [
        [null, null, null, null, null], 
        [null, null, null, null, null], 
        [null, null, null, null, null], 
        [null, null, null, 7, 7], 
        [null, null, null, 7, 7]
        ]
        On the other hand, if the pattern description was a square of varying sizes and colors. Then you should output a list of 2 matrices one for the square formed by 2s and other for the square formed by 7s.
        [
            [
            [null, null, null, null, null], 
            [null, null, null, null, null], 
            [null, null, null, null, null], 
            [null, null, null, 7, 7], 
            [null, null, null, 7, 7]
            ],
            [
            [2, 2, 2, null, null], 
            [2, 2, 2, null, null], 
            [2, 2, 2, null, null], 
            [null, null, null, null, null], 
            [null, null, null, null, null]
            ]

        ]
        Note that the position and digit of the cells in the relevant pattern matrix are as in the original matrix.
        Do not shy from finding multiple patterns adhering to the description of the pattern and reporting all the them as a list of matrices.
        For example, if you have a pattern description and multiple patterns adhere to the description then it is highly likely that these patterns would be
        distinguishable from each other. They would either be separated in position i.e. they would be non contiguos or they would have differenct digits.
        In these ways or other creative ways the patterns would be distinguishable from each other and you can report all the patterns as a list of matrices.
        Also note that just because a part of pattern is not non contiguos or has different digits does not make it a different pattern, you should also look
        description of the pattern and decide using your wisdom as what would be the most relevant segregation of the patterns.
        """
        return prompt


