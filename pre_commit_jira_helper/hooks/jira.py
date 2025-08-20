"""Jira issue prepend hook implementation."""

from __future__ import annotations

import re
from pathlib import Path

from pre_commit_jira_helper.base import CommitMessageHook
from pre_commit_jira_helper.git import GitOperations
from pre_commit_jira_helper.logger import get_logger

logger = get_logger("hooks.jira")


class JiraIssuePrependHook(CommitMessageHook):
    """Hook to prepend Jira issue from branch name to commit message."""

    def __init__(
        self,
        debug: bool = False,
        issue_pattern: str | None = None,
        separator: str = ": ",
        allowed_prefixes: list[str] | None = None,
    ):
        """Initialize the Jira hook.

        Args:
            debug: Enable debug logging.
            issue_pattern: Custom regex pattern for Jira issues.
            separator: Separator between issue and message.
            allowed_prefixes: List of allowed Jira project prefixes (e.g., ['ABC', 'DEF']).
                             If provided, only issues with these prefixes will be processed.
                             If None, all issues matching the pattern will be extracted.
        """
        super().__init__(debug=debug)
        self.issue_pattern = issue_pattern or r"[A-Z][A-Z0-9_]*-\d+"
        self.separator = separator
        self.allowed_prefixes = allowed_prefixes
        self.git = GitOperations()

    def extract_jira_issues(self, content: str) -> list[str]:
        """Extract all Jira issues from content.

        Args:
            content: The text to search for Jira issues.

        Returns:
            List of valid Jira issues found.
        """
        # Find all matches using the issue pattern
        matches = re.findall(self.issue_pattern, content)

        if not matches:
            logger.debug(f"No Jira issues found in: {content[:50]}...")
            return []

        valid_issues = []

        # If no prefix filter, return all matches
        if not self.allowed_prefixes:
            valid_issues = matches
            logger.debug(f"Found {len(matches)} Jira issues (no prefix filter): {matches}")
        else:
            # Filter by allowed prefixes
            for issue in matches:
                issue_prefix = issue.split("-")[0]
                if issue_prefix in self.allowed_prefixes:
                    valid_issues.append(issue)
                    logger.debug(f"Issue {issue} prefix '{issue_prefix}' is allowed")
                else:
                    logger.debug(
                        f"Issue {issue} prefix '{issue_prefix}' not in allowed prefixes: "
                        f"{self.allowed_prefixes}"
                    )

        if valid_issues:
            logger.debug(f"Final valid issues: {valid_issues}")

        return valid_issues

    def should_run(self, commit_msg_filepath: Path | str) -> bool:
        """Check if the hook should run.

        Args:
            commit_msg_filepath: Path to the commit message file.

        Returns:
            True if hook should run, False otherwise.
        """
        # Get branch name
        branch_name = self.git.get_current_branch()
        if not branch_name:
            logger.debug("No branch name found, skipping")
            return False

        # Check for Jira issues in branch
        self.branch_issues = self.extract_jira_issues(branch_name)
        if not self.branch_issues:
            logger.debug("No valid Jira issues in branch name, skipping")
            return False

        # Read commit message
        self.commit_msg = self.read_commit_message(commit_msg_filepath)
        if not self.commit_msg:
            logger.debug("Empty commit message, skipping")
            return False

        # Check if any of the branch issues already exist in the commit message
        existing_issues = self.extract_jira_issues(self.commit_msg)
        new_issues = [issue for issue in self.branch_issues if issue not in existing_issues]

        if not new_issues:
            logger.debug(
                f"All branch issues {self.branch_issues} already exist in commit message, skipping"
            )
            return False

        # Store only the new issues that need to be added
        self.new_issues = new_issues
        return True

    def process(self, commit_msg_filepath: Path | str) -> bool:
        """Process the hook logic.

        Args:
            commit_msg_filepath: Path to the commit message file.

        Returns:
            True if processing was successful.
        """
        # Prepend all new issues to message
        issues_str = ", ".join(self.new_issues)
        new_message = f"{issues_str}{self.separator} {self.commit_msg}"
        logger.info(f"Prepending issues ({issues_str}) to commit message")

        # Write updated message
        self.write_commit_message(commit_msg_filepath, new_message)
        return True
