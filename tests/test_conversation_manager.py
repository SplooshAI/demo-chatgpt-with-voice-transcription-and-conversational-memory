import unittest
from src.lib.conversation_manager import manage_conversation_history

class TestConversationManager(unittest.TestCase):

    def test_manage_conversation_history_less_than_max(self):
        messages = [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
        max_history = 5
        result = manage_conversation_history(messages, max_history)
        self.assertEqual(result, messages)

    def test_manage_conversation_history_equal_to_max(self):
        messages = [{'role': 'user', 'content': 'Message 1'}, {'role': 'assistant', 'content': 'Response 1'},
                    {'role': 'user', 'content': 'Message 2'}, {'role': 'assistant', 'content': 'Response 2'},
                    {'role': 'user', 'content': 'Message 3'}]
        max_history = 5
        result = manage_conversation_history(messages, max_history)
        self.assertEqual(result, messages)

    def test_manage_conversation_history_more_than_max(self):
        messages = [{'role': 'user', 'content': 'Message 1'}, {'role': 'assistant', 'content': 'Response 1'},
                    {'role': 'user', 'content': 'Message 2'}, {'role': 'assistant', 'content': 'Response 2'},
                    {'role': 'user', 'content': 'Message 3'}, {'role': 'assistant', 'content': 'Response 3'},
                    {'role': 'user', 'content': 'Message 4'}]
        max_history = 5
        expected_result = messages[-5:]
        result = manage_conversation_history(messages, max_history)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
