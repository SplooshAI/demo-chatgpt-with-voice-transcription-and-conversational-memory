import os
import pyaudio
import wave
from dotenv import load_dotenv
from pynput import keyboard
from openai import OpenAI

# Application constants
APPLICATION_NAME = "Explore ChatGPT: The command-line edition"

# See https://platform.openai.com/docs/models for the latest models (e.g. gpt-3.5-turbo-1106, gpt-3.5-turbo, gpt-4, etc.)
CHATGPT_MODEL = "gpt-4-1106-preview"

# See https://platform.openai.com/docs/models/whisper-1 for the latest models (e.g. whisper-1, etc.)
WHISPER_MODEL = "whisper-1"

# Conversational memory
MAX_HISTORY = 10  # Adjust this number based on your requirements

# Initialize PyAudio
p = pyaudio.PyAudio()

# Load .env file from the same directory as main.py
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Assumes OPENAI_API_KEY is available as an environment variable
client = OpenAI()

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 10000
    WAVE_OUTPUT_FILENAME = os.path.join(os.path.dirname(__file__), "data/prompts/user_prompt.wav")

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

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def whisper():
    try:
        record_audio()
        wav_file_path = os.path.join(os.path.dirname(__file__), "data/prompts/user_prompt.wav")
        with open(wav_file_path, "rb") as audio_file:
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

        if len(messages) > MAX_HISTORY:
            messages = messages[-MAX_HISTORY:]

if __name__ == "__main__":
    print(f"\n👋 Welcome to {APPLICATION_NAME}\n")
    voice_gpt()
