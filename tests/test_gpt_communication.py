import pytest
from unittest.mock import Mock, patch
from src.lib.gpt_communication import communicate_with_gpt

def test_communicate_with_gpt_success():
    # Mock the OpenAI client's response
    mock_response = iter([
        Mock(choices=[Mock(delta=Mock(content="response part 1"))]),
        Mock(choices=[Mock(delta=Mock(content="response part 2"))])
    ])
    
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response

    # Call the function
    model = "test-model"
    messages = [{"role": "user", "content": "Hello, GPT!"}]
    response = communicate_with_gpt(mock_client, model, messages)

    # Check if the response is concatenated correctly
    assert response == "response part 1response part 2"

def test_communicate_with_gpt_empty_response():
    # Mock the OpenAI client's response with no content
    mock_response = iter([
        Mock(choices=[Mock(delta=Mock(content=None))])
    ])

    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response

    # Call the function
    model = "test-model"
    messages = [{"role": "user", "content": "Hello, GPT!"}]
    response = communicate_with_gpt(mock_client, model, messages)

    # Check if the response is empty
    assert response == ""
