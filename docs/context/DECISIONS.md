# Locked Decisions

_Decisions the user has settled. Planners and plan checkers read this file and follow what it locks; a plan that needs to break a decision raises the conflict instead of working around it. The ab-discuss skill appends one section per topic, with the decisions and why, the non-goals and the open questions. You can add a section by hand in the same shape. Change a decision here only when the user changes it._

## Greeting script (2026-11-22, ship pipeline, unattended assumptions)

Request: "Add a greeting script to the repository." Nobody could be asked, so these assumptions were locked as the conservative reading.

**Decisions**
- The script is a standalone Python file at `scripts/greet.py`, since the conventions put one-off scripts in `scripts/`. It is not part of the `tally` package and adds no console entry point to `pyproject.toml`, so the published package and its public interface stay unchanged.
- Standard library only, runs on Python 3.9 or later, the same as `tally`.
- Usage: `python3 scripts/greet.py [NAME]`. It prints `Hello, NAME!` and a newline to stdout and exits 0. With no name, or a name that is empty or only whitespace, it greets `World`. Surrounding whitespace in the name is stripped.
- More than one argument prints `usage: greet.py [NAME]` to stderr and exits 2, the same shape as `tally`'s usage error. A name with spaces is passed quoted.
- The script exposes `greet(name: str | None = None) -> str` and `main(argv: list[str] | None = None) -> int`, following `tally/__init__.py`.
- Tests go in `tests/test_greet.py` and run under the existing `python3 -m unittest`.
- `README.md` gets a short "Greeting script" section, so the script can be found.

**Non-goals**
- No localization, no time-of-day greetings, no options or flags beyond the optional name.
- No change to `tally` or its packaging.

**Open questions**
- None blocking. If the person wanted the greeting as a `tally` subcommand or an installed console script instead, that is a follow-up change.
