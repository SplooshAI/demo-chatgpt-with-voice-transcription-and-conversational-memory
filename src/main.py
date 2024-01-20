import os
from openai import OpenAI
from lib.environment import load_environment_variables
from lib.gpt_communication import communicate_with_gpt
from lib.input_handler import get_user_input
from lib.conversation_manager import manage_conversation_history
from lib.prompt_manager import read_initial_prompt

# Application constants
APPLICATION_NAME = "Explore ChatGPT: The command-line edition"
CHATGPT_MODEL = "gpt-4-1106-preview"
WHISPER_MODEL = "whisper-1"
WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH = os.path.join(os.path.dirname(__file__), "data/tmp/openai_whisper_transcribed_user_prompt.wav")
MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY = 10

# Load environment variables
base_path = os.path.dirname(__file__)
load_environment_variables(base_path)

# Initialize OpenAI client
client = OpenAI()

def init_gpt():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    initial_prompt = read_initial_prompt(base_path)
    if initial_prompt:
        messages.append({"role": "user", "content": initial_prompt})

    while True:
        user_input = get_user_input(client, WHISPER_MODEL, WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH)
        if user_input is None:
            print(f"\n🤖 Thank you for using {APPLICATION_NAME}\n")
            break
        elif not user_input:
            continue

        print(f"You: {user_input}\n\nChatGPT: ")
        messages.append({"role": "user", "content": user_input})

        full_response_content = communicate_with_gpt(client, CHATGPT_MODEL, messages)
        print(full_response_content)
        messages.append({"role": "assistant", "content": full_response_content})

        messages = manage_conversation_history(messages, MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY)

if __name__ == "__main__":
    print(f"\n👋 Welcome to {APPLICATION_NAME}\n")
    init_gpt()
