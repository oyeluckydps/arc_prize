import os
from pathlib import Path
from PIL import Image
from .input_chat import sequential_input_chat
from utils.file_handling import image_folder_path, json_folder_path, load_json_by_page
from .snapshot import get_snapshots
from connectors.gemini import Gemini

# Define the folder for images
IMAGES_FOLDER = Path("snapshots/evaluation_challenges/")

def setup_gemini_chat(page_image_path: str, total_train_index: int, total_test_index: int) -> Oracle:
    """
    Sets up the Germini chat session.

    Args:
        page_image_path (str): The path to the page image.
        total_train_index (int): The total number of training inputs.
        total_test_index (int): The total number of test inputs.

    Returns:
        oracle: The Gemini chat session.
    """
    system_instruction = f"""I have got a puzzle to solve. {total_train_index} training input-output set of grids/matrixes are provided to me. I am to go through these matrices to find the correct causation between input and output. Then I have to apply the same causation rule to the {total_train_index} test images for which I am only provided with the input to generate the corresponding output. The input images and the output images are grids of various colors, where black is assumed the absence of any color. Your job is to extract the cell and grid features as required to complete the task asked via prompt.
                            The general strategy would be to solve the problem in four steps. 
                            1. INPUT COMMONALITY: First I will show you the input grids from both training and test set first. I would ask you to find the patterns and commonalities. 
                            2. OUTPUT COMMONALITY: Then, I would ask you to do the same with output images from both training and test set. 
                            3. CAUSATION: Then using the patterns and commonalities that you have found for the input sets and the output sets, I would ask you to draw the causation from input to output.
                            4. EXTENSION: Finally, I will again provide you the test input images and it is your job is to apply the causation rules found in the last step to generate the output for these test cases."""
    
    oracle = Gemini(strategy_method="zero_shot", system_info=system_instruction)
    return oracle

def analyze_images(working_set: str, page_number: int) -> None:
    """
    Analyzes images in the specified working set and page number.

    Args:
        working_set (str): The working set to be used.
        page_number (int): The page number to be loaded.
    """
    get_snapshots(working_set, page_number)

    # Define the path to the images folder
    image_path = image_folder_path(working_set, page_number)  

    # Define the path to the data folder
    folder_path = json_folder_path(working_set)
    
    # Call the function from data_initialize.py for page number 3
    result = load_json_by_page(folder=folder_path, page_number=page_number)

    train_inputs = [elem['input'] for elem in result['train']]
    test_inputs = [elem['input'] for elem in result['test']]

    # Read all files in the directory
    files = list(image_path.glob('*.jpg'))

    # Identify the total_page.jpg file
    total_page_image_path = image_path / 'total_page.jpg'

    # Identify the max index for train and test files
    total_train_index, total_test_index = len(train_inputs), len(test_inputs)

    print(f"Total train index: {total_train_index}, Total test index: {total_test_index}")

    oracle = setup_gemini_chat(total_page_image_path, total_train_index, total_test_index)

    sequential_input_chat(oracle, total_train_index, total_test_index, train_inputs, test_inputs, image_path)

    print(oracle.model.chat_history)

    