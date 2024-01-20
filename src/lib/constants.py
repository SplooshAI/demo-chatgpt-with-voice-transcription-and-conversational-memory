import os

# Application constants
APPLICATION_NAME = "Explore ChatGPT: The command-line edition"
CHATGPT_MODEL = "gpt-4-1106-preview"
WHISPER_MODEL = "whisper-1"
WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH = os.path.join(os.path.dirname(__file__), "../data/tmp/openai_whisper_transcribed_user_prompt.wav")
MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY = 10
