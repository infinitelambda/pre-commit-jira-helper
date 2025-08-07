"""Example hook implementation to demonstrate extensibility."""

from __future__ import annotations

from pathlib import Path

from pre_commit_jira_helper.base import CommitMessageHook
from pre_commit_jira_helper.logger import get_logger

logger = get_logger("hooks.example")


class ExamplePrefixHook(CommitMessageHook):
    """Example hook that adds a custom prefix to commit messages.

    This demonstrates how easy it is to create new hooks.
    """

    def __init__(self, debug: bool = False, prefix: str = "[COMMIT]"):
        """Initialize the example hook.

        Args:
            debug: Enable debug logging.
            prefix: Custom prefix to add.
        """
        super().__init__(debug=debug)
        self.prefix = prefix

    def should_run(self, commit_msg_filepath: Path | str) -> bool:
        """Check if the hook should run.

        Args:
            commit_msg_filepath: Path to the commit message file.

        Returns:
            True if hook should run, False otherwise.
        """
        # Read commit message
        self.commit_msg = self.read_commit_message(commit_msg_filepath)
        if not self.commit_msg:
            logger.debug("Empty commit message, skipping")
            return False

        # Skip merge commits
        if self.is_merge_commit(self.commit_msg):
            logger.debug("Merge commit detected, skipping")
            return False

        # Skip if prefix already exists
        if self.commit_msg.startswith(self.prefix):
            logger.debug(f"Message already has prefix: {self.prefix}, skipping")
            return False

        return True

    def process(self, commit_msg_filepath: Path | str) -> bool:
        """Process the hook logic.

        Args:
            commit_msg_filepath: Path to the commit message file.

        Returns:
            True if processing was successful.
        """
        # Add prefix to message
        new_message = f"{self.prefix} {self.commit_msg}"
        logger.info(f"Adding prefix '{self.prefix}' to commit message")

        # Write updated message
        self.write_commit_message(commit_msg_filepath, new_message)
        return True
