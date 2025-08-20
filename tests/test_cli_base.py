"""Tests for CLI base module."""

from __future__ import annotations

import argparse

from pre_commit_jira_helper.cli.base import add_common_arguments, create_parser


class TestAddCommonArguments:
    """Test add_common_arguments function."""

    def test_add_common_arguments(self):
        """Test that common arguments are added correctly."""
        parser = argparse.ArgumentParser()
        add_common_arguments(parser)

        # Parse test arguments
        args = parser.parse_args(["test_commit_msg", "--debug"])

        assert args.commit_msg_filepath == "test_commit_msg"
        assert args.debug is True

    def test_add_common_arguments_no_debug(self):
        """Test common arguments without debug flag."""
        parser = argparse.ArgumentParser()
        add_common_arguments(parser)

        args = parser.parse_args(["test_commit_msg"])

        assert args.commit_msg_filepath == "test_commit_msg"
        assert args.debug is False


class TestCreateParser:
    """Test create_parser function."""

    def test_create_parser_minimal(self):
        """Test creating parser with minimal parameters."""
        parser = create_parser(prog="test-hook", description="Test hook description")

        assert parser.prog == "test-hook"
        assert parser.description == "Test hook description"
        assert parser.formatter_class == argparse.RawDescriptionHelpFormatter
        assert parser.epilog is None

    def test_create_parser_with_epilog(self):
        """Test creating parser with epilog."""
        epilog_text = "This is example usage"
        parser = create_parser(
            prog="test-hook", description="Test hook description", epilog=epilog_text
        )

        assert parser.epilog == epilog_text

    def test_create_parser_includes_common_arguments(self):
        """Test that created parser includes common arguments."""
        parser = create_parser(prog="test-hook", description="Test hook description")

        # Test that the parser can parse common arguments
        args = parser.parse_args(["test_commit_msg", "--debug"])

        assert args.commit_msg_filepath == "test_commit_msg"
        assert args.debug is True
