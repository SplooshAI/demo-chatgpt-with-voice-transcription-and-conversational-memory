import os
from openai import OpenAI
from .environment import load_environment_variables
from .gpt_communication import communicate_with_gpt
from .input_handler import get_user_input
from .conversation_manager import manage_conversation_history
from .prompt_manager import read_initial_prompt
from .constants import APPLICATION_NAME, CHATGPT_MODEL, WHISPER_MODEL, WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH, MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY

def init_gpt():
    # Load environment variables
    base_path = os.path.join(os.path.dirname(__file__), '..')
    load_environment_variables(base_path)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    initial_prompt = read_initial_prompt(base_path)
    if initial_prompt:
        messages.append({"role": "user", "content": initial_prompt})

    client = OpenAI()

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
        messages.append({"role": "assistant", "content": full_response_content})

        messages = manage_conversation_history(messages, MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY)
