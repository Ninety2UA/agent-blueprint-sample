"""Print a friendly greeting.

Usage: python3 scripts/greet.py [NAME]
"""

from __future__ import annotations

DEFAULT_NAME = "World"


def greet(name: str | None = None) -> str:
    """Return a greeting for name, or for DEFAULT_NAME when name is missing or blank."""
    cleaned = (name or "").strip()
    return f"Hello, {cleaned or DEFAULT_NAME}!"
