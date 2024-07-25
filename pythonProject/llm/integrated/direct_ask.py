from pathlib import Path

from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from ..challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from utils.file_handling import load_json_by_page
from ..connectors.dspy import DSPy
import dspy
from GUI.matplotlib.create_grid_image import create_grid_image
from ..utils import claude, claude_chat1

# Define a DSPy signature class
class ChallengeSignature(dspy.Signature):
    challenge_description: ChallengeDescription = dspy.InputField()
    training_set: list[InputOutputPair] = dspy.InputField()
    test_input_matrix: Matrix = dspy.InputField()
    query: str = dspy.InputField()
    output_matrix: Matrix = dspy.OutputField()

# Create an instance of the DSPy agent
direct_ask_agent = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=ChallengeSignature)


def direct_ask(test_case: int) -> list[list[int]]:
    # Define the query
    query = """
    Please go through the Challenge Description, then go through the input-output pairs of the training set. 
    Try to understand the causation that leads from the input matrix to the output matrix. 
    Get a grasp on the frequently occurring patterns as that would help in generating the output matrix.
    """

    # Load a challenge set
    page_number = test_case
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)

    # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]

    # Extract one input matrix from the test set
    test_matrix = Matrix(matrix=grids['test'][0]['input'])

    # Pass the challenge description sample object to the LLM agent
    response = direct_ask_agent.send_message(
        challenge_description=challenge_description_obj,
        training_set=training_set,
        test_input_matrix=test_matrix,
        query=query
    )

    # Display the output matrix using the GUI function
    output_matrix = response.output_matrix
    # create_grid_image(output_matrix)
    print(output_matrix)

