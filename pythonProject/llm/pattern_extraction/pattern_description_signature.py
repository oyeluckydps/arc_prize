import os
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict


# Define Pydantic models
class PatternDetails(BaseModel):
    """
    Represents details of a pattern found in matrices.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    name: str = Field(..., alias="Give a suitable name to this pattern")
    matrices: Optional[List[int]] = Field(None, alias="In which matrices is this pattern found?")
    prominent_reason: Optional[str] = Field(None, alias="What makes it a prominent and outstanding pattern?")
    location: Optional[str] = Field(None, alias="Where is the pattern to be found?")
    unique_identifier: Optional[str] = Field(None, alias="How to uniquely identify this pattern if an input matrix is provided?")
    common_features: Optional[List[str]] = Field(None, alias="If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?")
    varying_features: Optional[List[str]] = Field(None, alias="If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?")


class PatternList(BaseModel):
    """
    Represents a list of pattern descriptions found in matrices.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    list_of_patterns: List[PatternDetails] = Field(..., alias="List all the pattern descriptions of the patterns found in the matrices")


class PatternSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    question: str = dspy.InputField()
    matrices: Dict[str, List[List[int]]] = dspy.InputField()
    patterns_description: PatternList = dspy.OutputField()


def identify_patterns(question: str, matrices: Dict[str, List[List[int]]]) -> PatternList:
    """
    Identifies patterns in matrices based on the given question.

    Args:
        question (str): The question describing the matrices and pattern identification task.

    Returns:
        PatternList: A list of identified patterns.
    """
    # Initialize Claude model
    claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
    dspy.settings.configure(lm=claude)

    # Create a predictor using the PatternSignature
    predictor = dspy.TypedPredictor(PatternSignature)

    # Predict patterns based on the question
    solution = predictor(question=question, matrices=matrices)

    return solution.patterns_description

def main():
    """
    Main function to demonstrate pattern identification.
    """
    # Sample question describing the matrices and pattern identification task
    sample_question = """
    Please identify non-overlapping and distinct common patterns or features across the given input matrices. 
    List any unique patterns or exceptions that do not conform to these common patterns. 
    Ensure that the patterns are exhaustive such that if one were to remove the patterns one by one from a matrix, nothing should remain.
    
    In this list of patterns:
    Focus only on describing the physical patterns or features you observe in the matrices.
    Ensure that the patterns identified are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.
    
    Examples:
    If you see a background across all the input matrices, mention "background" as a single pattern.
    If you see square shapes of different sizes that can be generalized, mention "squares."
    If you observe random patterns at the same location in the matrices, mention "random pattern at the particular corner of matrix."
    
    Here are the input matrices:
    """

    sample_matrices = {
        "Matrix 2":
                    [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                    [8, 8, 8, 0, 7, 7, 0, 2, 2, 2],
                    [8, 8, 8, 0, 7, 7, 0, 2, 2, 2]
                    ],
        "Matrix 1":
                    [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 4],
                      [1, 1, 0, 2, 2, 0, 3, 3, 0, 4],
                      [1, 1, 0, 2, 2, 0, 3, 3, 0, 4]]
    }

    # Identify patterns
    patterns = identify_patterns(sample_question, sample_matrices)

    # Print identified patterns
    for pattern in patterns.list_of_patterns:
        print(f"Pattern: {pattern.name}")
        print(f"Location: {pattern.location}")
        print(f"Prominent reason: {pattern.prominent_reason}")
        print(f"Unique identifier: {pattern.unique_identifier}")
        print("---")

if __name__ == "__main__":
    main()