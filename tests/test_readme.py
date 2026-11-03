import unittest
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.text = README.read_text(encoding="utf-8")

    def test_has_faq_section(self):
        self.assertIn("## FAQ", self.text)

    def test_faq_answers_questions(self):
        start = self.text.index("## FAQ")
        end = self.text.index("## ", start + 1)
        faq = self.text[start:end]
        questions = [line for line in faq.splitlines() if line.startswith("- **")]
        self.assertGreaterEqual(len(questions), 2, "FAQ should answer at least two questions")


if __name__ == "__main__":
    unittest.main()
