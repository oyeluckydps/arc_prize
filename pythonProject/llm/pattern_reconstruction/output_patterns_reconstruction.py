import datetime
from typing import List, Tuple
from custom_types.matrix import Matrix
from custom_types.input_output_pair import InputOutputPair
from ..integrated.signatures.annotate_input_patterns import AnnotatedPattern
from ..challenge_details.challenge_description import ChallengeDescription, challenge_description_obj
from .signatures.reconstruct_output_patterns import ReconstructOutputPatterns, reconstruct_output_patterns_chat
from utils.cacher import cached_call

class OutputPatternsReconstruction:
    """Class for reconstructing output patterns based on input patterns and causation rules."""

    def __init__(self, page_number: int, training_set: List[InputOutputPair], 
                 annotated_input_patterns: List[List[AnnotatedPattern]], 
                 detailed_causation: List[str]):
        """
        Initialize the OutputPatternsReconstruction.

        Args:
            page_number (int): The page number for caching purposes.
            training_set (List[InputOutputPair]): List of input-output pairs for training.
            annotated_input_patterns (List[List[AnnotatedPattern]]): Annotated input patterns for each training case.
            detailed_causation (List[str]): Detailed causation rules for each training case.
        """
        self.page_number = page_number
        self.training_set = training_set
        self.annotated_input_patterns = annotated_input_patterns
        self.detailed_causation = detailed_causation
        self.reconstructed_output_patterns = []
        self.reconstructed_output_matrices = []
        self.time = f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        self.log_file = f"logs/output_reconstruction_{self.time}.txt"

    def reconstruct_output_patterns(self, input_grid: Matrix, 
                                    annotated_input_patterns: List[AnnotatedPattern])\
                                    -> Tuple[Matrix, List[AnnotatedPattern]]:
        """
        Reconstruct output patterns based on input grid, annotated input patterns, and detailed causation.

        Args:
            input_grid (Matrix): The input grid.
            annotated_input_patterns (List[AnnotatedPattern]): Annotated input patterns for the given input grid.
            detailed_causation (str): Detailed causation rules for the given input grid.

        Returns:
            List[AnnotatedPattern]: Reconstructed and annotated output patterns.
        """
        reconstruction_response = cached_call(reconstruct_output_patterns_chat.send_message)(
            f"integrated/reconstruct_output_patterns_{self.page_number}.pickle",
            ["reconstructed_output_patterns", "reconstructed_output_matrix"]
        )(
            challenge_description=challenge_description_obj,
            question=ReconstructOutputPatterns.sample_prompt(),
            input_grid=input_grid,
            annotated_input_patterns=annotated_input_patterns,
            detailed_causation=self.detailed_causation
        )

        reconstructed_output_patterns = reconstruction_response.reconstructed_output_patterns
        reconstructed_output_matrix = reconstruction_response.reconstructed_output_matrix

        print(f"Input Grid:\n{input_grid}\n")
        print(f"Annotated Input Patterns:\n{annotated_input_patterns}\n")
        print(f"Detailed Causation:\n{self.detailed_causation}\n")
        for recon_output_pattern in reconstructed_output_patterns:
            print(f"Reconstructed Output Pattern:\n{recon_output_pattern}\n")
        print(f"Reconstructed Output Matrix:\n{reconstructed_output_matrix}\n")
        print("=" * 80 + "\n")

        return reconstructed_output_matrix, reconstructed_output_patterns
    
    def reconstruct_all_output_patterns(self):
        """
        Iteratively reconstruct output patterns for all input grids in the training set.
        """
        for i, (input_output_pair, input_patterns) in enumerate(
            zip(self.training_set, self.annotated_input_patterns)):
            
            print(f"Reconstructing output for training case {i+1}:")
            reconstructed_matrix, reconstructed_patterns = self.reconstruct_output_patterns(
                input_output_pair.input,
                input_patterns
            )
            self.reconstructed_output_patterns.append(reconstructed_patterns)
            self.reconstructed_output_matrices.append(reconstructed_matrix)
            print(f"Reconstruction for training case {i+1} completed.\n")

        print("All output patterns have been reconstructed.")

