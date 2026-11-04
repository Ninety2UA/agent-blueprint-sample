# `tally chars` Command Implementation Plan

> **For the executing agent:** use the ab-executing-plans skill to implement this plan task by task.

> **Status:** IN PROGRESS

**Objective:** A user can run `tally chars FILE` and see the number of characters in FILE, the same way `tally words FILE` and `tally lines FILE` print theirs, and can find the command in the README.

**Means:** a `count_chars` function beside `count_words` and `count_lines`, dispatched from `run`, with `"chars"` added to `COMMANDS`.

**Spec:** the locked decisions in `docs/context/DECISIONS.md` § `tally chars` command.

**Architecture:** `tally/__init__.py` holds the whole tool: pure counting functions, `run(command, path)` which reads the file as UTF-8 and dispatches on the command, and `main(argv)` which validates arguments against `COMMANDS` and prints the count. The new command plugs into the same three places; argument and missing-file handling are shared, so they need no new code.

**Tech Stack:** Python 3.9+, standard library only; tests with `unittest` (`python3 -m unittest` from the project root).

**Estimated tasks:** 2 tasks, ~20 minutes. They touch different files and can run in parallel.

---

### Task 1: `count_chars` and the `chars` command

**Files:**
- Modify: `tally/__init__.py` (module docstring line 1, `COMMANDS` line 10, new `count_chars` after `count_lines` lines 18-22, `run` lines 25-32, `main` docstring line 36 and usage line 39)
- Test: `tests/test_tally.py`

Use the ab-test-driven-development skill.

**Step 1: Write the failing tests** in `tests/test_tally.py`, importing `count_chars` from `tally` alongside the existing imports:
- `CountTests.test_chars_counts_every_character`: `count_chars("ab c\n") == 5` (whitespace and newline count), `count_chars("") == 0`, and `count_chars("héllo") == 5` (code points, not UTF-8 bytes).
- `CommandLineTests.test_chars_command`: on the existing sample file (`"alpha beta\ngamma\n"`), `main(["chars", path])` returns `(0, "17\n")`.
- `CommandLineTests.test_chars_command_counts_crlf_as_one`: a file written with `write_bytes(b"a\r\nb\r\n")` gives `(0, "4\n")`, pinning the universal-newline reading that `lines` already relies on.
- `CommandLineTests.test_chars_missing_file`: `main(["chars", missing])` returns 1 with `no such file` on stderr.
- Change `test_usage_on_bad_arguments` to use `"bytes"` as the unknown command (it used `"chars"`, which becomes valid) and also assert `"chars"` appears in the usage message on stderr.

**Step 2: Run them to verify they fail**
Run: `python3 -m unittest -v` → Expected: ERROR at import (`cannot import name 'count_chars' from 'tally'`).

**Step 3: Implement**
- `count_chars(text: str) -> int` in `tally/__init__.py`, docstring `"""Return the number of characters in text, newlines and other whitespace included."""`; it returns `len(text)`.
- `COMMANDS = ("words", "lines", "chars")`.
- `run`: `if command == "chars": return count_chars(text)` before the `ValueError`.
- `main`: usage line `usage: tally (words|lines|chars) FILE\n`; docstring lists `tally chars FILE` too.
- Module docstring: `"""tally: count words, lines and characters in a text file."""`.

**Step 4: Run the project suite**
Run: `python3 -m unittest -v` → Expected: `OK`, 10 tests, with any failure named.
Run: `printf 'alpha beta\ngamma\n' > /tmp/tally-sample.txt && python3 -m tally chars /tmp/tally-sample.txt` → Expected: `17`, exit 0.

**Step 5: Commit** `feat(cli): add tally chars command`

#### Research Notes

- **Prior solutions:** `docs/solutions/` holds only its README; no earlier work on counting applies.
- **Framework (Python standard library):** `Path.read_text(encoding="utf-8")` opens the file in text mode with `newline=None`, so `\r\n` and a lone `\r` both arrive as `\n` (https://docs.python.org/3/library/functions.html#open, `newline` parameter; https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text). Checked here: bytes `a\r\nbé\n` read back as `'a\nbé\n'`, length 5. `len(str)` counts code points (https://docs.python.org/3/library/functions.html#len), which is what the locked decision asks for.
- **Gotcha, not a change:** the codec is `utf-8`, not `utf-8-sig`, so a leading byte-order mark is kept and counts as one character (bytes `EF BB BF 61 0D 62` read as `'\ufeffa\nb'`, length 4). The plan keeps the shared reading in `run`; changing the codec would alter `words` too and sits under Ask first.
- **Best practice:** `wc -m` counts characters in the current locale and `wc -c` counts bytes; `tally chars` matches `wc -m` under a UTF-8 locale except that CRLF counts as one, as decided.
- **Codebase:** the only integration points are `COMMANDS` (validated in `main`, line 38), the dispatch in `run` and the usage string; `tally/__main__.py` calls `main()` unchanged, and the `tally` console script in `pyproject.toml` points at `tally:main`, so nothing else needs editing. `test_usage_on_bad_arguments` (tests/test_tally.py) currently passes `"chars"` and would fail once the command exists, which is why Step 1 changes it.
- **Git history:** all files come from one commit (`94cde5b`); no earlier refactors or patterns to follow beyond the current code.

### Task 2: README mentions `tally chars`

**Files:**
- Modify: `README.md` (intro sentence line 3, new `## Usage` section after `## Install`)

**Step 1: Edit** the intro to say the tool counts words, lines and characters, and add a `## Usage` section after `## Install` with a bash block listing `tally words FILE`, `tally lines FILE` and `tally chars FILE`, one line each saying what it prints (characters: Unicode characters, whitespace and newlines included).

**Step 2: Verify**
Run: `grep -n "tally chars FILE" README.md` → Expected: one match inside the Usage block.
No other automated verification exists for documentation.

**Step 3: Commit** `docs(readme): document tally chars`

#### Research Notes

- **Codebase:** `README.md` has no Usage section today (sections: intro, Install, Tests, License); the new section goes between Install and Tests. The intro sentence on line 3 says "counts words and lines".
- **Git history:** several unmerged remote branches (`origin/ab/docs-readme-add-a-usage-section-*`) once added a Usage section; none is on `main`, so there is nothing to reconcile with.

---

## Boundaries

- **Always do:** write the tests first and watch them fail; run `python3 -m unittest` before each commit; keep the standard library only; keep the existing exit codes and error messages unchanged.
- **Ask first:** any new dependency or change to `pyproject.toml`; changing the behavior of `words` or `lines`; changing how non-UTF-8 files are handled.
- **Never do:** delete or skip an existing test (`test_usage_on_bad_arguments` is changed, not removed); edit `BACKLOG.md`; commit secrets; push or open a pull request.

## Assumptions (unanswered rigor probes)

- "Characters" means Unicode code points after UTF-8 decoding, not bytes (`wc -c`) or grapheme clusters; recorded in `docs/context/DECISIONS.md`.
- `\r\n` counts as one character because the file is read with universal newlines, as for `lines`.

## Review Focus

1. The sample-file count is 17: whitespace and both newlines count (`test_chars_command`).
2. Non-ASCII text counts code points, not bytes (`test_chars_counts_every_character`, `"héllo"` → 5).
3. CRLF files count `\r\n` as one character (`test_chars_command_counts_crlf_as_one`).
4. The usage path still fires for an unknown command and now names `chars` (`test_usage_on_bad_arguments` with `"bytes"`).
5. The missing-file path is shared with `chars` (`test_chars_missing_file`).
