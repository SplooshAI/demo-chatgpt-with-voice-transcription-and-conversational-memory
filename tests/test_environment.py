import pytest
from unittest.mock import patch, mock_open
from src.lib.environment import load_environment_variables
import os

@pytest.fixture
def mock_env_files():
    # Mock content for .env.sample file
    env_sample_content = "REQUIRED_VAR1=\nREQUIRED_VAR2=\n"

    # Using mock_open to simulate file reading
    mock_file = mock_open(read_data=env_sample_content)

    with patch("builtins.open", mock_file):
        yield

def test_load_environment_variables_success(mock_env_files):
    with patch.dict(os.environ, {"REQUIRED_VAR1": "value1", "REQUIRED_VAR2": "value2"}):
        # No exit or print expected
        with patch("builtins.print") as mock_print, patch("sys.exit") as mock_exit:
            load_environment_variables("dummy/base/path")
            mock_print.assert_not_called()
            mock_exit.assert_not_called()

def test_load_environment_variables_failure(mock_env_files):
    with patch.dict(os.environ, {}, clear=True):
        with patch("builtins.print") as mock_print:
            with pytest.raises(SystemExit) as sys_exit:
                load_environment_variables("dummy/base/path")
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 1
            mock_print.assert_called()
