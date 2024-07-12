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
import dspy
from connectors.dspy_LMs.claude_chat import ClaudeChat

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


class TestDSPy(unittest.TestCase):
    def setUp(self):
        # Set up Anthropic model
        self.claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
        self.claude_chat = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

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

    def test_initialization_anthropic(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='', model=self.claude)
        self.assertIsNotNone(dspy_instance)
        self.assertEqual(dspy_instance.strategy_method, 'one_shot')
        self.assertEqual(dspy_instance.system_info, '')

    def test_send_message_one_shot_anthropic(self):
        dspy_instance = DSPy(strategy_method='one_shot', system_info='', model=self.claude)
        response = dspy_instance.send_message(question = "What is the capital of France?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response.answer, str)

    def test_chat_strategy_anthropic(self):
        dspy_instance = DSPy(strategy_method='chat', system_info='', chat_model=self.claude_chat)
        response1 = dspy_instance.send_message("My name is Dr. Seuss. I am a cartoonist and creator of Grinch. ")
        self.assertIsNotNone(response1)
        self.assertIsInstance(response1, str)
        response2 = dspy_instance.send_message("Name one character created by me that I mentioned in the previous message.")
        self.assertIsNotNone(response2)
        self.assertIsInstance(response2, str)
        self.assertIn("Grinch", response2)


if __name__ == '__main__':
    unittest.main()