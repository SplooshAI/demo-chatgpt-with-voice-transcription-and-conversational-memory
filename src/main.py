import os
from lib.audio import record_audio
from lib.environment import load_environment_variables
from lib.transcription import transcribe_audio
from lib.gpt_communication import communicate_with_gpt
from openai import OpenAI

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

    gpt_prompt_path = os.path.join(base_path, 'data/prompts/gpt_prompt.txt')
    if os.path.exists(gpt_prompt_path):
        with open(gpt_prompt_path, 'r', errors="ignore") as file:
            initial_prompt = file.read().strip()
            if initial_prompt:
                messages.append({"role": "user", "content": initial_prompt})

    while True:
        user_input = input("\nType message, 'q' to quit, or press Enter to record audio: ")
        if user_input.lower() == 'q':
            print(f"\n🤖 Thank you for using {APPLICATION_NAME}\n")
            break
        elif user_input == "":
            print("\nPress 'Page Down' to start/stop recording")
            record_audio(WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH)
            user_input = transcribe_audio(client, WHISPER_MODEL, WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH)
            if not user_input:
                continue
            print(f"You: {user_input}\n\nChatGPT: ")

        messages.append({"role": "user", "content": user_input})

        full_response_content = communicate_with_gpt(client, CHATGPT_MODEL, messages)
        print(full_response_content)

        if full_response_content:
            messages.append({"role": "assistant", "content": full_response_content})

        if len(messages) > MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY:
            messages = messages[-MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY:]

if __name__ == "__main__":
    print(f"\n👋 Welcome to {APPLICATION_NAME}\n")
    init_gpt()
