import os
import dspy
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix
from ...integrated.signatures.annotate_input_patterns import AnnotatedPattern
from ...challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class ReconstructOutputPatterns(dspy.Signature):
    """
    A class to reconstruct output patterns based on input patterns and causation rules.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    input_grid: Matrix = dspy.InputField()
    annotated_input_patterns: List[AnnotatedPattern] = dspy.InputField()
    detailed_causation: str = dspy.InputField()
    question: str = dspy.InputField()

    reconstructed_output_patterns: List[AnnotatedPattern] = dspy.OutputField()
    reconstructed_output_matrix: Matrix = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def sample_prompt() -> str:
        prompt = """
        You are provided with the description of the challenge and the various components involved in the puzzle. Please read that carefully.

        Your task is to reconstruct the output patterns and the complete output matrix based on the following information:
        1. The input grid
        2. Annotated input patterns extracted from the input grid
        3. Detailed causation rules that describe how input patterns transform into output patterns

        Follow these steps to reconstruct the output patterns:

        1. Analyze the input grid and the annotated input patterns carefully.
        2. Study the detailed causation rules to understand how input patterns should be transformed.
        3. Apply the causation rules to the input patterns to generate output patterns.
        4. Annotate the reconstructed output patterns with appropriate tags and causation explanations.
        5. Ensure that your reconstructed output patterns are consistent with the transformation rules described in the detailed causation.

        Remember:
        - You only have access to the input grid, annotated input patterns, and detailed causation.
        - Your goal is to recreate the output patterns as accurately as possible based solely on the provided information.
        - Use the tags from the input patterns and the detailed causation to refer to patterns consistently.

        Provide your reconstructed output patterns as a list of AnnotatedPattern objects, each containing:
        - The reconstructed pattern matrix
        - Annotations including a relevant tag and an explanation of how the causation worked to recreate this pattern.
        - Use the reconstructed output pattern matrices and annotations to create a complete output matrix.

        Be as detailed and precise as possible in your reconstruction and annotations.
        """
        return prompt

reconstruct_output_patterns_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=ReconstructOutputPatterns)
