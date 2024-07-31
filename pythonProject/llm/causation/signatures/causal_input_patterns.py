import os, sys
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair
from ...pattern_extraction.signatures.pattern_description_signature import PatternDetails
from ...challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from ...integrated.signatures.annotate_input_patterns import AnnotatedPattern, CausationAnnotation

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class RelevantInputPatternMap(BaseModel):
    annotated_input_patterns: List[AnnotatedPattern]
    annotated_output_pattern: AnnotatedPattern
    relevant_input_pattern_tags: List[str]
    detailed_causation: str

class CausalInputPatterns(dspy.Signature):
    """
    A class to identify causal input patterns for a given output pattern and describe the causation.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    probable_causation: str = dspy.InputField()
    input_matrix: Matrix = dspy.InputField()
    output_matrix: Matrix = dspy.InputField()
    input_patterns: List[Matrix] = dspy.InputField()
    output_pattern: Matrix = dspy.InputField()
    question: str = dspy.InputField()

    relevant_input_pattern_map: RelevantInputPatternMap = dspy.OutputField()
    
    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        You are provided with the following information:
        1. Description of the challenge
        2. Question
        3. Probable causation
        4. Complete input matrix
        5. Complete output matrix
        6. List of input patterns extracted from the input matrix
        7. One output pattern extracted from the output matrix

        Your task is to analyze these components and perform the following:

        1. Identify Relevant Input Patterns:
           - Examine the given output pattern.
           - Determine which input patterns from the provided list are required to reproduce this output pattern.
           - List the tags of these relevant input patterns after annotation.

        2. Annotate Patterns:
           - Assign meaningful tags to each relevant input pattern and the output pattern.
           - Provide a tag even if the pattern is not relevant to the transformation and in the caudation you may simple mention uninvolved.
           - These tags should represent the most important characteristics of the patterns, considering their role in the transformation.
           - The tags should be consistent with the causation description.
           
        3. Describe Detailed Causation:
           - Write a detailed algorithm that explains how the identified input patterns transform into the given output pattern.
           - This algorithm should be written as a step-by-step process that a computational system could follow.
           - Use the assigned tags to refer to the patterns in your algorithm.
           - Ensure that the algorithm only uses information from the annotated input patterns to produce the output pattern.

        Remember:
        - You only have access to the input patterns you've identified as relevant, not the entire input matrix.
        - The algorithm should be clear enough for an LLM to follow and reproduce the output pattern without seeing it.
        - Use the annotations (tags) consistently when referring to patterns in your causation description.
        - Try to identify the relevant input patterns and use them to form the ouput pattern. 
        - Remmeber that all input patterns may or may not be relevant to the transformation.
        
        Your response should include:
        1. Annotated input patterns (only the relevant ones)
        2. Annotated output pattern
        3. List of tags of relevant input patterns
        4. Detailed causation algorithm

        This information will be crucial for an LLM to understand and apply the transformation process accurately.
        """
        return prompt

causal_input_patterns_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=CausalInputPatterns)
