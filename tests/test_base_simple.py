"""Simple tests for base module."""

from __future__ import annotations

from unittest.mock import Mock

from pre_commit_jira_helper.base import BaseHook, CommitMessageHook


class ConcreteBaseHook(BaseHook):
    """Concrete implementation of BaseHook for testing."""

    def __init__(self, *args, should_run_result=True, process_result=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_run_result = should_run_result
        self.process_result = process_result

    def should_run(self, **_kwargs):
        return self.should_run_result

    def process(self, **_kwargs):
        return self.process_result


class TestBaseHook:
    """Test BaseHook class."""

    def test_init_without_debug(self):
        """Test initialization without debug mode."""
        hook = ConcreteBaseHook(debug=False)
        assert hook.debug is False

    def test_init_with_debug(self, mocker):
        """Test initialization with debug mode."""
        mock_enable = mocker.patch("pre_commit_jira_helper.logger.enable_debug_logging")
        hook = ConcreteBaseHook(debug=True)
        assert hook.debug is True
        mock_enable.assert_called_once()

    def test_run_success_should_run_true_process_true(self):
        """Test successful run when should_run=True and process=True."""
        hook = ConcreteBaseHook(should_run_result=True, process_result=True)
        result = hook.run(test_arg="value")
        assert result == 0

    def test_run_success_should_run_false(self):
        """Test run when should_run=False."""
        hook = ConcreteBaseHook(should_run_result=False, process_result=True)
        result = hook.run(test_arg="value")
        assert result == 0

    def test_run_failure_process_false(self):
        """Test run when process returns False."""
        hook = ConcreteBaseHook(should_run_result=True, process_result=False)
        result = hook.run(test_arg="value")
        assert result == 1

    def test_run_exception_without_debug(self):
        """Test run when an exception occurs without debug mode."""

        class FailingHook(BaseHook):
            def should_run(self, **_kwargs):
                return True

            def process(self, **_kwargs):
                raise ValueError("Test error")

        hook = FailingHook(debug=False)
        result = hook.run()
        assert result == 1

    def test_run_exception_with_debug(self, mocker):
        """Test run when an exception occurs with debug mode."""
        mocker.patch("pre_commit_jira_helper.logger.enable_debug_logging")

        class FailingHook(BaseHook):
            def should_run(self, **_kwargs):
                return True

            def process(self, **_kwargs):
                raise ValueError("Test error")

        hook = FailingHook(debug=True)
        result = hook.run()
        assert result == 1


class ConcreteCommitMessageHook(CommitMessageHook):
    """Concrete implementation of CommitMessageHook for testing."""

    def should_run(self, **_kwargs):
        return True

    def process(self, **_kwargs):
        return True


class TestCommitMessageHook:
    """Test CommitMessageHook class."""

    def test_read_commit_message_success(self, mocker):
        """Test successful commit message reading."""
        test_content = (
            "Initial commit\n# Please enter the commit message\n"
            "# Lines starting with '#' will be ignored"
        )

        # Mock the path's existence and open method
        mock_path = mocker.patch("pre_commit_jira_helper.base.Path")
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.open.return_value.__enter__ = Mock(
            return_value=iter(test_content.split("\n"))
        )
        mock_path_instance.open.return_value.__exit__ = Mock(return_value=None)

        hook = ConcreteCommitMessageHook()
        result = hook.read_commit_message("/tmp/commit_msg")

        assert result == "Initial commit"

    def test_read_commit_message_file_not_exists(self, mocker):
        """Test commit message reading when file doesn't exist."""
        mock_path = mocker.patch("pre_commit_jira_helper.base.Path")
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        hook = ConcreteCommitMessageHook()
        result = hook.read_commit_message("/tmp/nonexistent")

        assert result == ""

    def test_write_commit_message(self, mocker):
        """Test commit message writing."""
        mock_path_class = mocker.patch("pre_commit_jira_helper.base.Path")
        mock_path_instance = Mock()
        mock_path_class.return_value = mock_path_instance

        hook = ConcreteCommitMessageHook()
        test_message = "ABC-123: New feature implementation"
        hook.write_commit_message("/tmp/commit_msg", test_message)

        mock_path_instance.write_text.assert_called_once_with(test_message, encoding="utf-8")

    def test_is_merge_commit_true(self):
        """Test merge commit detection for merge messages."""
        hook = ConcreteCommitMessageHook()

        merge_messages = [
            "Merge branch 'feature' into main",
            "Merge pull request #123 from user/feature",
            "Merge remote-tracking branch 'origin/develop'",
        ]

        for message in merge_messages:
            assert hook.is_merge_commit(message) is True

    def test_is_merge_commit_false(self):
        """Test merge commit detection for non-merge messages."""
        hook = ConcreteCommitMessageHook()

        non_merge_messages = [
            "Initial commit",
            "ABC-123: Add new feature",
            "Fix bug in authentication module",
            "Update documentation",
        ]

        for message in non_merge_messages:
            assert hook.is_merge_commit(message) is False
