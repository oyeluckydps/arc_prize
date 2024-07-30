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
from llm.pattern_reconstruction.output_patterns_reconstruction import OutputPatternsReconstruction 
from llm.verification.output_verification import OutputVerification

def main():
    page_number = 3
    grids = load_json_by_page(folder=Path('processed_json/evaluation_challenges/'), page_number=page_number)
    
    # Form a list of input-output pairs
    training_set = [InputOutputPair(input=Matrix(matrix=elem['input']), output=Matrix(matrix=elem['output'])) for elem in grids['train']]
    
    # Find the most probable causation and the input patterns for each training case.
    if IS_DEBUG:
        extractor = load_cached_data(f"cache/integrated/input_extractor_{page_number}.pickle")
        if extractor is None:
            extractor = TrainingCasesBasedPatternExtractor(training_set)
            extractor.find_probable_causation(page_number)
            extractor.find_input_patterns(page_number)
            extractor.decompose_input_grids()
            save_cached_data(f"cache/integrated/input_extractor_{page_number}.pickle", extractor)

    # Find the input pattern extractor code and patterns programatically for each input case.
    if IS_DEBUG:
        new_extractor = load_cached_data(f"cache/integrated/input_extractor_programatically_{page_number}.pickle")
        if new_extractor is None:
            extractor.find_python_code(page_number, 'input')
            extractor.patterns_extractor('input')
            save_cached_data(f"cache/integrated/input_extractor_programatically_{page_number}.pickle", extractor)

    # Find the output patterns for each training case.
    if IS_DEBUG:
        new_extractor = load_cached_data(f"cache/integrated/output_extractor_{page_number}.pickle")
        if new_extractor is None:
            extractor.find_output_patterns(page_number)
            extractor.decompose_output_grids()
            save_cached_data(f"cache/integrated/output_extractor_{page_number}.pickle", extractor)
        else:
            extractor = new_extractor

    # Find the input pattern extractor code and patterns programatically for each input case.
    if IS_DEBUG:
        new_extractor = load_cached_data(f"cache/integrated/input_extractor_programatically_{page_number}.pickle")
        if new_extractor is None:
            extractor.find_python_code(page_number, 'input')
            extractor.patterns_extractor('input')
            save_cached_data(f"cache/integrated/input_extractor_programatically_{page_number}.pickle", extractor)

    # Annotate the input and output patterns for each training case.
    if IS_DEBUG:
        new_extractor = load_cached_data(f"cache/integrated/annotated_extractor_{page_number}.pickle")
        if new_extractor is None:
            extractor.annotate_patterns(page_number)
            save_cached_data(f"cache/integrated/annotated_extractor_{page_number}.pickle", extractor)
        else:
            extractor = new_extractor

    # Reconstruct the output based on the input annotation and the detailed causation.
    if IS_DEBUG:
        reconstructor = load_cached_data(f"cache/integrated/output_reconstructor_{page_number}.pickle")
        if reconstructor is None:
            reconstructor = OutputPatternsReconstruction(
                page_number=page_number,
                training_set=training_set,
                annotated_input_patterns=extractor.annotated_input_patterns,
                detailed_causation=extractor.detailed_causation
            )
            reconstructor.reconstruct_all_output_patterns()
            save_cached_data(f"cache/integrated/output_reconstructor_{page_number}.pickle", reconstructor)
        
        # Access the results
        reconstructed_patterns = reconstructor.reconstructed_output_patterns
        reconstructed_matrices = reconstructor.reconstructed_output_matrices

        print(f"Number of reconstructed output patterns: {len(reconstructed_patterns)}")
        print(f"Number of reconstructed output matrices: {len(reconstructed_matrices)}")

    # Verify the reconstructed output patterns and matrices.
    verifier = OutputVerification(
        training_set=training_set,
        annotated_input_patterns=extractor.annotated_input_patterns,
        annotated_output_patterns=extractor.annotated_output_patterns,
        reconstructed_output_patterns=reconstructor.reconstructed_output_patterns,
        reconstructed_output_matrices=reconstructor.reconstructed_output_matrices
    )

    print("\nStarting verification process...")
    verifier.verify_and_report_differences()
    print("Verification process completed.")


if __name__ == "__main__":
    main()

