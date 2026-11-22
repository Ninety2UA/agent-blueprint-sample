import importlib.util
import unittest
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
