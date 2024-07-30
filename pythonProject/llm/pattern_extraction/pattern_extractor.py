from typing import List

from preprocess_sample_json import pp
from .signatures.pattern_description_signature import Matrix, PatternDetails
from .signatures.pattern_extraction_signature import PatternExtractionSignature
from .validation import validate_patterns
from ..utils import log_interaction, dspy_pattern_extractor


def compare_pattern_lists(list1: List[Matrix], list2: List[Matrix]) -> bool:
    """
    Compare two lists of Matrix objects for equality, regardless of order.
    
    Args:
        list1 (List[Matrix]): First list of Matrix objects
        list2 (List[Matrix]): Second list of Matrix objects
    
    Returns:
        bool: True if the lists contain the same Matrix objects, False otherwise
    """
    if len(list1) != len(list2):
        return False
    
    # Create a copy of list2 to modify
    list2_copy = list2.copy()
    
    for matrix1 in list1:
        found = False
        for matrix2 in list2_copy:
            if matrix1 == matrix2:  # This uses the __eq__ method we defined
                found = True
                list2_copy.remove(matrix2)
                break
        if not found:
            return False
    
    return True


def extract_and_validate_patterns(grid: Matrix, pattern_description: PatternDetails, log_file: str = None) -> List[Matrix]:
    """
    Extract patterns from a grid and validate them.

    Args:
        grid (Matrix): The input grid.
        pattern_description (PatternDetails): The pattern description.
        log_file (str): Path to the log file.

    Returns:
        List[Matrix]: List of validated extracted patterns.
    """
    prompt = PatternExtractionSignature.sample_prompt()
    last_round_extracted_patterns = []

    while True:
        response = dspy_pattern_extractor.send_message(query=prompt, matrix=grid, pattern_description=pattern_description, 
                                                        num_of_rows=len(grid.matrix), num_of_cols=len(grid.matrix[0]))
        
        # print(dspy_pattern_extractor.model.history[-1]["prompt"])
        # print(dspy_pattern_extractor.model.history[-1]["response"].__dict__["content"][0].__dict__["text"])
        
        if log_file is not None:
            log_interaction(log_file, prompt, response)
        extracted_patterns = list(response.output_pattern)

        if compare_pattern_lists(extracted_patterns, last_round_extracted_patterns):
            break

        print("=" * 80)
        print(f"A total of {len(extracted_patterns)=} patterns were extracted from the grid for the pattern description {pattern_description.name}")
        print("Original grid:")
        pp.pprint(grid.matrix)
        for i, pattern in enumerate(extracted_patterns):
            print(f"Pattern {i+1}:")
            pp.pprint(pattern.matrix)
        print("=" * 80)

        failure_reports = validate_patterns(grid, extracted_patterns)

        if not failure_reports:
            return extracted_patterns
        
        # If there are failures, send them back to the LLM
        prompt = f"""
        The extracted patterns failed validation. Please correct the patterns based on the following failure reports:
        
        FAILURE REPORTS:
        {failure_reports}

        Correct your course of action based on the failure reports and perform the following task:
        {PatternExtractionSignature.sample_prompt()}
        """
        last_round_extracted_patterns = extracted_patterns
        if log_file is not None:
            log_interaction(log_file, prompt, "Resubmitting to LLM")

    