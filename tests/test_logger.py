"""Tests for logger module."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from unittest.mock import Mock

from pre_commit_jira_helper.logger import (
    LOGGER_NAME,
    disable_logging,
    enable_debug_logging,
    get_logger,
    log_to_file,
    logger,
    setup_logging,
)


class TestGetLogger:
    """Test the get_logger function."""

    def test_get_logger_without_name(self):
        """Test getting logger without specifying name."""
        result = get_logger()
        assert result.name == LOGGER_NAME

    def test_get_logger_with_name(self):
        """Test getting logger with specified name."""
        result = get_logger("test")
        assert result.name == f"{LOGGER_NAME}.test"


class TestSetupLogging:
    """Test the setup_logging function."""

    def test_setup_logging_defaults(self):
        """Test setup_logging with default parameters."""
        setup_logging()

        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert logger.handlers[0].stream == sys.stderr
        assert not logger.propagate

    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level."""
        setup_logging(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_setup_logging_custom_format(self):
        """Test setup_logging with custom format string."""
        custom_format = "%(levelname)s: %(message)s"
        setup_logging(format_string=custom_format)

        handler = logger.handlers[0]
        assert handler.formatter._fmt == custom_format

    def test_setup_logging_custom_stream(self):
        """Test setup_logging with custom stream."""
        mock_stream = Mock()
        setup_logging(stream=mock_stream)

        handler = logger.handlers[0]
        assert handler.stream == mock_stream

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup_logging clears existing handlers."""
        old_handler = logging.StreamHandler()
        logger.addHandler(old_handler)

        setup_logging()
        assert len(logger.handlers) == 1
        # Check that we have a new handler (not the old one)
        assert logger.handlers[0] != old_handler

    def test_setup_logging_string_level(self):
        """Test setup_logging with string level."""
        setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG


class TestEnableDebugLogging:
    """Test the enable_debug_logging function."""

    def test_enable_debug_logging(self):
        """Test enabling debug logging."""
        enable_debug_logging()

        assert logger.level == logging.DEBUG
        assert len(logger.handlers) == 1

        handler = logger.handlers[0]
        expected_format = (
            "[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        assert handler.formatter._fmt == expected_format


class TestDisableLogging:
    """Test the disable_logging function."""

    def test_disable_logging(self):
        """Test disabling logging."""
        setup_logging()
        assert len(logger.handlers) > 0

        disable_logging()

        assert len(logger.handlers) == 0
        assert logger.level == logging.CRITICAL + 1


class TestLogToFile:
    """Test the log_to_file function."""

    def test_log_to_file_defaults(self, mocker):
        """Test adding file handler with defaults."""
        test_file = Path("test.log")
        mock_handler = Mock()
        mock_file_handler = mocker.patch("logging.FileHandler", return_value=mock_handler)

        log_to_file(test_file)

        mock_file_handler.assert_called_once_with(test_file)
        mock_handler.setLevel.assert_called_once_with(logging.INFO)
        mock_handler.setFormatter.assert_called_once()

    def test_log_to_file_custom_level(self, mocker):
        """Test adding file handler with custom level."""
        test_file = Path("test.log")
        mock_handler = Mock()
        mocker.patch("logging.FileHandler", return_value=mock_handler)

        log_to_file(test_file, level=logging.DEBUG)

        mock_handler.setLevel.assert_called_once_with(logging.DEBUG)

    def test_log_to_file_custom_format(self, mocker):
        """Test adding file handler with custom format."""
        test_file = Path("test.log")
        custom_format = "%(message)s"
        mock_handler = Mock()
        mocker.patch("logging.FileHandler", return_value=mock_handler)

        log_to_file(test_file, format_string=custom_format)

        mock_handler.setFormatter.assert_called_once()

    def test_log_to_file_string_path(self, mocker):
        """Test adding file handler with string path."""
        test_file = "test.log"
        mock_handler = Mock()
        mock_file_handler = mocker.patch("logging.FileHandler", return_value=mock_handler)

        log_to_file(test_file)

        mock_file_handler.assert_called_once_with(test_file)
