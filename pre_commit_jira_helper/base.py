"""Base classes for pre-commit hooks."""

from __future__ import annotations

import abc
from pathlib import Path

from pre_commit_jira_helper.logger import get_logger

logger = get_logger("base")


class BaseHook(abc.ABC):
    """Abstract base class for pre-commit hooks."""

    def __init__(self, debug: bool = False):
        """Initialize the hook.

        Args:
            debug: Enable debug logging.
        """
        self.debug = debug
        if debug:
            self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging for the hook."""
        from pre_commit_jira_helper.logger import enable_debug_logging

        enable_debug_logging()

    @abc.abstractmethod
    def should_run(self, **kwargs) -> bool:
        """Check if the hook should run.

        Returns:
            True if the hook should run, False otherwise.
        """
        ...

    @abc.abstractmethod
    def process(self, **kwargs) -> bool:
        """Process the hook logic.

        Returns:
            True if processing was successful, False otherwise.
        """
        ...

    def run(self, **kwargs) -> int:
        """Run the hook.

        Returns:
            Exit code (0 for success, non-zero for failure).
        """
        try:
            if not self.should_run(**kwargs):
                logger.debug(f"{self.__class__.__name__} skipping: conditions not met")
                return 0

            success = self.process(**kwargs)
            return 0 if success else 1

        except Exception as e:
            logger.error(f"Hook failed: {e}")
            if self.debug:
                logger.exception("Full traceback:")
            return 1


class CommitMessageHook(BaseHook):
    """Base class for commit message hooks."""

    def read_commit_message(self, filepath: Path | str) -> str:
        """Read commit message from file.

        Args:
            filepath: Path to the commit message file.

        Returns:
            The commit message without comment lines.
        """
        path = Path(filepath)
        if not path.exists():
            logger.error(f"Commit message file not found: {path}")
            return ""

        lines = []
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.startswith("#"):
                    lines.append(line)

        message = "".join(lines)
        logger.debug(f"Read commit message ({len(message)} chars)")
        return message

    def write_commit_message(self, filepath: Path | str, message: str) -> None:
        """Write commit message to file.

        Args:
            filepath: Path to the commit message file.
            message: The commit message to write.
        """
        path = Path(filepath)
        path.write_text(message, encoding="utf-8")
        logger.debug(f"Wrote commit message to {path}")

    def is_merge_commit(self, message: str) -> bool:
        """Check if the message is for a merge commit.

        Args:
            message: The commit message.

        Returns:
            True if this is a merge commit, False otherwise.
        """
        return message.startswith("Merge ")
