import importlib.util
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "greet.py"

_spec = importlib.util.spec_from_file_location("greet", SCRIPT)
greet_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(greet_module)
greet = greet_module.greet


class GreetTests(unittest.TestCase):
    def test_greets_given_name(self):
        self.assertEqual(greet("Ada"), "Hello, Ada!")

    def test_defaults_to_world(self):
        self.assertEqual(greet(), "Hello, World!")
        self.assertEqual(greet(None), "Hello, World!")

    def test_blank_name_defaults_to_world(self):
        self.assertEqual(greet(""), "Hello, World!")
        self.assertEqual(greet("   "), "Hello, World!")

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(greet("  Ada \n"), "Hello, Ada!")

    def test_keeps_inner_spaces_and_unicode(self):
        self.assertEqual(greet("Zoë Smith"), "Hello, Zoë Smith!")


class CommandLineTests(unittest.TestCase):
    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = greet_module.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_prints_greeting_for_name(self):
        self.assertEqual(self.run_main("Ada"), (0, "Hello, Ada!\n", ""))

    def test_prints_default_greeting_without_args(self):
        self.assertEqual(self.run_main(), (0, "Hello, World!\n", ""))

    def test_usage_on_too_many_arguments(self):
        self.assertEqual(
            self.run_main("Ada", "Lovelace"),
            (2, "", "usage: greet.py [NAME]\n"),
        )

    def test_runs_as_a_script(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "Ada"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Hello, Ada!\n")
