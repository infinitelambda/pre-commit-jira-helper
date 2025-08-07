"""Git operations for pre-commit hooks."""

from __future__ import annotations

from pre_commit_jira_helper.logger import get_logger
from pre_commit_jira_helper.utils import run_command

logger = get_logger("git")


class GitOperations:
    """Handle Git-related operations."""

    @staticmethod
    def get_current_branch() -> str | None:
        """Get the current Git branch name.

        Returns:
            The branch name or None if in detached state or error.
        """
        success, stdout, _ = run_command(["git", "symbolic-ref", "--short", "HEAD"])

        if success and stdout:
            logger.debug(f"Current branch: {stdout}")
            return stdout

        logger.debug("No branch detected (possibly in detached HEAD state)")
        return None

    @staticmethod
    def get_staged_files() -> list[str]:
        """Get list of staged files.

        Returns:
            List of staged file paths.
        """
        success, stdout, _ = run_command(["git", "diff", "--cached", "--name-only"])

        if success and stdout:
            files = stdout.split("\n")
            logger.debug(f"Found {len(files)} staged files")
            return files

        return []

    @staticmethod
    def get_commit_hash(short: bool = False) -> str | None:
        """Get the current commit hash.

        Args:
            short: Return short hash if True.

        Returns:
            The commit hash or None if error.
        """
        cmd = ["git", "rev-parse"]
        if short:
            cmd.append("--short")
        cmd.append("HEAD")

        success, stdout, _ = run_command(cmd)
        return stdout if success else None

    @staticmethod
    def get_repo_root() -> str | None:
        """Get the repository root directory.

        Returns:
            The repository root path or None if not in a git repo.
        """
        success, stdout, _ = run_command(["git", "rev-parse", "--show-toplevel"])
        return stdout if success else None
