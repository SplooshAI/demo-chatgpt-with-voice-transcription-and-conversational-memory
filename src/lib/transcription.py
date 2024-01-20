# Handles the transcription of audio using Whisper
from openai import OpenAI

def transcribe_audio(client, model, audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(model=model, file=audio_file)
        return transcript.text.strip()
    except Exception as e:
        print("Error during transcription:", e)
        return ""
