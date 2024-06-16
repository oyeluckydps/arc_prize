from pathlib import Path
from GUI.data_initialize import load_all_training_blocks
from conversions.matrix_handling import list_to_matrix
from pattern.segregation import input_based

def main():
    # Define the path to the folder
    folder_path = Path("processed_json/evaluation_challenges/")
    
    # Call the function from data_initialize.py for page number 3
    result = load_all_training_blocks(3)

    train_inputs = [list_to_matrix(elem['input']) for elem in result['train']]
    train_outputs = [list_to_matrix(elem['output']) for elem in result['train']]
    
    # Find patterns in train_inputs and train_outputs
    input_patterns = [input_based(matrix) for matrix in train_inputs]
    output_patterns = [input_based(matrix) for matrix in train_outputs]
    
    # Print the result
    print(result)
    print("Input Patterns:", input_patterns)
    print("Output Patterns:", output_patterns)

if __name__ == "__main__":
    main()