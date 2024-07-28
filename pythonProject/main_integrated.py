import sys, os
from pathlib import Path

from globals import IS_DEBUG
from utils.file_handling import load_json_by_page
from utils.cacher import save_cached_data, load_cached_data, cached_call
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from llm.pattern_extraction.training_cases_based_pattern_extractor import TrainingCasesBasedPatternExtractor
from llm.challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from llm.integrated.signatures.input_patterns_based_output_pattern_description import input_based_output_pattern_chat, InputPatternsBasedOutputPatternDescription
from llm.pattern_extraction.pattern_extractor import extract_and_validate_patterns

def main():
    page_number = 13
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
        # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]
    
    if IS_DEBUG:
        extractor = load_cached_data(f"cache/integrated/input_extractor_{page_number}.pickle")
        if extractor is None:

            extractor = TrainingCasesBasedPatternExtractor(training_set)
            extractor.find_probable_causation(page_number)
            extractor.find_input_patterns(page_number)
            extractor.decompose_input_grids()
            save_cached_data(f"cache/integrated/input_extractor_{page_number}.pickle", extractor)
    if IS_DEBUG:
        new_extractor = load_cached_data(f"cache/integrated/output_extractor_{page_number}.pickle")
        if new_extractor is None:
            extractor.find_output_patterns(page_number)
            extractor.decompose_output_grids()
            save_cached_data(f"cache/integrated/output_extractor_{page_number}.pickle", extractor)
        else:
            extractor = new_extractor
    pass



if __name__ == "__main__":
    main()

