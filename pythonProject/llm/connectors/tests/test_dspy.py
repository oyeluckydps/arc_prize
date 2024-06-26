import unittest
from dspy import DSPy

class TestDSPy(unittest.TestCase):
    def test_initialization(self):
        dspy_instance = DSPy(strategy_method='zero_shot', system_info='')
        self.assertIsNotNone(dspy_instance)
        self.assertEqual(dspy_instance.strategy_method, 'zero_shot')
        self.assertEqual(dspy_instance.system_info, '')

    def test_send_message_zero_shot(self):
        dspy_instance = DSPy(strategy_method='zero_shot', system_info='')
        response = dspy_instance.send_message("What is the capital of France?")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()

