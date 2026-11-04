"""Tests for the README's documented sections."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


class ReadmeTests(unittest.TestCase):
    def test_readme_has_changelog_section(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("## Changelog", text)


if __name__ == "__main__":
    unittest.main()