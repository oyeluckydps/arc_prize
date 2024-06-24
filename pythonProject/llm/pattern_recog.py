# Added comments to the code for better understanding

import os
from pathlib import Path
from PIL import Image
import google.generativeai as genai

# Configure the Gemini API
gemini_key_path = Path(".gemini_key")
with gemini_key_path.open('r') as file:
    gemini_key = file.read()
genai.configure(api_key=gemini_key)

# Define the folder for images
IMAGES_FOLDER = Path("snapshots/evaluation_challenges/")

def upload_to_gemini(path: Path, mime_type: str = None) -> genai.File:
    """
    Uploads the given file to Gemini.

    Args:
        path (Path): The path to the file to be uploaded.
        mime_type (str, optional): The MIME type of the file. Defaults to None.

    Returns:
        genai.File: The uploaded file object.
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def analyze_images(working_set: str, page_number: int) -> None:
    """
    Analyzes images in the specified working set and page number.

    Args:
        working_set (str): The working set to be used.
        page_number (int): The page number to be loaded.
    """
    # Define the path to the images
    image_path = Path(f'./snapshots/{working_set}/{page_number}/')

    # Read all files in the directory
    files = list(image_path.glob('*.jpg'))

    # Identify the total_page.jpg file
    total_page_file = image_path / 'total_page.jpg'
    if total_page_file.exists():
        upload_to_gemini(total_page_file, mime_type="image/jpeg")

    # Identify the max index for train and test files
    max_train_index = max_test_index = 0
    for file in files:
        parts = file.stem.split('_')
        if len(parts) == 3:
            case_type, index, io_type = parts
            index = int(index)
            if case_type == 'train':
                max_train_index = max(max_train_index, index)
            elif case_type == 'test':
                max_test_index = max(max_test_index, index)

    print(f"Max train index: {max_train_index}, Max test index: {max_test_index}")

def chat_with_gemini(image: Image, matrix: list, case_type: str, index: int) -> dict:
    """
    Handles the chat with Gemini for input grids of both training and test type.

    Args:
        image (Image): The image to be analyzed.
        matrix (list): The matrix representation of the image.
        case_type (str): The type of case ('train' or 'test').
        index (int): The index of the case.

    Returns:
        dict: The responses from Gemini.
    """
    # Convert the image to a format suitable for Gemini
    image_path = Path(f'temp_{case_type}_{index}.jpg')
    image.save(image_path)

    # Upload the image to Gemini
    uploaded_file = upload_to_gemini(image_path, mime_type="image/jpeg")

    # Start a chat session with Gemini
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        system_instruction="I have uploaded an image from a puzzle. You would find multiple input-output images (2-10) for Training. You would also find one or two test inputs for which output is blank (all black cells in the grid). The input images and the output images are grids of various colors, where black is assumed the absence of any color. Your job is to extract the cell and grid features as required to complete the task asked via prompt.",
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    uploaded_file,
                ],
            },
        ]
    )

    # Send the image to Gemini and ask it to analyze the input grids
    response1 = chat_session.send_message(f"I am sending a {case_type} input file of index {index}. Please analyze it.")
    response2 = chat_session.send_message("Look at the input files from all training set and even the training grid of the test cases sent earlier. Find the patterns or similarities between all of these input grids.")
    response3 = chat_session.send_message("Explain what you see, how it is related to what you have seen before, and the nature of input grids.")
    response4 = chat_session.send_message("Explain the change in your conclusion based on what you have thought earlier about the nature of input grids.")

    # Store the responses in a dictionary
    responses = {
        "what_gemini_sees": response1.text,
        "relation_to_previous": response2.text,
        "nature_of_input_grids": response3.text,
        "change_in_conclusion": response4.text,
    }

    # Clean up the temporary image file
    image_path.unlink()

    return responses

# Example usage
# image = Image.open('path_to_image.jpg')
# matrix = [[0, 1], [1, 0]]  # Example matrix
# responses = chat_with_gemini(image, matrix, 'train', 1)
# print(responses)
