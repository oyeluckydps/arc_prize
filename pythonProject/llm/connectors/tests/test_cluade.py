import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust the Python path to include the parent package
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from connectors.claude import Claude

class TestClaude(unittest.TestCase):

    def setUp(self):
        self.claude = Claude("chat", system_info="You are a helpful assistant.")

    @patch('anthropic.Anthropic')
    def test_initialize_claude(self, mock_anthropic):
        claude = Claude("chat")
        mock_anthropic.assert_called_once()
        self.assertIsNotNone(claude.client)

    def test_chat_history(self):
        self.assertEqual(self.claude.chat_history(), [])

    def test_clear_chat(self):
        self.claude._Claude__chat_history = [{"role": "user", "content": "Hello"}]
        self.claude.clear_chat()
        self.assertEqual(self.claude.chat_history(), [])

    @patch('anthropic.Anthropic')
    def test_one_shot_single_message(self, mock_anthropic):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello, how can I help you?")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        self.claude.initialize_claude()  # Reinitialize with mocked client
        response = self.claude.one_shot("Hi")
        self.assertEqual(response, "Hello, how can I help you?")
        mock_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_one_shot_multiple_messages(self, mock_anthropic):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Responses to your questions")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        self.claude.initialize_claude()  # Reinitialize with mocked client
        response = self.claude.one_shot(["Question 1", "Question 2"])
        self.assertEqual(response, "Responses to your questions")
        mock_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_chat_single_message(self, mock_anthropic):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Sure, I can help with that.")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        self.claude.initialize_claude()  # Reinitialize with mocked client
        response = self.claude.chat("Can you help me?")
        self.assertEqual(response, "Sure, I can help with that.")
        self.assertEqual(len(self.claude.chat_history()), 2)  # User message + Assistant response
        mock_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_chat_multiple_messages(self, mock_anthropic):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Responses to your questions")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        self.claude.initialize_claude()  # Reinitialize with mocked client
        response = self.claude.chat(["Question 1", "Question 2"])
        self.assertEqual(response, "Responses to your questions")
        self.assertEqual(len(self.claude.chat_history()), 3)  # Two user messages + Assistant response
        mock_client.messages.create.assert_called_once()

    def test_invalid_message_type(self):
        with self.assertRaises(ValueError):
            self.claude.one_shot(123)

        with self.assertRaises(ValueError):
            self.claude.chat(123)

if __name__ == '__main__':
    unittest.main()