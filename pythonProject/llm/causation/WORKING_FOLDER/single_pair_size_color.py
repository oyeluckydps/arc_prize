from pydantic import BaseModel
from typing import Tuple, List, Dict, Any

class GridAnalysis(BaseModel):
    dimensions: Tuple[int, int]
    color: List[int]

class Causation(BaseModel):
    dimension_function: str
    color_function: str
    dimension_causation: str
    color_causation: str

class CausationDict(BaseModel):
    input_dimensions: Tuple[int, int]
    input_color: List[int]
    output_dimensions: Tuple[int, int]
    output_color: List[int]
    causation: Causation

# This file will contain functions to handle the causation task for a single pair of input and output images.


def analyze_single_pair(input_image: Image, output_image: Image, input_matrix: List[List[int]], output_matrix: List[List[int]], case_type: str, index: int, chat_session) -> Dict[str, Any]:
    """
    Analyzes a single pair of input and output images and matrices.

    Args:
        input_image (Image): The input image to be analyzed.
        output_image (Image): The output image to be analyzed.
        input_matrix (List[List[int]]): The matrix representation of the input image.
        output_matrix (List[List[int]]): The matrix representation of the output image.
        case_type (str): The type of case ('train' or 'test').
        index (int): The index of the case.
        chat_session: The chat session object for interacting with the oracle.

    Returns:
        Dict[str, Any]: The analysis results including dimensions, colors, and causation.
    """
    prepare_oracle_for_causation(chat_session, case_type, index)
    input_responses = analyze_input_grid(chat_session, input_image, input_matrix)
    output_responses = analyze_output_grid(chat_session, output_image, output_matrix)
    
    input_analysis = extract_dimensions_and_color(input_responses["input_analysis"])
    output_analysis = extract_dimensions_and_color(output_responses["output_analysis"])
    
    causation_responses = find_causation(chat_session, input_analysis["dimensions"], input_analysis["color"], output_analysis["dimensions"], output_analysis["color"])
    
    causation = causation_responses["causation_analysis"]
    
    return create_causation_dict(input_analysis["dimensions"], input_analysis["color"], output_analysis["dimensions"], output_analysis["color"], causation)

def prepare_oracle_for_causation(chat_session, case_type: str, index: int) -> None:
    """
    Prepares the oracle for the causation task by sending detailed prompts.

    Args:
        chat_session: The chat session object for interacting with the oracle.
        case_type (str): The type of case ('train' or 'test').
        index (int): The index of the case.
    """
    chat_session.send_message(f"I am going to show you the {index}th input and output image of {case_type} type. Please be ready to analyze the properties related to the grid like dimensions, color, patterns, repetition, and groups of patterns. Finally, you need to tell the causation between the two grids.")

def analyze_input_grid(chat_session, input_image: Image, input_matrix: List[List[int]]) -> Dict[str, Any]:
    """
    Sends the input image and matrix to the oracle and asks it to analyze the input grids.

    Args:
        chat_session: The chat session object for interacting with the oracle.
        input_image (Image): The input image to be analyzed.
        input_matrix (List[List[int]]): The matrix representation of the input image.

    Returns:
        Dict[str, Any]: The analysis results including dimensions and colors.
    """
    responses = OrderedDict()
    responses["ready_for_image"] = chat_session.send_message("I am going to show you the input image. Please look at it.")
    responses["showed_image"] = chat_session.send_message(input_image)
    responses["ready_for_matrix"] = chat_session.send_message("Now I am going to show you the matrix in the form of a list of lists. The entries in the matrix correspond to the rows of the input grid. Please look at it.")
    responses["showed_matrix"] = chat_session.send_message(str(input_matrix))
    responses["input_analysis"] = chat_session.send_message("Analyze the input grid and provide the dimensions in the format (HEIGHT, WIDTH) and the color in the format of a set of digits {x, y, ...} where x, y are digits in the range [0, 9] and as found in the matrix. Reply in the following JSON format only: {\"dimensions\": (HEIGHT, WIDTH), \"color\": [x, y, ...]}")
    return responses
