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
    # Change the path and filename for the recorded audio
    WAVE_OUTPUT_FILENAME = os.path.join(os.path.dirname(__file__), "data/prompts/user_prompt.wav")

    frames = []
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    is_recording = False

    def on_press(key):
        nonlocal is_recording, frames
        if key == keyboard.Key.page_down and not is_recording:
            is_recording = True
            frames = []
            print('\nRecording...')
        elif key == keyboard.Key.page_down and is_recording:
            is_recording = False
            print('Recording stopped.\n\n')
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            if is_recording:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    print("IOError:", e)
            elif not listener.running:
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
    record_audio()
    # Update the file path to the new location
    wav_file_path = os.path.join(os.path.dirname(__file__), "data/prompts/user_prompt.wav")

    with open(wav_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file
        )
    return transcript.text

def voice_gpt():
    messages = [{"role": "system", "content": """
    You are a helpful assistant. 
    """}]

    # Update the path to load gpt_prompt.txt from the new directory
    gpt_prompt_path = os.path.join(os.path.dirname(__file__), 'data/prompts/gpt_prompt.txt')
    with open(gpt_prompt_path, 'r', errors="ignore") as filer:
        prompt = filer.read()

    while True:
        usermess = input("Type message, 'q' to quit, or press Enter to record audio: ")
        if usermess.lower() == 'q':
            print(f"\n🤖 Thank you for using {APPLICATION_NAME}\n")
            break
        elif usermess == "":
            print("\nPress 'Page Down' to start/stop recording")
            message = whisper()
            print(f"You asked: {message}\n--------------------------------------------------------\n")
            message = f"{message}\n{prompt}"
        else:
            message = usermess + '\n' + prompt
        prompt = ''  # Clear the input materials
        messages.append({"role": "user", "content": f"{message}"})
        response = client.chat.completions.create(
            model=CHATGPT_MODEL,
            temperature=0.75,
            messages=messages,
            stream=True,
        )
        print('ChatGPT:\n')
        for chunk in response:
            choice = chunk.choices[0]
            if choice.delta and choice.delta.content:
                # Print each chunk as it arrives
                print(choice.delta.content, end='', flush=True)
        print('\n--------------------------------------------------------\n')
        messages.append({"role": "assistant", "content": choice.delta.content})

if __name__ == "__main__":
    print(f"\n👋 Welcome to {APPLICATION_NAME}\n")
    voice_gpt()
