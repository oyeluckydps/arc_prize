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

class PatternDescriptionSignature(dspy.Signature):
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
        Please identify non-overlapping and distinct common pattern descriptions or feature description across the given input matrices. 
        Ensure that the patterns identified following the list of pattern descriptions provided by you are exhaustive 
        such that if one were to remove the patterns one by one from a matrix, nothing should remain.
        At the same time, ensure that the patterns that would be extracted following the description provided by you are distint 
        i.e no pattern in the provided grids should match two or more descriptions.
        Each pattern should be uniquely identifiable by only one description.
        List any unique patterns or exceptions that do not conform to these common patterns. 
        
        In this list of patterns descriptions:
        Focus only on describing the physical patterns or features you observe in the matrices.
        Ensure that the patterns identified are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.
        Try to find the generic pattern descriptions that adhere to many patterns. 
        If a pattern satisfies a pattern description already listed then it shouldn't satisfy pattern description for any other entry. 
        If you feel that some pattern might be missed due to above restrisction on the pattern description formation then try to make the pattern description as generic as possible so that it accounts for the left out patterns.
        
        Remember:
        A pattern description can help find multiple patterns in a single matrix.
        But no two or more pattern descriptions can describe the same pattern.
        
        Examples:
        If you see a background across all the input matrices, mention "background" as a single pattern.
        If you see square shapes of different sizes that can be generalized, mention "squares."
        If you observe random patterns at the same location in the matrices, mention "random pattern at the particular corner of matrix."
        
        Here are the input matrices:
        """
        return prompt
    

    

