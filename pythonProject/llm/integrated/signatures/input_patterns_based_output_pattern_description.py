import os, sys
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair
from ...pattern_extraction.signatures.pattern_description_signature import PatternDetails
from ...challenge_details.challenge_description import ChallengeDescription, challenge_description_obj

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class InputPatternsBasedOutputPatternDescription(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    input_output_pairs: List[InputOutputPair] = dspy.InputField()
    probable_causation: str = dspy.InputField()
    input_matrix: Matrix = dspy.InputField()
    extracted_input_patterns: List[Matrix] = dspy.InputField()
    output_matrix: Matrix = dspy.InputField()
    question: str = dspy.InputField()

    pattern_description: PatternDetails = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        You are provided the description of the challenge and the various components involved in the puzzle. I want you to read that.
        You are then provided with the description of the most probable cause of the transformation from the input matrix to the output matrix.
        Now, it is your job to concentrate on this transformation rule, and the provided input matrix along with all the interesting patterns extracted 
        from this input matrix. 
        It is your job to find the patterns from the output matrix that are most relevant to the transformation taking place on the input matrix 
        along with the extracted patterns.
        It is highly likely that the patterns extracted from the input matrix get transformed following the transformation rule, so try to describe the patterns
        of the output matrix that will be formed by applying the transformation rule on the extracted patterns.
        While trying to find the most relevant patterns' description, look at the other output matrices in the input-output pairs. It is highly likely that
        the patterns most relevant to the transformation rule will be common across all the output matrices.

        Try to find the descriptions that covers many patterns across all the matrices of type FOR_MATRIX_TYPE.

        1. Generic: Aim for descriptions that can apply to multiple instances across the FOR_MATRIX_TYPE matrices, rather than overly specific descriptions.

        2. Physical features only: Focus on observable physical patterns or features in the matrices, not abstract concepts.

        3. Common across matrices: Prioritize pattern descriptions that are present across all or most matrices, not just in one or two.

        4. Try to find the pattern description that covers the most patterns or most cells in the matrices.

        5. MOST IMPORTANT: Try to find the pattern description for the patterns that play the most significant role in transformation from the input matrix to the output matrix.
        
        Guidelines:
        - A single description can identify multiple patterns of same type within one matrix.
        - Include common elements across all matrices (e.g., background) as a single pattern if applicable.
        - Generalize similar shapes or elements of different sizes when possible 
            (e.g., "squares of varying sizes", "quadrilaterals instead of separating squares and rectangles into two patterns").
        - Note consistent positioning of elements (e.g., "random pattern in top-left corner").

        The entries in the matrices are either None/empty where it means absence of anything. 
        
        Some examples of pattern descriptions:
        1. Background of black color( digit 0) or any other color or a noisy background.
        1. Squares of varying sizes, with a background of random colors.
        2. A spiral pattern with a background of random colors.
        3. A circle with a background of random colors.
        4. A random pattern in the top-left corner.
        
        Use your imagination and creativity to find the most relevant pattern and try to describe it under a single generic description. 
        
        It is also possible that no special or specific pattern is present that is relevant to the causation/transformation.
        In this case, you must be very sure that the output matrix is a result of the transformation and there is no special pattern in it 
        that reveals better understanding of the transformation taking place.
        Only then you can mention the name as "COMPLETE_PATTERN_SET" signifying that the complete output matrix can no further be reduced to smaller or more relevant pattern and the complete matrix is relevant to the causation/transformation.

        Remember you need to give only one description for the most prominent patterns and it should be unambiguous. 
        An LLM or any automated machine should be able to read your description and the extraction algorithm 
        to unambiguously identify the patterns that are being described from the matrices. 
        In the extraction, only mention the algorithm and elements that are concerned with the output matrix as the LLM will use only this output matrix
        and the algorithm to extract the relevant patterns out of it. Do not talk about anything other than the mechanism to extract the output patterns.

        REMEMBER: You have to give the pattern description for the relevant patterns of output matrix only.
        """
        return prompt
    
input_based_output_pattern_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=InputPatternsBasedOutputPatternDescription)
