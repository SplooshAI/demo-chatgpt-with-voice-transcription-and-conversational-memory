import os
import unittest
from src.lib import constants

class TestConstants(unittest.TestCase):

    def test_application_name(self):
        self.assertEqual(constants.APPLICATION_NAME, "Explore ChatGPT: The command-line edition")

    def test_chatgpt_model(self):
        self.assertEqual(constants.CHATGPT_MODEL, "gpt-4-1106-preview")

    def test_whisper_model(self):
        self.assertEqual(constants.WHISPER_MODEL, "whisper-1")

    def test_whisper_transcribed_user_prompt_wav_path(self):
        expected_path = os.path.join(os.path.dirname(constants.__file__), "../data/tmp/openai_whisper_transcribed_user_prompt.wav")
        self.assertEqual(constants.WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH, expected_path)
        self.assertTrue(os.path.exists(constants.WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH))

    def test_max_conversation_history_to_retain_in_memory(self):
        self.assertEqual(constants.MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY, 10)
        self.assertIsInstance(constants.MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY, int)

if __name__ == '__main__':
    unittest.main()
