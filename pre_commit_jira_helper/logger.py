"""Centralized logger configuration for pre-commit hooks."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Package-wide logger name
LOGGER_NAME = "pre_commit_jira_helper"

# Get the root logger for the package
logger = logging.getLogger(LOGGER_NAME)


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Optional name for the logger. If not provided, returns the root package logger.
              If provided, creates a child logger under the package namespace.

    Returns:
        Logger instance.
    """
    if name:
        # Create child logger under package namespace
        return logging.getLogger(f"{LOGGER_NAME}.{name}")
    return logger


def setup_logging(
    level: int | str = logging.INFO,
    format_string: str | None = None,
    stream=None,
) -> None:
    """Configure logging for the entire package.

    Args:
        level: Logging level (e.g., logging.DEBUG, "DEBUG").
        format_string: Custom format string for log messages.
        stream: Output stream (default: sys.stderr).
    """
    if format_string is None:
        format_string = "[%(levelname)s] %(name)s: %(message)s"

    if stream is None:
        stream = sys.stderr

    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create and configure handler
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(format_string))

    # Configure the package logger
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


def enable_debug_logging() -> None:
    """Enable debug logging with detailed format."""
    setup_logging(
        level=logging.DEBUG,
        format_string=(
            "[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
        ),
    )


def disable_logging() -> None:
    """Disable all logging."""
    logger.handlers.clear()
    logger.setLevel(logging.CRITICAL + 1)


def log_to_file(
    filepath: Path | str,
    level: int | str = logging.INFO,
    format_string: str | None = None,
) -> None:
    """Add file logging handler.

    Args:
        filepath: Path to log file.
        level: Logging level.
        format_string: Custom format string.
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(logging.Formatter(format_string))
    file_handler.setLevel(level)

    logger.addHandler(file_handler)
