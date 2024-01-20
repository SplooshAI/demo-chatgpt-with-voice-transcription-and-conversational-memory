import unittest
from unittest.mock import patch, MagicMock
from src.lib import init_gpt

class TestInitGpt(unittest.TestCase):

    @patch('src.lib.init_gpt.OpenAI')
    @patch('src.lib.init_gpt.load_environment_variables')
    @patch('src.lib.init_gpt.read_initial_prompt')
    @patch('src.lib.init_gpt.get_user_input')
    @patch('src.lib.init_gpt.communicate_with_gpt')
    @patch('src.lib.init_gpt.manage_conversation_history')
    def test_init_gpt(self, mock_manage_conversation_history, mock_communicate_with_gpt, mock_get_user_input, mock_read_initial_prompt, mock_load_env, mock_openai):
        # Setup mock behavior
        mock_read_initial_prompt.return_value = "Initial prompt"
        mock_get_user_input.side_effect = ["User input", None]  # Simulate one iteration and then exit
        mock_communicate_with_gpt.return_value = "GPT response"

        # Call the function
        init_gpt.init_gpt()

        # Check if environment variables are loaded
        mock_load_env.assert_called_once()

        # Check if initial prompt is read
        mock_read_initial_prompt.assert_called_once()

        # Check if OpenAI client is initialized
        mock_openai.assert_called_once()

        # Check if user input is handled correctly
        self.assertEqual(mock_get_user_input.call_count, 2)

        # Check if communication with GPT is happening
        mock_communicate_with_gpt.assert_called_once_with(
            mock_openai(), 
            init_gpt.CHATGPT_MODEL, 
            [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': 'Initial prompt'},
                {'role': 'user', 'content': 'User input'},
                {'role': 'assistant', 'content': 'GPT response'}  # Include the assistant's response
            ]
        )

        # Check if conversation history is managed
        mock_manage_conversation_history.assert_called_once()

if __name__ == '__main__':
    unittest.main()
