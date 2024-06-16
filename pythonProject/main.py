from pathlib import Path
from GUI.data_initialize import load_all_training_blocks

def main():
    # Define the path to the folder
    folder_path = Path("processed_json/evaluation_challenges/")
    
    # Call the function from data_initialize.py for page number 3
    result = load_all_training_blocks(3)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()
