import pytest
from unittest.mock import Mock
from src.lib.audio import save_audio
import os
import wave

@pytest.fixture
def audio_output_path(tmp_path):
    return tmp_path / "test_audio.wav"

def test_save_audio_creates_correct_file_format(audio_output_path):
    # Create mock data to simulate recorded frames
    mock_frames = [b'test'] * 10
    mock_pyaudio_instance = Mock()
    mock_pyaudio_instance.get_sample_size.return_value = 2

    save_audio(mock_frames, mock_pyaudio_instance, str(audio_output_path), 'FORMAT', 1, 10000)

    # Verify if the file was created and is a valid wave file
    assert os.path.isfile(audio_output_path)
    with wave.open(str(audio_output_path), 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == 10000
