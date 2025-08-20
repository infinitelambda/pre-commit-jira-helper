"""Simple tests for Jira CLI module."""

from __future__ import annotations

from unittest.mock import Mock

from pre_commit_jira_helper.cli.jira import main


class TestMain:
    """Test main function."""

    def test_main_minimal_args(self, mocker):
        """Test main with minimal arguments."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mocker.patch("pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook)

        result = main(["/tmp/commit_msg"])

        assert result == 0
        mock_hook.run.assert_called_once_with(commit_msg_filepath="/tmp/commit_msg")

    def test_main_with_debug(self, mocker):
        """Test main with debug flag."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mock_class = mocker.patch(
            "pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook
        )

        result = main(["/tmp/commit_msg", "--debug"])

        assert result == 0
        mock_class.assert_called_once_with(
            debug=True,
            issue_pattern=None,
            separator=": ",
            allowed_prefixes=None,
        )

    def test_main_with_custom_pattern(self, mocker):
        """Test main with custom pattern."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mock_class = mocker.patch(
            "pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook
        )

        result = main(["/tmp/commit_msg", "--pattern", "[A-Z]{3,}-\\d+"])

        assert result == 0
        mock_class.assert_called_once_with(
            debug=False,
            issue_pattern="[A-Z]{3,}-\\d+",
            separator=": ",
            allowed_prefixes=None,
        )

    def test_main_with_custom_separator(self, mocker):
        """Test main with custom separator."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mock_class = mocker.patch(
            "pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook
        )

        result = main(["/tmp/commit_msg", "--separator", " - "])

        assert result == 0
        mock_class.assert_called_once_with(
            debug=False,
            issue_pattern=None,
            separator=" - ",
            allowed_prefixes=None,
        )

    def test_main_with_prefixes_single(self, mocker):
        """Test main with single prefix."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mock_class = mocker.patch(
            "pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook
        )

        result = main(["/tmp/commit_msg", "--prefixes", "ABC"])

        assert result == 0
        mock_class.assert_called_once_with(
            debug=False,
            issue_pattern=None,
            separator=": ",
            allowed_prefixes=["ABC"],
        )

    def test_main_with_prefixes_multiple(self, mocker):
        """Test main with multiple prefixes."""
        mock_hook = Mock()
        mock_hook.run.return_value = 0

        mock_class = mocker.patch(
            "pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook
        )

        result = main(["/tmp/commit_msg", "--prefixes", "ABC,def,XYZ"])

        assert result == 0
        mock_class.assert_called_once_with(
            debug=False,
            issue_pattern=None,
            separator=": ",
            allowed_prefixes=["ABC", "DEF", "XYZ"],
        )

    def test_main_hook_failure(self, mocker):
        """Test main when hook returns failure."""
        mock_hook = Mock()
        mock_hook.run.return_value = 1

        mocker.patch("pre_commit_jira_helper.cli.jira.JiraIssuePrependHook", return_value=mock_hook)

        result = main(["/tmp/commit_msg"])

        assert result == 1
