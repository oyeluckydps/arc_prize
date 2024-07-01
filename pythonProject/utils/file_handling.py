from typing import List
from pathlib import Path
import json

def image_folder_path(working_set: str = None, page_number: int = None) -> Path:
    """
    Constructs the path to the image folder based on the working set and page number.

    Parameters:
    - working_set (str, optional): The working set directory.
    - page_number (int, optional): The page number directory.

    Returns:
    - Path: The constructed image folder path.
    """
    image_path = Path(f'./snapshots/')
    if working_set is not None:
        image_path = image_path / working_set
        if page_number is not None:
            image_path = image_path / str(page_number)
    return image_path

def get_snapshot_images_path(working_set: str, page_number: int, grid_type: str = None, index: int = None, grid_name: str = None) -> List[Path]:
    """
    Get the paths of snapshot images based on the provided parameters.

    Parameters:
    - working_set (str): The working set directory.
    - page_number (int): The page number directory.
    - grid_type (str, optional): The grid type (e.g., 'train').
    - index (int, optional): The index (e.g., 0).
    - grid_name (str, optional): The grid name (e.g., 'pair').

    Returns:
    - List[Path]: A list of paths to the matching snapshot images.
    """
    # Get the base directory path
    base_path = image_folder_path(working_set, page_number)
    
    # Construct the search pattern
    pattern = ""
    if grid_type is not None:
        pattern += grid_type
    else:
        pattern += "*"
    
    pattern += "_"
    
    if index is not None:
        pattern += str(index)
    else:
        pattern += "*"
    
    pattern += "_"
    
    if grid_name is not None:
        pattern += grid_name
    else:
        pattern += "*"
    
    pattern += ".jpg"
    
    # Find all files matching the pattern
    matching_files = list(base_path.glob(pattern))
    
    return matching_files

def json_folder_path(working_set: str) -> Path:
    folder_path = Path(f"processed_json/")
    if working_set is not None:
        folder_path = folder_path / working_set
    return folder_path

def load_json_by_page(folder: str, page_number: int) -> dict:
    """
    Loads the JSON file corresponding to the given page number.
    The file name should be in the format 'XXX_*.json' where XXX is the zero-padded page number.

    Parameters:
    - folder (str): The folder containing the JSON files.
    - page_number (int): The page number to load.

    Returns:
    - dict: The loaded JSON data.
    """
    # Ensure the page number is zero-padded to three digits
    padded_page_number = f'{page_number:03d}'
    pattern = f"{padded_page_number}_*.json"

    # Using pathlib with glob to find the correct file
    json_file_path = None
    for file in Path(folder).glob(pattern):
        json_file_path = file
        break  # We take the first match

    print(json_file_path)
    if json_file_path:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    else:
        print(f"No file found for page number {page_number}")
        return None
