import unittest
import os, sys

# Adjust the Python path to include the parent package
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from connectors.dspy import DSPy
# from ..dspy import DSPy

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

if __name__ == '__main__':
    unittest.main()