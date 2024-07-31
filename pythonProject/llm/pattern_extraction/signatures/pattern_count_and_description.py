import os, sys
from typing import List, Optional, Dict
import dspy

from ...challenge_details.challenge_description import ChallengeDescription
from .pattern_description_signature import PatternDetails
from custom_types.matrix import Matrix

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class PatternCountAndDescription(dspy.Signature):
    """
    Defines the input and output fields for counting and describing pattern characteristics in a matrix.
    """
    challenge_description: ChallengeDescription = dspy.InputField()
    pattern_description: PatternDetails = dspy.InputField()
    matrix: Matrix = dspy.InputField()

    pattern_count: int = dspy.OutputField()
    pattern_characteristics: List[str] = dspy.OutputField()

    @staticmethod
    def sample_prompt() -> str:
        return """
        You are given a matrix, a pattern description, and a challenge description. Your task is to:
        1. Count the number of patterns in the matrix that adhere to the given pattern description.
        2. Provide specific characteristics of each identified pattern as they occur in this particular matrix.

        Guidelines:
        - Focus only on patterns that match the given pattern description.
        - Do NOT repeat information already provided in the pattern description.
        - For each pattern, describe its unique characteristics specific to this matrix, such as:
          - Its precise position or coordinates in the matrix
          - Its size or dimensions within this specific matrix
          - Any variations or unique features it has in this instance
          - How it relates to or interacts with other elements in this specific matrix
        - Be very descriptive and precise about the characteristics, focusing on what makes this instance of the pattern unique.

        Please return:
        1. The total count of patterns matching the description.
        2. A list of specific characteristics, one for each identified pattern, detailing how it appears in this particular matrix.

        Remember, the entries in the matrices are either integers or None (empty), where None means absence of anything.
        Your goal is to provide a detailed, matrix-specific description of each pattern instance.
        """

pattern_count_and_description_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=PatternCountAndDescription)