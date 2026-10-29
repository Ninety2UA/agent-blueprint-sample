import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tally import count_lines, count_words, main


class CountTests(unittest.TestCase):
    def test_words_splits_on_whitespace(self):
        self.assertEqual(count_words("one two\tthree\nfour"), 4)
        self.assertEqual(count_words(""), 0)

    def test_lines_ignores_trailing_newline(self):
        self.assertEqual(count_lines("a\nb\n"), 2)
        self.assertEqual(count_lines("a\nb"), 2)
        self.assertEqual(count_lines(""), 0)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.txt"
        self.path.write_text("alpha beta\ngamma\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_words_command(self):
        code, out, _ = self.run_main("words", str(self.path))
        self.assertEqual((code, out), (0, "3\n"))

    def test_lines_command(self):
        code, out, _ = self.run_main("lines", str(self.path))
        self.assertEqual((code, out), (0, "2\n"))

    def test_usage_on_bad_arguments(self):
        code, _, err = self.run_main("chars", str(self.path))
        self.assertEqual(code, 2)
        self.assertIn("usage", err)

    def test_missing_file(self):
        code, _, err = self.run_main("words", str(self.path) + ".missing")
        self.assertEqual(code, 1)
        self.assertIn("no such file", err)


if __name__ == "__main__":
    unittest.main()
