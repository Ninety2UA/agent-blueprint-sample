import unittest
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


class ReadmeTests(unittest.TestCase):
    def test_usage_section_shows_both_commands_with_output(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("## Usage", text)
        usage = text.split("## Usage", 1)[1].split("\n## ", 1)[0]
        self.assertIn("tally words", usage)
        self.assertIn("tally lines", usage)


if __name__ == "__main__":
    unittest.main()
