"""CLI module for the example prefix hook."""

from __future__ import annotations

from collections.abc import Sequence

from pre_commit_jira_helper.cli.base import create_parser
from pre_commit_jira_helper.hooks.example import ExamplePrefixHook


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point for the example hook CLI.

    Args:
        argv: Command line arguments.

    Returns:
        Exit code (0 for success).
    """
    parser = create_parser(
        prog="example-prefix-hook",
        description="Add a custom prefix to commit messages",
        epilog="""
Examples:
  When committing with message 'Add feature', the hook will change it to '[COMMIT] Add feature'

  With custom prefix:
  example-prefix-hook --prefix "[WIP]" COMMIT_MSG_FILE

Notes:
  - The hook skips if prefix already exists in commit message
  - Merge commits are ignored
  - You can customize the prefix with --prefix option
        """,
    )

    # Add example-specific arguments
    parser.add_argument(
        "--prefix",
        type=str,
        default="[COMMIT]",
        help="Custom prefix to add (default: '[COMMIT]')",
    )

    args = parser.parse_args(argv)

    # Create and run the hook
    hook = ExamplePrefixHook(
        debug=args.debug,
        prefix=args.prefix,
    )

    return hook.run(commit_msg_filepath=args.commit_msg_filepath)


if __name__ == "__main__":
    raise SystemExit(main())
