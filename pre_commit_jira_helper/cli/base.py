"""Base CLI functionality for all hooks."""

from __future__ import annotations

import argparse


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to any hook CLI parser.

    Args:
        parser: ArgumentParser instance to add arguments to.
    """
    parser.add_argument(
        "commit_msg_filepath",
        type=str,
        help="Path to the commit message file (provided by Git)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )


def create_parser(
    prog: str,
    description: str,
    epilog: str | None = None,
) -> argparse.ArgumentParser:
    """Create a standardized argument parser for hooks.

    Args:
        prog: Program name.
        description: Description of the hook.
        epilog: Optional epilog with examples and notes.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    add_common_arguments(parser)
    return parser
