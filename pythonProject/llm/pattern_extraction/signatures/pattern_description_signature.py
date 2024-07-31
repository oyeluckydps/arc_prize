import os, sys
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix

# Define Pydantic models
class PatternDetails(BaseModel):
    """
    Represents the details of a pattern found in matrices. 
    Try to find patterns that are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.
    Try to find the patterns that occur across all the matrices on priority and should be given higher weightage when comparing with other competitive patterns.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    name: str = Field(..., description="Give a suitable name to this pattern")
    matrices: Optional[List[int]] = Field(..., description="In which matrices is this pattern found?")
    extraction: str = Field(..., description="If I need to extract this pattern from the matrices then how should I do it? Describe a brief algorithm that specifies the exact method to extract patterns adhering to this description.")
    prominent_reason: Optional[str] = Field(..., description="What makes it a prominent and outstanding pattern?")
    location: Optional[str] = Field(..., description="Where is the pattern to be found?")
    unique_identifier: Optional[str] = Field(..., description="How to uniquely identify this pattern if an input matrix is provided?")
    common_features: Optional[List[str]] = Field(..., description="If the pattern is found across multiple inputs then what features of the pattern are common across these inputs? If there are no common features, then mention [] that is empty list.")
    varying_features: Optional[List[str]] = Field(..., description="If the pattern is found across multiple inputs then what features of the pattern vary across these inputs? If there are no varying features, then mention [] that is empty list.")


class PatternList(BaseModel):
    """
    Represents a list of pattern descriptions found in matrices.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    list_of_patterns: List[PatternDetails] = Field(..., description="List all the pattern descriptions of the patterns found in the matrices")


class DetailedPatternDescriptionSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    matrices: Dict[str, Matrix] = dspy.InputField()
    patterns_description: PatternList = dspy.OutputField()
    question: str = dspy.InputField()

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def sample_prompt() -> str:
        prompt = """
            Analyze the given input matrices and provide a list of pattern descriptions that meet the following criteria:

            1. Exhaustive: The patterns described should cover all elements in each matrix. If all described patterns were removed from a matrix, nothing should remain.

            2. Distinct and non-overlapping: Each pattern should be uniquely identifiable by only one description. No pattern should match multiple descriptions.

            3. Generic: Aim for descriptions that can apply to multiple instances across the matrices, rather than overly specific descriptions.

            4. Physical features only: Focus on observable physical patterns or features in the matrices, not abstract concepts.

            5. Inclusive: If a pattern doesn't fit neatly into other categories, create a more general description that can include it without overlapping with existing descriptions.

            6. Common across matrices: Prioritize pattern descriptions that are present across all or most matrices, not just in one or two.

            Guidelines:
            - A single description can identify multiple patterns within one matrix.
            - However, no single pattern should be described by multiple descriptions.
            - Include common elements across all matrices (e.g., background) as a single pattern if applicable.
            - Generalize similar shapes or elements of different sizes when possible (e.g., "squares of varying sizes").
            - Note consistent positioning of elements (e.g., "random pattern in top-left corner").
            - Before adding a new pattern description, carefully consider if the patterns it would describe are already covered by an existing description.

            Provide your analysis based on the following input matrices:
        """
        return prompt

