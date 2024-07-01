import unittest
import os, sys
import dspy
from pydantic import BaseModel, Field
from typing import List
from PIL import Image, JpegImagePlugin
from pathlib import Path

# Adjust the Python path to include the parent package
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from connectors.dspy_chat import DSPyChat

dspy.settings.configure(arbitrary_types_allowed=True)

class GridAnalysisOutput(BaseModel):
    '''
    Given the image, I want you to analyze the number of rows and columns in the grid, and the colors present in the grid as a list of human readable color names.
    '''
    num_rows: int
    num_columns: int
    colors: List[str]  # List of color strings in hexadecimal format

class ImageAnalysis(dspy.Signature):
    '''
    Given the image, I want you to analyze the number of rows and columns in the grid, and the colors present in the grid as a list of human readable color names.
    '''
    query: str = dspy.InputField(desc="The query to the image")
    analysis: GridAnalysisOutput = dspy.OutputField(desc="Number of rows and columns in the grid, and the colors present in the grid as a list of human readable color names.")
    

class TestDSPyChat(unittest.TestCase):
    def test_initialization(self):
        dspy_instance = DSPyChat()
        self.assertIsNotNone(dspy_instance)

    def test_iamge_and_text(self):
        dspy_instance = DSPyChat()
        img = Image.open(Path("./spiral.jpg"))
        response = dspy_instance.send_message(img, "What do you see in the image?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
    
    def test_iamge_and_signature(self):
        dspy_instance = DSPyChat(io_signature=ImageAnalysis)
        img = Image.open(Path("./spiral.jpg"))
        response = dspy_instance.send_message(img, query = "What do you see in the image?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response.analysis, GridAnalysisOutput)

if __name__ == '__main__':
    unittest.main()