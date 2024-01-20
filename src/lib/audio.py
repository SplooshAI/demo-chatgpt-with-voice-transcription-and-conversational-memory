import pyaudio
import wave
from pynput import keyboard

def record_audio(output_path, format=pyaudio.paInt16, channels=1, rate=10000, chunk=1024, test_mode=False, stream_reader=None):
    if test_mode:
        print("(!) EXITING EARLY: We do not actually record_audio during test mode (!)")
        open(output_path, 'wb').close()
        return

    # TODO: Testing audio hardware and keyboard interaction is something that is not going to be addressed in this reference code
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
                frame_data = (stream_reader(stream, chunk) if stream_reader else stream.read(chunk, exception_on_overflow=False))
                frames.append(frame_data)

    stream.stop_stream()
    stream.close()

    save_audio(frames, p, output_path, format, channels, rate)

def save_audio(frames, pyaudio_instance, file_path, format, channels, rate):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio_instance.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
