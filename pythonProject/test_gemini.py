import os
import google.generativeai as genai
from pathlib import Path
from PIL import Image

IMAGES_FOLDER = Path("./")

gemini_key_path = Path(".gemini_key")
with gemini_key_path.open('r') as file:
  gemini_key = file.read()

"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

genai.configure(api_key=gemini_key)

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="I have uploaded an image from a puzzle. You would find multiple input-output images (2-10) for Training. You would also find one or two test inputs for which output is blank (all black cells in the grid). The input images and the output images are grids of various colors, where black is assumed the absence of any color. Your job is to extract the cell and grid features as required to complete the task asked via prompt.",
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini(IMAGES_FOLDER/Path("004.png"), mime_type="image/png"),
]

chat_session = model.start_chat(
                                    history=[
                                        {
                                            "role": "user",
                                            "parts": [
                                                files[0],
                                                        ],
                                        },
                                    ]
)

second_image = Image.open(IMAGES_FOLDER/Path("total_page.jpg"))
response = chat_session.send_message("I would like you to analyze the input grids of the Training section and tell me how many training grid do you see. Next I would like you to comment on the shape or pattern of the non black cells for each grid and tell me if you find something common among all of these grids.")
print("### 1 ###" + response.text)
response2 = chat_session.send_message(second_image)
print("### 2 ###" + response2.text)
response3 = chat_session.send_message("Now Analyze this image too.")
print("### 3 ###" + response3.text)

pass