"""Print a friendly greeting.

Usage: python3 scripts/greet.py [NAME]
"""

from __future__ import annotations

import sys

DEFAULT_NAME = "World"


def greet(name: str | None = None) -> str:
    """Return a greeting for name, or for DEFAULT_NAME when name is missing or blank."""
    cleaned = (name or "").strip()
    return f"Hello, {cleaned or DEFAULT_NAME}!"


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point: greet.py [NAME]."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) > 1:
        sys.stderr.write("usage: greet.py [NAME]\n")
        return 2
    sys.stdout.write(greet(args[0] if args else None) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
