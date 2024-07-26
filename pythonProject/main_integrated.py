import sys, os
from pathlib import Path


from utils.file_handling import load_json_by_page
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from llm.pattern_extraction.test_cases_based_pattern_extractor import TestCasesBasedPatternExtractor

def main():
    page_number = 348
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
        # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]
    extractor = TestCasesBasedPatternExtractor(training_set)
    extractor.find_patterns(page_number, "input")
    extractor.decompose_grids("input")


if __name__ == "__main__":
    main()

