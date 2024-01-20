import unittest
from unittest.mock import patch, MagicMock
from src.lib.input_handler import get_user_input

class TestInputHandler(unittest.TestCase):

    @patch('src.lib.input_handler.input', return_value='Hello')
    def test_get_user_input_text(self, mocked_input):
        client = MagicMock()
        result = get_user_input(client, 'whisper_model', 'path')
        self.assertEqual(result, 'Hello')

    @patch('src.lib.input_handler.input', return_value='q')
    def test_get_user_input_quit(self, mocked_input):
        client = MagicMock()
        result = get_user_input(client, 'whisper_model', 'path')
        self.assertIsNone(result)

    @patch('src.lib.input_handler.input', return_value='')
    @patch('src.lib.input_handler.record_audio')
    @patch('src.lib.input_handler.transcribe_audio', return_value='Transcribed text')
    def test_get_user_input_audio(self, mocked_transcribe_audio, mocked_record_audio, mocked_input):
        client = MagicMock()
        result = get_user_input(client, 'whisper_model', 'path')
        mocked_record_audio.assert_called_once_with('path')
        mocked_transcribe_audio.assert_called_once_with(client, 'whisper_model', 'path')
        self.assertEqual(result, 'Transcribed text')

if __name__ == '__main__':
    unittest.main()
