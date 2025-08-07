"""Pre-commit hook to prepend a Jira issue to a commit message."""

import importlib.metadata

from pre_commit_jira_helper.logger import get_logger, logger, setup_logging

try:
    __version__ = importlib.metadata.version("pre-commit-jira-helper")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__", "logger", "get_logger", "setup_logging"]
