# Locked Decisions

_Decisions the user has settled. Planners and plan checkers read this file and follow what it locks; a plan that needs to break a decision raises the conflict instead of working around it. The ab-discuss skill appends one section per topic, with the decisions and why, the non-goals and the open questions. You can add a section by hand in the same shape. Change a decision here only when the user changes it._

## `tally chars` command (2026-11-04, ab-ship-pipeline, unattended assumptions)

Recorded without asking: the run was unattended, so each choice below is the conservative default.

**Decisions**

- `tally chars FILE` prints the number of characters in FILE followed by a newline, exits 0, and shares the existing argument check (exit 2 with usage) and missing-file check (exit 1, `tally: no such file: FILE`) with `words` and `lines`.
- A character is a Unicode code point of the file decoded as UTF-8, the way `words` and `lines` already read it (`Path.read_text(encoding="utf-8")` in `tally/__init__.py:run`). Whitespace and newlines count. Not bytes, not grapheme clusters.
- Because `read_text` uses universal newlines, a Windows line ending `\r\n` counts as one character, consistent with how `lines` sees the same file.
- The counting function is `count_chars(text: str) -> int` in `tally/__init__.py`, next to `count_words` and `count_lines`; `"chars"` joins `COMMANDS` and the usage line becomes `usage: tally (words|lines|chars) FILE`.
- The existing test `test_usage_on_bad_arguments` used `chars` as its example of an unknown command; it switches to another unknown name (`bytes`) so it keeps testing the usage path. No test is deleted or skipped.
- The README gets the command; no new dependency, no change to `pyproject.toml`.

**Non-goals**

- A byte count (`wc -c`), grapheme counting, or options such as reading stdin or several files.
- Changing how non-UTF-8 files are handled (all commands raise today; unchanged).
