"""Tests for utils module."""

from __future__ import annotations

import subprocess
from unittest.mock import Mock

from pre_commit_jira_helper.utils import run_command


class TestRunCommand:
    """Test the run_command function."""

    def test_successful_command(self, mocker):
        """Test successful command execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""

        mock_run = mocker.patch("subprocess.run", return_value=mock_result)

        success, stdout, stderr = run_command(["echo", "test"])

        assert success is True
        assert stdout == "test output"
        assert stderr == ""
        mock_run.assert_called_once_with(
            ["echo", "test"],
            capture_output=True,
            text=True,
            check=False,
            timeout=None,
        )

    def test_failed_command(self, mocker):
        """Test failed command execution."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "command failed"

        mocker.patch("subprocess.run", return_value=mock_result)

        success, stdout, stderr = run_command(["false"])

        assert success is False
        assert stdout == ""
        assert stderr == "command failed"

    def test_command_with_timeout(self, mocker):
        """Test command execution with timeout."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = ""

        mock_run = mocker.patch("subprocess.run", return_value=mock_result)

        success, stdout, stderr = run_command(["echo", "test"], timeout=30)

        assert success is True
        mock_run.assert_called_once_with(
            ["echo", "test"],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_timeout_expired(self, mocker):
        """Test command timeout."""
        mocker.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(["sleep", "10"], 5))

        success, stdout, stderr = run_command(["sleep", "10"], timeout=5)

        assert success is False
        assert stdout == ""
        assert stderr == "Command timed out"

    def test_subprocess_error(self, mocker):
        """Test subprocess error handling."""
        mocker.patch("subprocess.run", side_effect=subprocess.SubprocessError("Process error"))

        success, stdout, stderr = run_command(["invalid-command"])

        assert success is False
        assert stdout == ""
        assert stderr == "Process error"

    def test_os_error(self, mocker):
        """Test OS error handling."""
        mocker.patch("subprocess.run", side_effect=OSError("File not found"))

        success, stdout, stderr = run_command(["nonexistent"])

        assert success is False
        assert stdout == ""
        assert stderr == "File not found"

    def test_stdout_stderr_stripped(self, mocker):
        """Test that stdout and stderr are stripped of whitespace."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "  output with spaces  \n"
        mock_result.stderr = "  error with spaces  \n"

        mocker.patch("subprocess.run", return_value=mock_result)

        success, stdout, stderr = run_command(["echo", "test"])

        assert stdout == "output with spaces"
        assert stderr == "error with spaces"
