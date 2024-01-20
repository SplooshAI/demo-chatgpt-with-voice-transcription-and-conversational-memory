from .audio import record_audio
from .transcription import transcribe_audio

def get_user_input(client, whisper_model, whisper_transcribed_user_prompt_wav_path):
    user_input = input("\nType message, 'q' to quit, or press Enter to record audio: ")
    if user_input.lower() == 'q':
        return None
    elif user_input == "":
        print("\nPress 'Page Down' to start/stop recording")
        record_audio(whisper_transcribed_user_prompt_wav_path)
        return transcribe_audio(client, whisper_model, whisper_transcribed_user_prompt_wav_path)
    return user_input
