"""tally: count words and lines in a text file."""

from __future__ import annotations

import sys
from pathlib import Path

__version__ = "0.1.0"

COMMANDS = ("words", "lines")


def count_words(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())


def count_lines(text: str) -> int:
    """Return the number of lines in text; a trailing newline does not add a line."""
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def run(command: str, path: Path) -> int:
    """Run one command on the file at path and return its count."""
    text = path.read_text(encoding="utf-8")
    if command == "words":
        return count_words(text)
    if command == "lines":
        return count_lines(text)
    raise ValueError(f"unknown command: {command}")


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point: tally words FILE, tally lines FILE."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] not in COMMANDS:
        sys.stderr.write("usage: tally (words|lines) FILE\n")
        return 2
    command, name = args
    path = Path(name)
    if not path.is_file():
        sys.stderr.write(f"tally: no such file: {name}\n")
        return 1
    sys.stdout.write(f"{run(command, path)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
