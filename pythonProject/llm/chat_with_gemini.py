from PIL import Image
import google.generativeai as genai

def chat_with_gemini(image: Image, matrix: list, case_type: str, index: int, chat_session) -> dict:
    """
    Handles the chat with Gemini for input grids of both training and test type.

    Args:
        image (Image): The image to be analyzed.
        matrix (list): The matrix representation of the image.
        case_type (str): The type of case ('train' or 'test').
        index (int): The index of the case.
        chat_session: The chat session object for interacting with Gemini.

    Returns:
        dict: The responses from Gemini.
    """
    # Send the image to Gemini and ask it to analyze the input grids
    response1 = chat_session.send_message(image)
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

    return responses
