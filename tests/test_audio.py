import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from src.lib import audio
import pyaudio
import wave

def mock_wave_write():
    wave_write = MagicMock()
    wave_write.setnchannels.return_value = None
    wave_write.setsampwidth.return_value = None
    wave_write.setframerate.return_value = None
    wave_write.writeframes.return_value = None
    wave_write.close.return_value = None
    return wave_write

def test_save_audio_creates_file(monkeypatch):
    mock_frames = [b'test'] * 10
    mock_pyaudio_instance = Mock()
    mock_pyaudio_instance.get_sample_size.return_value = 2

    mock_wave = mock_wave_write()
    with monkeypatch.context() as m:
        m.setattr(wave, "open", mock_open())
        m.setattr("wave.open", lambda *args, **kwargs: mock_wave)
        audio.save_audio(mock_frames, mock_pyaudio_instance, 'test_output.wav', pyaudio.paInt16, 1, 10000)
        mock_wave.setnchannels.assert_called_with(1)
        mock_wave.setsampwidth.assert_called_with(2)
        mock_wave.setframerate.assert_called_with(10000)
        mock_wave.writeframes.assert_called_with(b'testtesttesttesttesttesttesttesttesttest')
        mock_wave.close.assert_called()

def test_record_audio_in_test_mode(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("builtins.open", mock_open())
        with patch("builtins.print") as mock_print:
            audio.record_audio('test_output.wav', test_mode=True)
            mock_print.assert_called_with("(!) EXITING EARLY: We do not actually record_audio during test mode (!)")
            open.assert_called_once_with('test_output.wav', 'wb')
