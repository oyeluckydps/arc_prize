from pathlib import Path
from utils.file_handling import load_json_by_page
from logic.conversions.matrix_handling import list_to_matrix
from logic.pattern.segregation import input_based
from GUI.patterns.display import display_patterns_list
from llm.snapshot import get_snapshots

def main():
    # Define the path to the folder
    folder_path = Path("processed_json/evaluation_challenges/")
    
    # Call the function from data_initialize.py for page number 3
    result = load_json_by_page(folder=folder_path, page_number=13)

    train_inputs = [list_to_matrix(elem['input']) for elem in result['train']]
    train_outputs = [list_to_matrix(elem['output']) for elem in result['train']]
    
    # Find patterns in train_inputs and train_outputs
    input_patterns = [input_based(matrix) for matrix in train_inputs]
    output_patterns = [input_based(matrix) for matrix in train_outputs]

    index = 1

    display_patterns_list(list(zip(input_patterns, output_patterns)))
    
    # Print the result
    print(result)
    
def snap():
    working_set = "evaluation_challenges"
    page_number = 13

    get_snapshots(working_set, page_number)

if __name__ == "__main__":
    snap()