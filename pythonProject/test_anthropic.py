import anthropic
import os
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
from utils.file_handling import load_json_by_page
from preprocess_sample_json import SingleLinePrettyPrinter

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

input_analysis_prompt = """
Please identify non-overlapping and distinct common patterns or features across the given input matrices. List any unique patterns or exceptions that do not conform to these common patterns. Ensure that the patterns are exhaustive such that if one were to remove the patterns one by one from a matrix, nothing should remain.

Provide your findings in the following JSON format:

    {
    "list_of_patterns": [
        {
        "A relevant name for first pattern identified": {
            "in which input matrices is it found?": [1, 2, ...],
            "What makes it a prominent and outstanding pattern?": "",
            "Where is the pattern to be found?": "",
            "How to uniquely identify this pattern if an input matrix is provided?": "",
            "If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?": [],
            "If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?": []
        }
        },
        {
        "A relevant name for second pattern": {
            "in which input matrices is it found?": [1, 2, ...],
            "What makes it a prominent and outstanding pattern?": "",
            "Where is the pattern to be found?": "",
            "How to uniquely identify this pattern if an input matrix is provided?": "","If the pattern is found across multiple inputs then what features of the pattern are common across these inputs?": [],
            "If the pattern is found across multiple inputs then what features of the pattern vary across these inputs?": []
        }
        }
        // Add more patterns as necessary
    ]
    }

In this list of patterns:

    Focus only on describing the physical patterns or features you observe in the matrices.
    Ensure that the patterns identified are non-overlapping, distinct, and exhaustive such that if one were to remove all identified patterns one by one from any matrix, nothing should remain.

Examples:

    If you see a background across all the input matrices, mention "background" as a single pattern.
    If you see square shapes of different sizes that can be generalized, mention "squares."
    If you observe random patterns at the same location in the matrices, mention "random pattern at the particular corner of matrix."
    """


def image_to_base64(image_path):
    # Open the image using PIL
    with Image.open(image_path) as image:
        # Create a BytesIO object to hold the image data
        buffered = BytesIO()
        # Save the image to the BytesIO object in PNG format
        image.save(buffered, format="PNG")
        # Get the byte data from the BytesIO object
        img_byte = buffered.getvalue()
        # Encode the byte data to base64
        img_base64 = base64.b64encode(img_byte)
        # Convert the base64 byte data to a string
        img_base64_str = img_base64.decode("utf-8")
    return img_base64_str

img = image_to_base64(Path("total_page.jpg"))

data = load_json_by_page(folder="./processed_json/evaluation_challenges", page_number=22)

all_input_matrices = {f"input_{ind}": pair['input'] for ind, pair in enumerate(data['train'])}

pp = SingleLinePrettyPrinter()
all_inputs_string = pp.pformat(all_input_matrices)

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": input_analysis_prompt
                },
                {
                    "type": "text",
                    "text": all_inputs_string
                }
            ]
        }
    ]
)

print(message.content[0].text)

pass
