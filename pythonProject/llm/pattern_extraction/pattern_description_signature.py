import os, sys
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from GUI.matplotlib.create_grid_image import create_grid_image
from preprocess_sample_json import pp

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


# Define the Pydantic model for matrix
class Matrix(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    matrix: List[List[Optional[int]]] = Field(description="The grid with integers representing colors or None representing absence of anything.")

    def show(self):
        create_grid_image(self.matrix)
    
    # def __str__(self):
    #     return pp.pformat(self.matrix)


class DetailedPatternDescriptionSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    question: str = dspy.InputField()
    matrices: Dict[str, Matrix] = dspy.InputField()
    patterns_description: PatternList = dspy.OutputField()

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
    

class ShortDetail(BaseModel):
    """
    Represents the details of a pattern found in matrices. 
    """
    model_config = ConfigDict(populate_by_name=True)
    
    name: str = Field(..., description="Give a suitable name to this pattern description.")
    pattern_description: str = Field(..., description="Provide a description for the patterns.")


class ShortPatternList(BaseModel):
    """
    Represents a list of pattern descriptions found in matrices.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    list_of_patterns: List[ShortDetail] = Field(..., description="List all the pattern descriptions of the patterns found in the matrices")
    

class ShortPatternDescriptionSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    question: str = dspy.InputField()
    matrices: Dict[str, Matrix] = dspy.InputField()
    patterns_description: ShortPatternList = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt() -> str:
        prompt = """
            Analyze the provided matrices and identify distinct pattern descriptions. Focus on:

            1. Physical resemblance and visual representations in the matrices.
            2. Easily identifiable patterns such as squares, circles, spirals, etc.
            3. Complex shapes that occur together or complement each other.
            4. Noisy patterns.
            5. Patterns that always occur together across all matrices.

            Guidelines:
            - Describe only patterns that are visually apparent and consistent across matrices.
            - Keep your list of pattern descriptions concise.
            - Aim for 2-3 types of patterns; rarely exceed 5 types.
            - Ensure each pattern description is unique and non-overlapping.
            - Make pattern descriptions very distinct from each other.
            - If two pattern descriptions are similar, combine them into a more generic description that encompasses both.

            List your pattern descriptions below:
        """
        return prompt
