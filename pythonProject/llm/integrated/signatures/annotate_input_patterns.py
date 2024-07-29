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


class CausationAnnotation(BaseModel):
    tag: str = Field(..., description="The tag/name that is most relevant to this pattern.")
    causation: str = Field(..., description="The causation/transformation rule that helps in the transformation of this pattern.")

    model_config = ConfigDict(populate_by_name=True)


class AnnotatedPattern(BaseModel):
    matrix: Matrix = Field(..., description="The pattern to be annotated")
    annotations: CausationAnnotation = Field(..., description="The annotations/tags that are are most relevant to this pattern.")
    
    model_config = ConfigDict(populate_by_name=True)


class AnnotatePatterns(dspy.Signature):
    """
    A class to annotate the input and output patterns and find a detailed causation.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    question: str = dspy.InputField()
    input_ouptut_pairs: List[InputOutputPair] = dspy.InputField()
    probable_causation: str = dspy.InputField()
    input_matrix :Matrix = dspy.InputField()
    extracted_input_patterns: List[Matrix] = dspy.InputField()
    output_matrix :Matrix = dspy.InputField()
    extracted_output_patterns: List[Matrix] = dspy.InputField()

    detailed_causation: str = dspy.OutputField()
    annotated_input_patterns: List[AnnotatedPattern] = dspy.OutputField()
    annotated_output_patterns: List[AnnotatedPattern] = dspy.OutputField()
    
    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        You are provided the description of the challenge and the various components involved in the puzzle. I want you to read that.
        You are then provided with the description of the most probable cause of the transformation from the input matrix to the output matrix.
        You are also provided the training set as the input_output_pairs. 
        These pair of matrices contain all the input and corresponding output grids of the training set.
        
        Now I want you to focus on the following
            - input matrix
            - patterns extracted from the input matrix
            - output matrix 
            - patterns extracted from the output matrix
        
        Given these input and output matrices and their corresponding patterns, you need to do the follwing three tasks:
            - Find Detailed Causation: Given the patterns found in the input matrix, 
                identify the most relevant and most prominent causation/transformation rule that transforms each pattern or a group of the input patterns 
                into one or more patterns in the output matrix. Write the causation as a set of instructions/algorithms for an LLM to follow.
                The LLM should be able to transform the input patterns into the corresponding output patterns using the detailed causation that you provide here.
                Use the tags that you will annotate to refer to the input patterns and the output patterns. 
                Remember that the LLM will have access to the input grid, extracted input patterns with its annotation, and the detailed causation that you provide here.
                The LLM should be able to use only these information and recreate the otuput patterns. 
                Remember that the LLM will not have access to the output grid and pattern during the transformation process.
            - Annonate input patterns: With respect to the causation/transformation rule for each pattern or group of patterns, 
                provide the most relevant name to a pattern or the same name to the group of patterns. So that they can be referred easily. 
                If you need to refer to the patterns in an order then you may use an index followed by a hyphen. 
                Mention the naming convention in the detailed causation field so that the LLM can refer to the input patterns with ambiguity.
                In the causation field, specify how this particular pattern or group of patterns with the same tag 
                are tranformed into the output pattern/patterns. Mention the causation as a set of instructions/algorithms for an LLM to follow.
                The LLM should be able to transform the input patterns into the corresponding output patterns using the detailed causation that you provide here.
                Use the tags that you will annotate to refer to the input patterns and the output patterns. 
                Remember that the LLM will have access to the input grid, extracted input patterns with its annotation, and the detailed causation that you provide here.
                The LLM should be able to use only these information and recreate the otuput patterns. 
                Remember that the LLM will not have access to the output grid and pattern during the transformation process.
            - Annonate output patterns: With respect to the causation/transformation rule for each pattern or group of patterns. 
                Provide a relevant name to each pattern or group of patterns. So that they can be referred easily. In the causation field,
                specify how this particular pattern or group of patterns is constructed from the input pattern/patterns.
        
        Strategy:
            1. Think about all the patterns found in the input matrix and try to find how they combine or tranform to form the patterns found in the output matrix.
                This will form the detailed causation. 
            2. Once you have identified the causation/transformation rule, for each input pattern, try to find the most relevant tag that represents the
                most important characteristic of the pattern given the identified causation, characteristic (such as color, size, shape, etc.) of the pattern itself.
            3. For each of this input patterns, along with tag write the causation rule/algorithm that must be followed to transform this pattern 
                into the corresponding. Refer to output patterns by their tag only as the LLM will not have access to the output matrices while applying these
                causation rules to recreate the output patterns. Do not refer to the properties/characteristics of the output matrices.
                Mention the tags of output patterns that this input pattern is going to affect or transform into.
            4. Do the same for the output matrix and annotate the output patterns. Find the most relevant tag for each output pattern that represents the
                most important characteristic of the pattern given the identified causation, characteristic (such as color, size, shape, etc.) of the pattern itself.
            5. For each of this output patterns, along with tag write how the causation rule/algorithm worked on input pattern/patterns 
                to transform into this output pattern. Also mention the tag of input patterns that were used to transform this output pattern.
            6. Finally, in the detailed causation, provide a detailed overview of the causation rule/algorithm that was used 
                to transform the input pattern/patterns into the output pattern/patterns.
        """
        return prompt
    
annotate_patterns_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=AnnotatePatterns)

