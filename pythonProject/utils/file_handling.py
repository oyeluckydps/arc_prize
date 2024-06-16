from pathlib import Path
import json
import glob

def load_json_by_page(folder, page_number):
    """
    Loads the JSON file corresponding to the given page number.
    The file name should be in the format 'XXX_*.json' where XXX is the zero-padded page number.
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

