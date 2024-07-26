import sys, os
from pathlib import Path

from llm.pattern_extraction.decomposer import GridPatternExtractor
from llm.pattern_extraction.signatures.pattern_description_signature import Matrix
from utils.file_handling import load_json_by_page

def main():
    working_set = 'train'
    grids_type = 'input'
    page_number = 4
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
    _004_input_matrices = [Matrix(matrix=grid[grids_type]) for grid in grids[working_set]]
    extractor = GridPatternExtractor(_004_input_matrices, grids_type=grids_type)
    extractor.decompose_grids()

if __name__ == "__main__":
    main()

