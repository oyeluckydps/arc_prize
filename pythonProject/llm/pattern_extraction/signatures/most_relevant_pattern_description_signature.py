
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from .pattern_description_signature import PatternDescription
from custom_types.matrix import Matrix


class MostRelevantPatternDescriptionSignature(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    matrices: Dict[str, Matrix] = dspy.InputField()
    pattern_description: PatternDescription = dspy.OutputField()
    question: str = dspy.InputField()

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt() -> str:
        prompt = """
            Analyze the given input matrices and provide the pattern description of the most relevant and the most frequently occuring patterns. 
            Try to generalize your the descriptions to cover as many patterns as possibles in all matrices.

            1. Generic: Aim for descriptions that can apply to multiple instances across the matrices, rather than overly specific descriptions.

            2. Physical features only: Focus on observable physical patterns or features in the matrices, not abstract concepts.

            3. Common across matrices: Prioritize pattern descriptions that are present across all or most matrices, not just in one or two.

            4. Try to find the pattern description that covers the most patterns or most cells in the matrices.

            Guidelines:
            - A single description can identify multiple patterns within one matrix.
            - Include common elements across all matrices (e.g., background) as a single pattern if applicable.
            - Generalize similar shapes or elements of different sizes when possible 
                (e.g., "squares of varying sizes", "quadrilaterals instead of separating squares and rectangels into two patterns").
            - Note consistent positioning of elements (e.g., "random pattern in top-left corner").

            The entries in the matrices are either None/empty where it means absernce of anything. 
            Else it can be a digit between 0 and 9 which represent difference colors.
            For example 0 represents black color, 1 represents red color, 2 represents green color and so on. Try to find the patterns based on these phenomena.

            Some examples of pattern descriptions:
            1. Background of black color( digit 0) or any other color or a noisy background.
            1. Squares of varying sizes, with a background of random colors.
            2. A spiral pattern with a background of random colors.
            3. A circle with a background of random colors.
            4. A random pattern in the top-left corner.

            Use your imagination and creativity to describe most of the patterns under a single generic description. 
            
            It is also possible that all the patterns on the provided matrices are covered by a single description 
            but in this case, you must be very sure that one description that is not very generic accounts for all the patterns.
            If you can be slightly specific and find a pattern or group of patterns that are different from other patterns or cells then mention it.
            However, if you are sure that all the patterns are covered by a single description then you can mention the name as "COMPLETE_PATTERN_SET".

            Remember you need to given description of only one pattern and the it should be unambiguos. 
            An LLM or any automated machine should be able to read your description and unambiguously identify the patterns that is being described from the matrices.

            Provide your analysis based on the following input matrices:
        """
        return prompt
    

