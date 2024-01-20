import pytest
from unittest.mock import Mock, patch, mock_open
from src.lib.transcription import transcribe_audio

def test_transcribe_audio_success():
    # Mock OpenAI client and its response
    mock_client = Mock()
    mock_client.audio.transcriptions.create.return_value = Mock(text="mocked transcription")

    # Call the transcribe_audio function
    with patch("builtins.open", mock_open(read_data="audio data")):
        transcription = transcribe_audio(mock_client, "mock_model", "mock_audio_path")

    # Assert that the transcription is as expected
    assert transcription == "mocked transcription"

def test_transcribe_audio_failure():
    # Mock OpenAI client to raise an exception
    mock_client = Mock()
    mocked_exception = Exception("mocked exception")
    mock_client.audio.transcriptions.create.side_effect = mocked_exception

    # Call the transcribe_audio function and expect an empty string due to the exception
    with patch("builtins.open", mock_open(read_data="audio data")):
        with patch("builtins.print") as mock_print:
            transcription = transcribe_audio(mock_client, "mock_model", "mock_audio_path")
            mock_print.assert_called_with("Error during transcription:", mocked_exception)

    # Assert that the transcription is empty
    assert transcription == ""
