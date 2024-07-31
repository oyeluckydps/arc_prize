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

class IOBasedPatternDescription(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    input_ouptut_pairs: List[InputOutputPair] = dspy.InputField()
    probable_causation: str = dspy.InputField()
    FOR_MATRIX_TYPE :str = dspy.InputField()
    question: str = dspy.InputField()

    pattern_description: PatternDetails = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt(FOR_MATRIX_TYPE) -> str:
        prompt = f"""
            You have been provided with a list of input-output pairs. These pairs are part of training set that is described in the Challenge Description.
            Given these pairs, it is your task to identify the most relevant pattern that plays 
            the most significant role in tranforming the input matrix to the output matrix for the {FOR_MATRIX_TYPE} matrices.
            To achieve this task you may first take a look at the causation/tranformation details provided in the probable_causation.
            Now based on this probable causation, for matrices of the {FOR_MATRIX_TYPE} type, you need to identify the most relevant pattern 
            that plays the most significant role in tranformation of the input matrices to the output matrices.

            Try to find the descriptions that covers many patterns across all the {FOR_MATRIX_TYPE} matrices.

            1. Generic: Aim for descriptions that can apply to multiple instances across the {FOR_MATRIX_TYPE} matrices, rather than overly specific descriptions.

            2. Physical features only: Focus on observable physical patterns or features in the matrices, not abstract concepts.

            3. Common across matrices: Prioritize pattern descriptions that are present across all or most matrices, not just in one or two.

            4. Try to find the pattern description that covers the most patterns or most cells in the matrices.

            5. MOST IMPORTANT: Try to find the pattern description for the patterns that play the most significant role in tranformation from 
                the input matrix to the output matrix.
            
            Guidelines:
            - A single description can identify multiple patterns of same type within one matrix.
            - Include common elements across all matrices (e.g., background) as a single pattern if applicable.
            - Generalize similar shapes or elements of different sizes when possible 
                (e.g., "squares of varying sizes", "quadrilaterals instead of separating squares and rectangels into two patterns").
            - Note consistent positioning of elements (e.g., "random pattern in top-left corner").

            The entries in the matrices are either None/empty where it means absernce of anything. 
            
            Some examples of pattern descriptions:
            1. Background of black color( digit 0) or any other color or a noisy background.
            1. Squares of varying sizes, with a background of random colors.
            2. A spiral pattern with a background of random colors.
            3. A circle with a background of random colors.
            4. A random pattern in the top-left corner.
            
            Use your imagination and creativity to find the most relevant pattern and try to describe it under a single generic description. 
            
            It is also possible that no special or specific pattenr is present that is relevant to the causation/tranformation.
            In this case, you must be very sure that the complete {"input matrices are tranformed into output matrices" if FOR_MATRIX_TYPE == "input"
                                        else "output matrices are results of transformation on input matrix"}.
            Only then you can mention the name as "COMPLETE_PATTERN_SET" signifying that the 
            complete {FOR_MATRIX_TYPE} matrix can no further be reduced to smaller or more relevant pattern and the complete matrix is relevant to the causation/tranformation.

            Remember you need to given description of only one pattern and the it should be unambiguos. 
            An LLM or any automated machine should be able to read your description and the extraction algorithm 
            to unambiguously identify the patterns that is being described from the matrices.

            REMEBER: You have to give the pattern description for the matrices of {FOR_MATRIX_TYPE} only.

            Provide your analysis based on the following input-output matrix pairs:
        """
        return prompt
    
io_based_pattern_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=IOBasedPatternDescription)


