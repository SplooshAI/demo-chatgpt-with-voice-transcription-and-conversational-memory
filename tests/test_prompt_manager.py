import unittest
from unittest.mock import patch, mock_open
from src.lib.prompt_manager import read_initial_prompt

class TestPromptManager(unittest.TestCase):

    @patch('src.lib.prompt_manager.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Test prompt text')
    def test_read_initial_prompt_file_exists(self, mock_file, mock_exists):
        base_path = 'some/base/path'
        result = read_initial_prompt(base_path)
        self.assertEqual(result, 'Test prompt text')

    @patch('src.lib.prompt_manager.os.path.exists', return_value=False)
    def test_read_initial_prompt_file_not_exists(self, mock_exists):
        base_path = 'some/base/path'
        result = read_initial_prompt(base_path)
        self.assertEqual(result, '')

if __name__ == '__main__':
    unittest.main()
