from PIL import Image
from collections import OrderedDict
import pprint

import google.generativeai as genai

def sequential_input_chat(chat_session, total_train_index, total_test_index, train_inputs, test_inputs, image_path):
    chat_session.send_message(f"I'm about to show you a series of input grids. Each input grid is supplied as both a colored image and a matrix of numerical values")
    chat_session.send_message(f"""The color schema used is as followed. 
                                [ 0: (0, 0, 0),          # Black
                                  1: (255, 0, 0),        # Red
                                  2: (0, 255, 0),        # Green
                                  3: (0, 0, 255),        # Blue
                                  4: (255, 255, 0),      # Yellow
                                  5: (255, 0, 255),      # Magenta
                                  6: (0, 255, 255),      # Cyan
                                  7: (128, 0, 128),      # Purple
                                  8: (255, 165, 0),      # Orange
                                  9: (0, 128, 128)       # Teal  ]
                              Use this schema to establish that the information in grid image and the matrix is same.""")
    chat_session.send_message(f"There are a total of {total_train_index} training grids and a total of {total_test_index} test grids.")
    chat_session.send_message(f"Your task is to analyze these input grids thoroughly and identify the commonalities among the dimensions, colours, patterns, rules, repetition of patterns, and groups of patterns. Please confirm you're ready to begin this analysis.")
    
    # Usage of zero_shot_input_chat
    for idx in range(total_train_index):
        image = Image.open(image_path/f"train_{idx}_input.jpg")
        matrix = train_inputs[idx]
        print(f"Train-{idx}: Starting chat with LLM...")
        responses = zero_shot_input_chat(image, matrix, 'train', idx, chat_session)
        pprint.pprint(responses)
    
    for idx in range(total_test_index):
        image = Image.open(image_path/f"test_{idx}_input.jpg")
        matrix = test_inputs[idx]
        print(f"Test-{idx}: Starting chat with LLM...")
        responses = zero_shot_input_chat(image, matrix, 'test', idx, chat_session)
        pprint.pprint(responses)
    
    return chat_session


def zero_shot_input_chat(image: Image, matrix: list, case_type: str, index: int, chat_session) -> dict:
    """
    Handles the chat with Oracle for input grids of both training and test type.

    Args:
        image (Image): The image to be analyzed.
        matrix (list): The list of list of int(color) representation of the image.
        case_type (str): The type of case ('train' or 'test').
        index (int): The index of the case.
        chat_session: The chat session object for interacting with Oracle.

    Returns:
        dict: The responses from Oracle.
    """
    # Send the image to Oracle and ask it to analyze the input grids
    responses = OrderedDict()
    responses["ready_for_image"]        = chat_session.send_message("I am going to show you the {index}th input image of {case_type} type. Please look at it.")
    responses["showed_image"]           = chat_session.send_message(image)
    responses["ready_for_matrix"]       = chat_session.send_message("Now I am going to show you the the matrix in form of a list of lists. The entries in the matrix correspond to the rows of the input grid. Please look at it.")
    responses["showed_matrix"]          = chat_session.send_message(str(matrix))
    responses["this_set_concl"]         = chat_session.send_message("Based on the image of grid and the matrix shared here, what do you think is the nature of the input grid? Kindly share your thoughts about the dimensions, color, patterns, repetitions and everything else that you find relevant")
    responses["relation_to_previous"]   = chat_session.send_message("Now, look at the input grids and matrices sent earlier. Find the commonalities among the dimensions, colors, and patterns among all of these input grids. If this was the first set of input grid and matrix then reply that it is the first set.")
    responses["change_in_conclusion"]   = chat_session.send_message("Now, explain what new have you learned about the nature of input grids. If this was the first set of input grid and matrix then reply that it is the first set.")
    responses["overall_conclusion"]     = chat_session.send_message("Finally, what conclusions can you draw about the images and the matrices that you have seen so far? Is there any generic pattern that you can draw from the images and matrices? Do you have a hypothesis as to how these images share some common features?")

    return responses
