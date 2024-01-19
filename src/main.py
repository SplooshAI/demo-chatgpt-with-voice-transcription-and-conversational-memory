import os
import pyaudio
import wave
from dotenv import load_dotenv
from pynput import keyboard
from openai import OpenAI

# Application constants
APPLICATION_NAME = "Explore ChatGPT: The command-line edition"
CHATGPT_MODEL = "gpt-4-1106-preview"
WHISPER_MODEL = "whisper-1"
WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH = os.path.join(os.path.dirname(__file__), "data/prompts/user_prompt.wav")  # Constant for the audio file path
MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY = 10

# Initialize PyAudio
p = pyaudio.PyAudio()

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Check environment variables
env_sample_path = os.path.join(os.path.dirname(__file__), '.env.sample')
with open(env_sample_path, 'r') as file:
    required_env_vars = [line.split('=')[0] for line in file if line.strip() and not line.startswith('#')]
    missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_env_vars:
    print("💥 Missing environment variables ->\n\n\t", ', '.join(missing_env_vars))
    print("\nPlease define the missing environment variables in src/.env file to run this application.\n")
    exit(1)

# Initialize OpenAI client
client = OpenAI()

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 10000

    frames = []
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    is_recording = False

    def on_press(key):
        nonlocal is_recording
        if key == keyboard.Key.page_down:
            if not is_recording:
                is_recording = True
                frames.clear()
                print('\n🎙️  Recording... (Press Page Down to stop)')
            else:
                is_recording = False
                print('🚨 Recording stopped.\n')
                return False

    with keyboard.Listener(on_press=on_press) as listener:
        while is_recording or listener.running:
            if is_recording:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    print("IOError:", e)
                    break

    stream.stop_stream()
    stream.close()

    wf = wave.open(WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH, 'wb')  # Use constant here
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def whisper():
    try:
        record_audio()
        with open(WHISPER_TRANSCRIBED_USER_PROMPT_WAV_PATH, "rb") as audio_file:  # Use constant here
            transcript = client.audio.transcriptions.create(model=WHISPER_MODEL, file=audio_file)
        return transcript.text.strip()
    except Exception as e:
        print("Error during transcription:", e)
        return ""

def voice_gpt():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    gpt_prompt_path = os.path.join(os.path.dirname(__file__), 'data/prompts/gpt_prompt.txt')
    if os.path.exists(gpt_prompt_path):
        with open(gpt_prompt_path, 'r', errors="ignore") as filer:
            initial_prompt = filer.read().strip()
            if initial_prompt:
                messages.append({"role": "user", "content": initial_prompt})

    while True:
        usermess = input("Type message, 'q' to quit, or press Enter to record audio: ")
        if usermess.lower() == 'q':
            print(f"\n🤖 Thank you for using {APPLICATION_NAME}\n")
            break
        elif usermess == "":
            print("\nPress 'Page Down' to start/stop recording")
            usermess = whisper()
            if not usermess:
                continue
            print(f"You: {usermess}\n\nChatGPT: ")

        messages.append({"role": "user", "content": usermess})

        response = client.chat.completions.create(model=CHATGPT_MODEL, temperature=0.75, messages=messages, stream=True)
        full_response_content = ""
        for chunk in response:
            choice = chunk.choices[0]
            if choice.delta and choice.delta.content:
                response_content = choice.delta.content
                print(response_content, end='', flush=True)
                full_response_content += response_content

        # Print a newline
        print("\n\n")

        if full_response_content.strip():
            messages.append({"role": "assistant", "content": full_response_content.strip()})

        if len(messages) > MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY:
            messages = messages[-MAX_CONVERSATION_HISTORY_TO_RETAIN_IN_MEMORY:]

if __name__ == "__main__":
    print(f"\n👋 Welcome to {APPLICATION_NAME}\n")
    voice_gpt()
