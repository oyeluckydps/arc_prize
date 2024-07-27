from typing import List

from preprocess_sample_json import pp
from .signatures.pattern_description_signature import Matrix, PatternDetails
from .signatures.pattern_extraction_signature import PatternExtractionSignature
from .validation import validate_patterns
from ..utils import log_interaction, dspy_pattern_extractor

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
    while True:
        response = dspy_pattern_extractor.send_message(query=prompt, matrix=grid, pattern_description=pattern_description)
        
        # print(dspy_pattern_extractor.model.history[-1]["prompt"])
        # print(dspy_pattern_extractor.model.history[-1]["response"].__dict__["content"][0].__dict__["text"])
        
        if log_file is not None:
            log_interaction(log_file, prompt, response)
        extracted_patterns = list(response.output_pattern)

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
        if log_file is not None:
            log_interaction(log_file, prompt, "Resubmitting to LLM")

    