def analyze_output_grid(chat_session, output_image: Image, output_matrix: List[List[int]]) -> Dict[str, Any]:
    """
    Sends the output image and matrix to the oracle and asks it to analyze the output grids.

    Args:
        chat_session: The chat session object for interacting with the oracle.
        output_image (Image): The output image to be analyzed.
        output_matrix (List[List[int]]): The matrix representation of the output image.

    Returns:
        Dict[str, Any]: The analysis results including dimensions and colors.
    """
    responses = OrderedDict()
    responses["ready_for_image"] = chat_session.send_message("I am going to show you the output image. Please look at it.")
    responses["showed_image"] = chat_session.send_message(output_image)
    responses["ready_for_matrix"] = chat_session.send_message("Now I am going to show you the matrix in the form of a list of lists. The entries in the matrix correspond to the rows of the output grid. Please look at it.")
    responses["showed_matrix"] = chat_session.send_message(str(output_matrix))
    responses["output_analysis"] = chat_session.send_message("Analyze the output grid and provide the dimensions in the format (HEIGHT, WIDTH) and the color in the format of a set of digits {x, y, ...} where x, y are digits in the range [0, 9] and as found in the matrix. Reply in the following JSON format only: {\"dimensions\": (HEIGHT, WIDTH), \"color\": [x, y, ...]}")
    return responses
def extract_dimensions_and_color(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the dimensions and color from the JSON response.

    Args:
        response (Dict[str, Any]): The JSON response from the oracle.

    Returns:
        Dict[str, Any]: The extracted dimensions and color.
    """
    return {
        "dimensions": response["dimensions"],
        "color": response["color"]
    }

def find_causation(chat_session, input_dimensions: tuple, input_color: list, output_dimensions: tuple, output_color: list) -> Dict[str, Any]:
    """
    Asks the oracle to find the causation between the dimensions and colors of the input and output grids.

    Args:
        chat_session: The chat session object for interacting with the oracle.
        input_dimensions (tuple): The dimensions of the input grid.
        input_color (list): The colors of the input grid.
        output_dimensions (tuple): The dimensions of the output grid.
        output_color (list): The colors of the output grid.

    Returns:
        Dict[str, Any]: The causation results including dimension and color functions and explanations.
    """
    responses = OrderedDict()
    responses["causation_analysis"] = chat_session.send_message(f"I am sending the dimensions and color of the input grid and the output grid. Find the causation. Input dimensions: {input_dimensions}, Input color: {input_color}, Output dimensions: {output_dimensions}, Output color: {output_color}. Reply in the following JSON format only: {{\"dimension_function\" : <A python function that takes in dimensions and color of the input and returns the output dimensions.>, \"color_function\" : <A python function that takes in dimensions and color of the input and returns the output colors as set.>, \"dimension_causation\" : Explain the causation leading to the output dimensions in natural language based on the input dimensions and color., \"color_causation\" : Explain the causation leading to the output colors in natural language based on the input dimensions and color.}}")
    return responses


def create_causation_dict(input_dimensions: tuple, input_color: list, output_dimensions: tuple, output_color: list, causation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a dictionary of input and output dimensions and color and the causations derived by the oracle.

    Args:
        input_dimensions (tuple): The dimensions of the input grid.
        input_color (list): The colors of the input grid.
        output_dimensions (tuple): The dimensions of the output grid.
        output_color (list): The colors of the output grid.
        causation (Dict[str, Any]): The causation results from the oracle.

    Returns:
        Dict[str, Any]: The dictionary containing input and output dimensions, colors, and causations.
    """
    return {
        "input_dimensions": input_dimensions,
        "input_color": input_color,
        "output_dimensions": output_dimensions,
        "output_color": output_color,
        "causation": causation
    }









