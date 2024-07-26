import sys, os
from pathlib import Path

from llm.integrated.signatures.io_based_pattern_description import io_based_pattern_chat
from llm.causation.signatures.probable_causation import ProbableCausation, probable_causation_chat
from llm.challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from utils.file_handling import load_json_by_page
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix

def main():
    working_set = 'train'
    grids_type = 'input'
    page_number = 4
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
        # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]

    causation_response = probable_causation_chat.send_message(
        challenge_description = challenge_description_obj,
        question = ProbableCausation.sample_prompt(),
        input_ouptut_pairs = training_set
    )

    print(causation_response.causation_description)

    pattern_description_response = io_based_pattern_chat.send_message(
        challenge_description = challenge_description_obj,
        question = io_based_pattern_chat.sample_prompt(),
        input_ouptut_pairs = training_set,
        probable_causation = causation_response.causation_description,
        FOR_MATRIX_TYPE = 'input'
    )
    print(pattern_description_response.pattern_description)


if __name__ == "__main__":
    main()

