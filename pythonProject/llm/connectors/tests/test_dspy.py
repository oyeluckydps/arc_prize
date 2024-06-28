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
        print(response)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()


