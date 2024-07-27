import sys, os
from pathlib import Path

from globals import IS_DEBUG
from utils.file_handling import load_json_by_page
from utils.cacher import save_cached_data, load_cached_data, cached_call
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from llm.pattern_extraction.test_cases_based_pattern_extractor import TestCasesBasedPatternExtractor
from llm.challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from llm.integrated.signatures.input_patterns_based_output_pattern_description import input_based_output_pattern_chat, InputPatternsBasedOutputPatternDescription
from llm.pattern_extraction.pattern_extractor import extract_and_validate_patterns

def main():
    page_number = 4
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
        # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]
    
    if IS_DEBUG:
        extractor = load_cached_data(f"cache/integrated/extractor_{page_number}.pickle")
        if extractor is None:

            extractor = TestCasesBasedPatternExtractor(training_set)
            extractor.find_patterns(page_number, "input")
            extractor.decompose_grids("input")
            save_cached_data(f"cache/integrated/extractor_{page_number}.pickle", extractor)
        probable_causation = extractor.probable_causation
        all_input_extracted_patterns = extractor.extracted_patterns

    all_patterns_for_an_input_matrix = [[pattern for _, _, extracted in patterns_for_io_pair.values() for pattern in extracted] \
                                        for patterns_for_io_pair in all_input_extracted_patterns.values()]
    
    
    all_pattern_descriptions = []
    all_extracted_output_patterns = []
    for i, input_extracted_patterns in enumerate(all_input_extracted_patterns):
        input_based_ouptut_pattern = cached_call(input_based_output_pattern_chat.send_message)\
                                (f"integrated/input_based_output_pattern_description_{page_number}_{i}.pickle", ["pattern_description"])
        pattern_description = input_based_ouptut_pattern(
            challenge_description = challenge_description_obj,
            question = InputPatternsBasedOutputPatternDescription.sample_prompt(),
            input_ouptut_pairs = training_set,
            probable_causation = probable_causation,
            input_matrix = training_set[i].input,
            extracted_input_patterns = all_patterns_for_an_input_matrix[i],
            output_matrix = training_set[i].output
        )
        all_pattern_descriptions.append(pattern_description.pattern_description)
        
        print("=" * 80)
        print(f"Extracting output patterns in accordance to the pattern description from grid {i+1}.")
        print(f"Pattern description: {pattern_description.pattern_description}")
        print(f"Grid: ")
        print(training_set[i].output)
        print("=" * 80)

        extracted_patterns = extract_and_validate_patterns(training_set[i].output, pattern_description.pattern_description)
        all_extracted_output_patterns.append(extracted_patterns)
    


    
    


    

if __name__ == "__main__":
    main()

