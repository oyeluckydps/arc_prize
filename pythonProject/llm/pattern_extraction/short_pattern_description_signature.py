import os, sys
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from .pattern_description_signature import Matrix

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
    
        