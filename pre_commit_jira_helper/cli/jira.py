"""CLI module for Jira issue prepend hook."""

from __future__ import annotations

from collections.abc import Sequence

from pre_commit_jira_helper.cli.base import create_parser
from pre_commit_jira_helper.hooks.jira import JiraIssuePrependHook


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point for the Jira hook CLI.

    Args:
        argv: Command line arguments.

    Returns:
        Exit code (0 for success).
    """
    parser = create_parser(
        prog="prepend-jira-issue",
        description="Prepend Jira issue(s) from branch name to commit message",
        epilog="""
Examples:
  Basic usage (extracts all Jira issues matching pattern):
    On branch 'feature/ABC-123-DEF-456-new-feature' -> 'ABC-123, DEF-456: commit message'
    prepend-jira-issue COMMIT_MSG_FILE

  Only allow specific prefixes (filters to matching prefixes only):
    On branch 'feature/ABC-123-XYZ-999-test' with --prefixes ABC,DEF -> 'ABC-123: commit message'
    prepend-jira-issue --prefixes ABC,DEF COMMIT_MSG_FILE

  With custom pattern and separator:
    prepend-jira-issue --pattern "[A-Z]{3,}-\\d+" --separator ": " COMMIT_MSG_FILE

Notes:
  - Default pattern: [A-Z][A-Z0-9_]*-\\d+ (PROJECT-NUMBER format, matches Atlassian's pattern)
  - Without --prefixes: Extracts ALL issues matching the pattern
  - With --prefixes: Extracts ONLY issues with specified prefixes
  - Multiple issues are joined with commas: "ABC-123, DEF-456: message"
  - Skips if all branch issues already exist in commit message
        """,
    )

    # Add Jira-specific arguments
    parser.add_argument(
        "--pattern",
        type=str,
        help="Custom regex pattern for issue extraction (default: [A-Z][A-Z0-9_]*-\\d+)",
    )
    parser.add_argument(
        "--separator",
        type=str,
        default=": ",
        help="Separator between issue(s) and message (default: ': ')",
    )
    parser.add_argument(
        "--prefixes",
        type=str,
        help=(
            "Comma-separated list of allowed Jira project prefixes (e.g., 'ABC,DEF,XYZ'). "
            "If not provided, ALL issues matching the pattern will be extracted."
        ),
    )

    args = parser.parse_args(argv)

    # Parse prefixes if provided
    allowed_prefixes = None
    if args.prefixes:
        allowed_prefixes = [prefix.strip().upper() for prefix in args.prefixes.split(",")]

    # Create and run the hook
    hook = JiraIssuePrependHook(
        debug=args.debug,
        issue_pattern=args.pattern,
        separator=args.separator,
        allowed_prefixes=allowed_prefixes,
    )

    return hook.run(commit_msg_filepath=args.commit_msg_filepath)


if __name__ == "__main__":
    raise SystemExit(main())
