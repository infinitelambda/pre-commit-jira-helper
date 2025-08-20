"""Simple tests for Jira hook implementation."""

from __future__ import annotations

from pre_commit_jira_helper.hooks.jira import JiraIssuePrependHook


class TestJiraIssuePrependHook:
    """Test JiraIssuePrependHook class."""

    def test_init_defaults(self):
        """Test initialization with default parameters."""
        hook = JiraIssuePrependHook()

        assert hook.debug is False
        assert hook.issue_pattern == r"[A-Z][A-Z0-9_]*-\d+"
        assert hook.separator == ": "
        assert hook.allowed_prefixes is None

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        hook = JiraIssuePrependHook(
            debug=True,
            issue_pattern=r"[A-Z]{3,}-\d+",
            separator=" - ",
            allowed_prefixes=["ABC", "DEF"],
        )

        assert hook.debug is True
        assert hook.issue_pattern == r"[A-Z]{3,}-\d+"
        assert hook.separator == " - "
        assert hook.allowed_prefixes == ["ABC", "DEF"]

    def test_extract_jira_issues_no_matches(self):
        """Test extracting Jira issues when none found."""
        hook = JiraIssuePrependHook()
        result = hook.extract_jira_issues("feature/no-issues-here")
        assert result == []

    def test_extract_jira_issues_with_matches_no_filter(self):
        """Test extracting Jira issues without prefix filter."""
        hook = JiraIssuePrependHook()
        result = hook.extract_jira_issues("feature/ABC-123-DEF-456-test")
        assert result == ["ABC-123", "DEF-456"]

    def test_extract_jira_issues_with_prefix_filter_allowed(self):
        """Test extracting Jira issues with prefix filter - allowed prefixes."""
        hook = JiraIssuePrependHook(allowed_prefixes=["ABC", "XYZ"])
        result = hook.extract_jira_issues("feature/ABC-123-DEF-456-XYZ-789")
        assert result == ["ABC-123", "XYZ-789"]

    def test_extract_jira_issues_with_prefix_filter_none_allowed(self):
        """Test extracting Jira issues with prefix filter - no allowed prefixes."""
        hook = JiraIssuePrependHook(allowed_prefixes=["ABC"])
        result = hook.extract_jira_issues("feature/DEF-456-XYZ-789")
        assert result == []

    def test_extract_jira_issues_custom_pattern(self):
        """Test extracting Jira issues with custom pattern."""
        hook = JiraIssuePrependHook(issue_pattern=r"[A-Z]{3,}-\d+")
        result = hook.extract_jira_issues("feature/ABC-123-ABCD-456")
        # Both ABC-123 and ABCD-456 match the pattern [A-Z]{3,}-\d+ (3 or more letters)
        # ABC has 3 letters, ABCD has 4 letters, so both should match
        assert result == ["ABC-123", "ABCD-456"]

    def test_should_run_no_branch(self, mocker):
        """Test should_run when no branch is detected."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value=None)

        result = hook.should_run("/tmp/commit_msg")

        assert result is False

    def test_should_run_no_issues_in_branch(self, mocker):
        """Test should_run when no Jira issues in branch name."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value="feature/no-issues")

        result = hook.should_run("/tmp/commit_msg")

        assert result is False

    def test_should_run_empty_commit_message(self, mocker):
        """Test should_run when commit message is empty."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value="feature/ABC-123")
        mocker.patch.object(hook, "read_commit_message", return_value="")

        result = hook.should_run("/tmp/commit_msg")

        assert result is False

    def test_should_run_issues_already_exist(self, mocker):
        """Test should_run when all branch issues already exist in commit message."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value="feature/ABC-123")
        mocker.patch.object(hook, "read_commit_message", return_value="ABC-123: Initial commit")

        result = hook.should_run("/tmp/commit_msg")

        assert result is False

    def test_should_run_success_new_issues(self, mocker):
        """Test should_run when there are new issues to add."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value="feature/ABC-123-DEF-456")
        mocker.patch.object(hook, "read_commit_message", return_value="ABC-123: Initial commit")

        result = hook.should_run("/tmp/commit_msg")

        assert result is True
        assert hook.new_issues == ["DEF-456"]

    def test_should_run_success_all_new_issues(self, mocker):
        """Test should_run when all issues are new."""
        hook = JiraIssuePrependHook()
        mocker.patch.object(hook.git, "get_current_branch", return_value="feature/ABC-123-DEF-456")
        mocker.patch.object(hook, "read_commit_message", return_value="Initial commit")

        result = hook.should_run("/tmp/commit_msg")

        assert result is True
        assert hook.new_issues == ["ABC-123", "DEF-456"]

    def test_process_single_issue(self, mocker):
        """Test process method with single new issue."""
        hook = JiraIssuePrependHook()
        hook.new_issues = ["ABC-123"]
        hook.commit_msg = "Initial commit"

        mock_write = mocker.patch.object(hook, "write_commit_message")
        result = hook.process("/tmp/commit_msg")

        assert result is True
        mock_write.assert_called_once_with("/tmp/commit_msg", "ABC-123:  Initial commit")

    def test_process_multiple_issues(self, mocker):
        """Test process method with multiple new issues."""
        hook = JiraIssuePrependHook()
        hook.new_issues = ["ABC-123", "DEF-456"]
        hook.commit_msg = "Initial commit"

        mock_write = mocker.patch.object(hook, "write_commit_message")
        result = hook.process("/tmp/commit_msg")

        assert result is True
        mock_write.assert_called_once_with("/tmp/commit_msg", "ABC-123, DEF-456:  Initial commit")

    def test_process_custom_separator(self, mocker):
        """Test process method with custom separator."""
        hook = JiraIssuePrependHook(separator=" - ")
        hook.new_issues = ["ABC-123"]
        hook.commit_msg = "Initial commit"

        mock_write = mocker.patch.object(hook, "write_commit_message")
        result = hook.process("/tmp/commit_msg")

        assert result is True
        mock_write.assert_called_once_with("/tmp/commit_msg", "ABC-123 -  Initial commit")
