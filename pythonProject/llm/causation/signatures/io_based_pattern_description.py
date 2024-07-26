
from typing import List, Optional, Dict
import dspy
from pydantic import BaseModel, Field, ConfigDict
from custom_types.matrix import Matrix
from custom_types.input_output_pair import input_output_pair
from ...pattern_extraction.signatures.pattern_description_signature import PatternDetails
from ...challenge_details.challenge_description import ChallengeDescription, challenge_description_obj

from ...connectors.dspy import DSPy
from ...connectors.dspy_LMs.claude_chat import ClaudeChat

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

class IOBasedProbableCausation(dspy.Signature):
    """
    Defines the input and output fields for the pattern identification task.
    """
    challenge_description: ChallengeDescription = dspy.InputField(default=challenge_description_obj)
    question: str = dspy.InputField()
    input_ouptut_pairs: List[input_output_pair] = dspy.InputField()
    causation_description: str = dspy.OutputField()

    model_config = ConfigDict(from_attributes=True)


    @staticmethod
    def sample_prompt() -> str:
        prompt = """
            You have been provided with a list of input-output pairs. These pairs are part of training set that is described in the Challenge Description.
            I want you to take a look at the input-output pairs and identify the most relevant and the most prominent caudation rule for tranforming the input matrix to the output matrix.
            While finding the causation/transformation rules try to focus on the following:
            1. Patterns: Try to talk about the patterns that are found in input and the output matrices and how the patterns transform from the input to the output.
            2. Movement: Try to figure out if there has been movement of the patterns in the input matrix to the output matrix.
            3. Colors: Try to figure out if there has been a change in the colors of the patterns in the input matrix to the output matrix.
            4. Affine transformations: Try to figure out if there has been an tranlation, rotation, scaling, mirror image along a particular axis
              of the patterns in the input matrix to the output matrix.
            5. Noise Removal: In some cases the input matrix would be noisy and the output matrix would just be a filtered version of the input matrix.
            6. OTHER: Most imporantly - Do not stick to the above mentioned rules only. Use your imagnination and creativity to figure out the most significant
            transformation rule that is present in the input matrix to the output matrix.

            Describe the Patterns that you are talking about in detail unambiguously. 
            Describe the transformation rule that you are talking about in even more detail. 
            One should be able to read your description of patterns and transformation to understand them.

            Be as descriptive as you can while describing the patterns and transformation rule. Do not be vague.
        """
        return prompt
    

probable_causation_chat = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat, io_signature=IOBasedProbableCausation)
