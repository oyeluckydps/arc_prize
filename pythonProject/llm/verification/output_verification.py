from typing import List, Tuple
from custom_types.input_output_pair import InputOutputPair
from custom_types.matrix import Matrix
from ..integrated.signatures.annotate_input_patterns import AnnotatedPattern

class OutputVerification:
    """Class for verifying reconstructed output patterns and matrices."""

    def __init__(self, training_set: List[InputOutputPair],
                 annotated_input_patterns: List[List[AnnotatedPattern]],
                 annotated_output_patterns: List[List[AnnotatedPattern]],
                 reconstructed_output_patterns: List[List[AnnotatedPattern]],
                 reconstructed_output_matrices: List[Matrix]):
        """
        Initialize the OutputVerification.

        Args:
            training_set (List[InputOutputPair]): List of input-output pairs for training.
            annotated_input_patterns (List[List[AnnotatedPattern]]): Annotated input patterns for each training case.
            annotated_output_patterns (List[List[AnnotatedPattern]]): Annotated output patterns for each training case.
            reconstructed_output_patterns (List[List[AnnotatedPattern]]): Reconstructed output patterns for each training case.
            reconstructed_output_matrices (List[Matrix]): Reconstructed output matrices for each training case.
        """
        self.training_set = training_set
        self.annotated_input_patterns = annotated_input_patterns
        self.annotated_output_patterns = annotated_output_patterns
        self.reconstructed_output_patterns = reconstructed_output_patterns
        self.reconstructed_output_matrices = reconstructed_output_matrices

    
    def check_matrix_equality(self, original: Matrix, reconstructed: Matrix) -> Tuple[bool, Matrix]:
        """
        Check if the output matrix and reconstructed output matrix are equal.

        Args:
            original (Matrix): Original output matrix.
            reconstructed (Matrix): Reconstructed output matrix.

        Returns:
            Tuple[bool, Matrix]: 
                - Boolean indicating if matrices are equal
                - Matrix where equal elements are None and different elements are from the reconstructed matrix
        """
        difference_matrix = []
        has_differences = False

        for i in range(len(original.matrix)):
            row = []
            for j in range(len(original.matrix[0])):
                if original.matrix[i][j] == reconstructed.matrix[i][j]:
                    row.append(None)
                else:
                    row.append(reconstructed.matrix[i][j])
                    has_differences = True
            difference_matrix.append(row)

        return not has_differences, Matrix(matrix=difference_matrix)


    def check_pattern_equality(self, original: List[AnnotatedPattern], reconstructed: List[AnnotatedPattern]) -> Tuple[bool, List[str]]:
        """
        Check if the extracted patterns and the output patterns are equal.

        Args:
            original (List[AnnotatedPattern]): Original annotated output patterns.
            reconstructed (List[AnnotatedPattern]): Reconstructed annotated output patterns.

        Returns:
            Tuple[bool, List[str]]: 
                - Boolean indicating if patterns are equal
                - List of difference descriptions
        """
        differences = []
        if len(original) != len(reconstructed):
            differences.append(f"Number of patterns differ: Original {len(original)}, Reconstructed {len(reconstructed)}")
            return False, differences

        for i, (orig, recon) in enumerate(zip(original, reconstructed)):
            if orig.matrix != recon.matrix:
                differences.append(f"Pattern {i+1} matrices differ: Original {orig.matrix}, Reconstructed {recon.matrix}")
            if orig.annotations != recon.annotations:
                differences.append(f"Pattern {i+1} annotations differ: Original {orig.annotations}, Reconstructed {recon.annotations}")

        return len(differences) == 0, differences

    def verify_and_report_differences(self):
        """
        Verify equality of output matrices and patterns, and report differences.
        """
        for i, (input_output_pair, orig_patterns, recon_patterns, recon_matrix) in enumerate(
            zip(self.training_set, self.annotated_output_patterns,
                self.reconstructed_output_patterns, self.reconstructed_output_matrices)
        ):
            print(f"\nVerifying training case {i+1}:")
            
            # Check matrix equality
            matrices_equal, matrix_differences = self.check_matrix_equality(input_output_pair.output, recon_matrix)
            print(f"Matrix equality: {'Yes' if matrices_equal else 'No'}")
            
            if not matrices_equal:
                print("Matrix differences:")
                print(matrix_differences)
            
            # Check pattern equality
            patterns_equal, pattern_differences = self.check_pattern_equality(orig_patterns, recon_patterns)
            print(f"Pattern equality: {'Yes' if patterns_equal else 'No'}")
            
            if not patterns_equal:
                print("Pattern differences:")
                for diff in pattern_differences:
                    print(f"  {diff}")
            
            print("-" * 50)

    