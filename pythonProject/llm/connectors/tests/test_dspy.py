import unittest
import os, sys
import dspy
from pydantic import BaseModel, Field
from typing import List
from PIL import Image, JpegImagePlugin
from pathlib import Path

# Adjust the Python path to include the parent package
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from connectors.dspy import DSPy
# from ..dspy import DSPy


# Define the Character class using Pydantic
class Character(BaseModel):
    name: str
    shade_of_character: str
    characteristic: str

# Define the Signature for the story-to-characters task
class StoryToCharacters(dspy.Signature):
    '''
    Given the story text, extract the characters with their shades and characteristics.
    '''
    story: str = dspy.InputField(desc="The story text")
    characters: List[Character] = dspy.OutputField(desc="List of characters with their shades and characteristics")

story_text = """
In the quaint village of Brookhaven, nestled by a tranquil river, three friends embodied vastly different spirits.
Rosalind, the spirited and adventurous baker, was known for her bold ideas and infectious energy,
always dreaming up new recipes and hosting lively gatherings in her cozy, pastel-colored bakery.
Contrarily, Oliver, the quiet and introspective watchmaker, spent his days meticulously crafting intricate timepieces,
his mind often lost in the precision of ticking gears and philosophical musings.
Completing the trio was Emilia, the empathetic and gentle schoolteacher,
whose nurturing nature and soothing voice calmed even the rowdiest classroom.
"""

dspy.settings.configure(arbitrary_types_allowed=True)

class GridAnalysisOutput(BaseModel):
    num_rows: int
    num_columns: int
    colors: List[str]  # List of color strings in hexadecimal format

# Define the Signature for the image to grid analysis task.
class ImageAnalysis(dspy.Signature, BaseModel):
    '''
    Given the image, I want you to analyze the number of rows and columns in the grid, and the colors present in the grid as a list of human readable color names.
    '''
    image: JpegImagePlugin.JpegImageFile = dspy.InputField(desc="The input image containing the grid.")
    analysis: GridAnalysisOutput = dspy.OutputField(desc="Number of rows and columns in the grid, and the colors present in the grid as a list of human readable color names.")
    class Config:
        arbitrary_types_allowed = True


class TestDSPy(unittest.TestCase):
    def test_initialization(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='')
        self.assertIsNotNone(dspy_instance)
        self.assertEqual(dspy_instance.strategy_method, 'one_shot')
        self.assertEqual(dspy_instance.system_info, '')

    def test_send_message_one_shot(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='')
        response = dspy_instance.send_message(question = "What is the capital of France?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response.answer, str)

    def test_chat_strategy(self):
        dspy_instance = DSPy(strategy_method='chat', system_info='')
        response1 = dspy_instance.send_message("My name is Dr. Seuss. I am a cartoonist and creator of Grinch. ")
        self.assertIsNotNone(response1)
        self.assertIsInstance(response1, str)
        
        response2 = dspy_instance.send_message("Name one character created by me that I mentioned in the previous message.")
        self.assertIsNotNone(response2)
        self.assertIsInstance(response2, str)
        self.assertIn("Grinch", response2)

    def test_direct_strategy(self):
        dspy_instance = DSPy(strategy_method='direct', system_info='')
        response = dspy_instance.send_message("What is the capital of Germany?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

    def test_one_shot_with_signature(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='', io_signature=StoryToCharacters)
        response = dspy_instance.send_message(story = story_text)
        self.assertIsNotNone(response)
        self.assertIsInstance(response.characters, list)
        self.assertEqual(len(response.characters), 3)

    def test_one_shot_with_image(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='', io_signature=ImageAnalysis)
        img = Image.open(Path("./spiral.jpg"))
        response = dspy_instance.send_message(image = img)
        self.assertIsNotNone(response)
        self.assertIsInstance(response.analysis, GridAnalysisOutput)
        self.assertEqual(response.analysis.num_rows, 11)
        self.assertEqual(response.analysis.num_columns, 11)
        self.assertEqual(len(response.analysis.colors), 4)

if __name__ == '__main__':
    unittest.main()