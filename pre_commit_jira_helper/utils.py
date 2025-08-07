"""Utility functions for pre-commit hooks."""

from __future__ import annotations

import subprocess

from pre_commit_jira_helper.logger import get_logger

logger = get_logger("utils")


def run_command(command: list[str], timeout: int | None = None) -> tuple[bool, str, str]:
    """Run a command and return its output.

    Args:
        command: Command to run as a list of arguments.
        timeout: Optional timeout in seconds.

    Returns:
        Tuple of (success, stdout, stderr).
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        success = result.returncode == 0
        if not success:
            logger.debug(f"Command failed with code {result.returncode}: {result.stderr}")
        return success, result.stdout.strip(), result.stderr.strip()

    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout} seconds: {' '.join(command)}")
        return False, "", "Command timed out"

    except (subprocess.SubprocessError, OSError) as e:
        logger.error(f"Failed to run command {command}: {e}")
        return False, "", str(e)
