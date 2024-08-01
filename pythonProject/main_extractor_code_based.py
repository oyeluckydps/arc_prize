from typing import List
from pathlib import Path

from utils.file_handling import load_json_by_page
from custom_types.matrix import Matrix
from globals import IS_DEBUG, VERSION
from custom_types.input_output_pair import InputOutputPair
from utils.cacher import load_cached_data, save_cached_data
from llm.pattern_extraction.pattern_extraction_programatically import PatternExtractionProgramatically

def main_extractor_code_based(training_set: List[InputOutputPair], page_number: int):
    """
    Main function to orchestrate the pattern extraction process.
    
    Args:
    training_set (List[InputOutputPair]): List of input-output pairs for training.
    page_number (int): Page number for caching purposes.
    IS_DEBUG (bool): Flag to enable debug mode and run additional steps.
    """
    extractor = PatternExtractionProgramatically(page_number, training_set)
    extractor.find_probable_causation()

    if IS_DEBUG:
        # Block 1: Find INPUT pattern descriptions, count, python code, and extract patterns
        cache_file = f"cache/integrated/{VERSION}/{page_number}/checkpoint/1_input_pattern_extraction.pickle"
        cached_data = load_cached_data(cache_file)

        if cached_data:
            extractor = cached_data
        else:
            extractor.find_pattern_description('input')
            extractor.count_and_describe_patterns('input')
            extractor.find_python_code('input')
            extractor.input_patterns_extractor()

            # save_cached_data(cache_file, extractor)

        # Block 2: Find INPUT pattern descriptions, count, python code, and extract patterns
        cache_file = f"cache/integrated/{VERSION}/{page_number}/checkpoint/2_output_pattern_extraction.pickle"
        cached_data = load_cached_data(cache_file)

        if cached_data:
            extractor = cached_data
        else:
            extractor.find_pattern_description( 'output')
            extractor.count_and_describe_patterns('output')
            extractor.find_python_code('output')
            extractor.output_patterns_extractor()
            
            # save_cached_data(cache_file, extractor)

        # Block 3: Map relevant input patterns to output patterns.
        cache_file = f"cache/integrated/{VERSION}/{page_number}/checkpoint/3_relevant_input_patterns.pickle"
        cached_data = load_cached_data(cache_file)

        if cached_data:
            extractor = cached_data
        else:
            extractor.map_relevant_input_patterns()
            # extractor.find_mapping_python_code()
            
            save_cached_data(cache_file, extractor)
    else:
        extractor.find_probable_causation()
        extractor.find_pattern_description('input')
        extractor.find_pattern_description('output')
        extractor.count_and_describe_patterns('input')
        extractor.count_and_describe_patterns('output')
        extractor.find_python_code()
        extractor.patterns_extractor()
        extractor.map_relevant_input_patterns()
        extractor.find_mapping_python_code()
    return extractor


if __name__ == "__main__":
    page_number = 3
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
    
    # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]
    extractor = main_extractor_code_based(training_set, page_number)
    pass

