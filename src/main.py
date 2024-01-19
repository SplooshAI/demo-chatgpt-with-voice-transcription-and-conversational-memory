# src/main.py
import os
import pyaudio
import wave
from dotenv import load_dotenv
from pynput import keyboard
import time
from openai import OpenAI
import re

# Initialize PyAudio
p = pyaudio.PyAudio()

# Print the list of available audio devices
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

# Load .env file from the same directory as main.py
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Assumes OPENAI_API_KEY is available as an environment variable
client = OpenAI()

def record_audio(duration=None):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 10000

    # Adjust the path to save user_response.wav in the src directory
    WAVE_OUTPUT_FILENAME = os.path.join(os.path.dirname(__file__), "user_response.wav")

    frames = []
    stream = None
    is_recording = False
    recording_stopped = False

    def start_recording():
        nonlocal stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    def stop_recording():
        nonlocal frames, stream, recording_stopped
        stream.stop_stream()
        stream.close()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        recording_stopped = True

    def on_key(key):
        nonlocal is_recording, frames
        if key == keyboard.Key.page_down:
            if not is_recording:
                print('Recording...')
                start_recording()
                is_recording = True
            else:
                stop_recording()
                is_recording = False
                print('Recording stopped.')
            frames = []

    listener = keyboard.Listener(on_press=on_key)
    listener.start()
    start_time = time.time()

    while listener.running:
        if is_recording:
            data = stream.read(CHUNK)
            frames.append(data)
        if recording_stopped:
            listener.stop()
        elif duration and (time.time() - start_time) > duration:
            listener.stop()
        time.sleep(0.01)

# This opens up the file, streams it to the Whisper API, and outputs the raw transcript string.
def whisper():
    record_audio()
    # Correctly adjust the path to the 'user_response.wav' file
    wav_file_path = os.path.join(os.path.dirname(__file__), "user_response.wav")
    with open(wav_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def voice_gpt():
    messages = [{"role": "system", "content": """
    You are a helpful assistant. 
    """}]

    # Adjust the path to load gpt_prompt.txt from the src directory
    gpt_prompt_path = os.path.join(os.path.dirname(__file__), 'gpt_prompt.txt')
    with open(gpt_prompt_path, 'r', errors="ignore") as filer:
        prompt = filer.read()

    while True:
        usermess = input("Type message or press Enter to record audio: ")
        if usermess == "":
            print("Press 'Page Down' to start/stop recording")
            message = whisper()
            print(f"{message}")
            message = f"{message}\n{prompt}"
        else:
            message = usermess + '\n' + prompt
        prompt = ''  # Clear the input materials
        messages.append({"role": "user", "content": f"{message}"})
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0.75,
            messages=messages,
            stream=True,
        )
        answer_accumulator = ''
        print('--------------------------------------------------------\nChatGPT:')
        for chunk in response:
            choice = chunk.choices[0]
            if choice.delta and choice.delta.content:
                answer = choice.delta.content.replace('\n', ' ')
                answer_accumulator += answer
                print(answer, end='', flush=True)
        print('\n--------------------------------------------------------')
        messages.append({"role": "assistant", "content": f"{answer_accumulator}"})


if __name__ == "__main__":
    voice_gpt()
