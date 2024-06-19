# Plandex: created the matrix_handling module
import numpy as np

def list_to_matrix(list_of_lists):
    try:
        matrix = np.array(list_of_lists, dtype=int)
        return matrix
    except ValueError as e:
        print(f"Error converting list of lists to matrix: {e}")
        return None

def matrix_to_list(matrix):
    try:
        list_of_lists = matrix.tolist()
        # Ensure all elements are integers
        list_of_lists = [[int(item) for item in row] for row in list_of_lists]
        return list_of_lists
    except ValueError as e:
        print(f"Error converting matrix to list of lists: {e}")
        return None
