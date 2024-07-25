from pathlib import Path
from custom_types.input_output_pair import InputOutputPair
from challenge_details.challenge_description import challenge_description_obj
from utils.file_handling import load_json_by_page
from dspy import DSPy
from dspy.signatures import Signature
from GUI.matplotlib.create_grid_image import create_grid_image

# Load a challenge set
working_set = 'train'
grids_type = 'input'
page_number = 4
grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)

# Form a list of input-output pairs
training_set = [InputOutputPair(input=elem['input'], output=elem['output']) for elem in grids['train']]

# Extract one input matrix from the test set
test_matrix = grids['test'][0]['input']

# Define a DSPy signature class
class ChallengeSignature(Signature):
    challenge_description: challenge_description_obj
    training_set: list[InputOutputPair]
    test_input_matrix: list[list[int]]
    query: str
    output_matrix: list[list[int]]

# Create an instance of the DSPy agent
dspy_agent = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=ChallengeSignature)

# Define the query
query = """
Please go through the Challenge Description, then go through the input-output pairs of the training set. 
Try to understand the causation that leads from the input matrix to the output matrix. 
Get a grasp on the frequently occurring patterns as that would help in generating the output matrix.
"""

# Pass the challenge description sample object to the LLM agent
response = dspy_agent.send_message(
    challenge_description=challenge_description_obj,
    training_set=training_set,
    test_input_matrix=test_matrix,
    query=query
)

# Display the output matrix using the GUI function
output_matrix = response.output_matrix
create_grid_image(output_matrix)
