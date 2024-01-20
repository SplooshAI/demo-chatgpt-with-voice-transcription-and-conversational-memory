# This module handles audio recording and processing tasks.
import pyaudio
import wave
from pynput import keyboard

def record_audio(output_path, format=pyaudio.paInt16, channels=1, rate=10000, chunk=1024, test_mode=False):
    # TODO: Find a way to test this in earnest. For now, if we are in test mode, exit the function early
    if test_mode:
        print("(!) EXITING EARLY: We do not actually record_audio during test mode (!)")
        # Create an empty file to simulate the output
        open(output_path, 'wb').close()
        return
    
    p = pyaudio.PyAudio()
    frames = []
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
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
                    data = stream.read(chunk, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    print("IOError:", e)
                    break

    stream.stop_stream()
    stream.close()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
