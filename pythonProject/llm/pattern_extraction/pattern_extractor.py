from typing import List
from .pattern_description_signature import Matrix, PatternDetails
from .pattern_extraction_signature import PatternExtractionSignature
from .validation import validate_patterns
from .utils_pattern_extraction import log_interaction, dspy_pattern_extractor

def extract_and_validate_patterns(grid: Matrix, pattern_description: PatternDetails, log_file: str) -> List[Matrix]:
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
        log_interaction(log_file, prompt, response)
        
        extracted_patterns = list(response.output_pattern)
        failure_reports = validate_patterns(grid, extracted_patterns)
        
        if not failure_reports:
            return extracted_patterns
        
        # If there are failures, send them back to the LLM
        prompt = f"""
        The extracted patterns failed validation. Please correct the patterns based on the following failure reports:
        
        {failure_reports}
        
        Original grid:
        {grid}
        
        Pattern description:
        {pattern_description}
        """
        log_interaction(log_file, prompt, "Resubmitting to LLM")

    