"""Tests for git module."""

from __future__ import annotations

from pre_commit_jira_helper.git import GitOperations


class TestGitOperations:
    """Test GitOperations class."""

    def test_get_current_branch_success(self, mocker):
        """Test successful branch name retrieval."""
        mocker.patch(
            "pre_commit_jira_helper.git.run_command",
            return_value=(True, "feature/ABC-123-test", ""),
        )

        result = GitOperations.get_current_branch()

        assert result == "feature/ABC-123-test"

    def test_get_current_branch_no_branch(self, mocker):
        """Test branch retrieval when in detached HEAD state."""
        mocker.patch(
            "pre_commit_jira_helper.git.run_command",
            return_value=(False, "", "fatal: ref HEAD is not a symbolic ref"),
        )

        result = GitOperations.get_current_branch()

        assert result is None

    def test_get_current_branch_empty_stdout(self, mocker):
        """Test branch retrieval with empty stdout."""
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(True, "", ""))

        result = GitOperations.get_current_branch()

        assert result is None

    def test_get_staged_files_success(self, mocker):
        """Test successful staged files retrieval."""
        files_output = "file1.py\nfile2.py\nfile3.txt"
        mocker.patch(
            "pre_commit_jira_helper.git.run_command", return_value=(True, files_output, "")
        )

        result = GitOperations.get_staged_files()

        assert result == ["file1.py", "file2.py", "file3.txt"]

    def test_get_staged_files_no_files(self, mocker):
        """Test staged files retrieval when no files are staged."""
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(False, "", ""))

        result = GitOperations.get_staged_files()

        assert result == []

    def test_get_staged_files_empty_output(self, mocker):
        """Test staged files retrieval with empty output."""
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(True, "", ""))

        result = GitOperations.get_staged_files()

        assert result == []

    def test_get_commit_hash_full(self, mocker):
        """Test getting full commit hash."""
        commit_hash = "abc123def456789012345678901234567890abcd"
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(True, commit_hash, ""))

        result = GitOperations.get_commit_hash(short=False)

        assert result == commit_hash

    def test_get_commit_hash_short(self, mocker):
        """Test getting short commit hash."""
        short_hash = "abc123d"
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(True, short_hash, ""))

        result = GitOperations.get_commit_hash(short=True)

        assert result == short_hash

    def test_get_commit_hash_failure(self, mocker):
        """Test commit hash retrieval failure."""
        mocker.patch(
            "pre_commit_jira_helper.git.run_command",
            return_value=(False, "", "fatal: not a git repository"),
        )

        result = GitOperations.get_commit_hash()

        assert result is None

    def test_get_repo_root_success(self, mocker):
        """Test successful repository root retrieval."""
        repo_root = "/home/user/project"
        mocker.patch("pre_commit_jira_helper.git.run_command", return_value=(True, repo_root, ""))

        result = GitOperations.get_repo_root()

        assert result == repo_root

    def test_get_repo_root_failure(self, mocker):
        """Test repository root retrieval failure."""
        mocker.patch(
            "pre_commit_jira_helper.git.run_command",
            return_value=(False, "", "fatal: not a git repository"),
        )

        result = GitOperations.get_repo_root()

        assert result is None
