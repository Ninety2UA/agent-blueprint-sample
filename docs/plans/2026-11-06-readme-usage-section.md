# README Usage Section Implementation Plan

> **Status:** COMPLETE

> **For the executing agent:** use the ab-executing-plans skill to implement this plan task by task.

**Objective:** A reader of `README.md` learns how to run tally's two commands and sees exactly what each prints, without reading the source.

**Means:** One new `## Usage` section in `README.md`, with an example whose output was produced by running it.

**Spec:** Locked decisions in `docs/context/DECISIONS.md` § README usage section (2026-11-06).

**Architecture:** Documentation only. The CLI in `tally/__init__.py` is unchanged; the section documents its existing behavior: `main()` accepts exactly `words FILE` or `lines FILE` (`COMMANDS = ("words", "lines")`, `tally/__init__.py:10`) and writes the count followed by a newline to stdout (`tally/__init__.py:46`). The `tally` console script comes from `[project.scripts]` in `pyproject.toml`, installed by the README's existing `pip install -e .` step; `tally/__main__.py` makes `python3 -m tally` work without installing.

**Tech Stack:** Markdown; Python 3.9+ standard library (unchanged).

**Estimated tasks:** 1 task, ~10 minutes.

---

## Assumptions (unattended run, no person asked)

- The "two most common commands" are `tally words FILE` and `tally lines FILE`, the only two the CLI has.
- "Short" means: a synopsis line, one example block covering both commands with their output, and one sentence on `python3 -m tally`. Exit codes and error messages are left out.
- No automated test is added: the change alters no behavior. The examples are verified by running them, and the existing suite must stay green.

## Research summary (Stage 2a, run inline)

- **Learnings:** `docs/solutions/` holds only its README; `docs/learnings/LEARNINGS.md`, `docs/decisions/`, `docs/research/` and `docs/specs/` hold only template examples unrelated to the README. No prior art beyond the locked decisions above.
- **Framework docs:** no framework is involved; plain Markdown in a GitHub-rendered README. Use fenced blocks with a language tag (`text` for the synopsis, `console` for the example session), matching the fenced `bash` blocks the README already uses.
- **Codebase context:** must change `README.md` only (insert between the `## Install` block, which ends at line 13, and `## Tests`, line 15). Nothing imports the README except `pyproject.toml` (`readme = "README.md"`, package long description), which needs no change. Tests in `tests/test_tally.py` cover the documented behavior (`test_words_command`, `test_lines_command`) and must still pass.

---

### Task 1: Add the Usage section to the README

**Files:**
- Modify: `README.md` (insert after the `## Install` code block, before `## Tests`)
- Test: none new (documentation only); `tests/test_tally.py` must stay green

**Step 1: Confirm the example output** by running it in a scratch folder:

Run, from the repository root: `(root=$(pwd) && cd "$(mktemp -d)" && printf 'the quick brown fox\njumps over the lazy dog\n' > notes.txt && PYTHONPATH="$root" python3 -m tally words notes.txt && PYTHONPATH="$root" python3 -m tally lines notes.txt)`
→ Expected: `9` then `2`, each on its own line, exit 0.

**Step 2: Write the section** in `README.md`, in this order:
1. Heading `## Usage`.
2. A `text` fenced synopsis: `tally (words|lines) FILE` (the same string as the usage message in `tally/__init__.py:39`).
3. One sentence: `words` prints the number of whitespace-separated words in `FILE`, `lines` the number of lines (a trailing newline does not add a line), each as a bare number on stdout.
4. A `console` fenced example with `$ ` prompts: create `notes.txt` with `printf 'the quick brown fox\njumps over the lazy dog\n' > notes.txt`, then `$ tally words notes.txt` followed by output `9`, then `$ tally lines notes.txt` followed by output `2`.
5. One sentence: without installing, run the same commands as `python3 -m tally words notes.txt`.

Keep lines at or under 100 characters, as the README's existing prose does.

**Step 3: Verify the README matches the tool.** Re-run the Step 1 command and compare each number with the README.
Run: `grep -n -A20 '^## Usage' README.md` → Expected: the section sits between `## Install` and `## Tests`, and shows `9` after `tally words notes.txt` and `2` after `tally lines notes.txt`.

**Step 4: Run the project suite**
Run: `python3 -m unittest` → Expected: `OK` (6 tests), exit 0.

**Step 5: Commit** `docs(readme): add a short usage section`, with a body saying why: readers had install and test steps but no way to learn the commands without reading the source.


#### Research Notes

_Added by the ab-deepen-plan skill (five research perspectives, run inline in this session)._

- **Prior solutions:** none in `docs/solutions/`; nothing to reuse or avoid.
- **Best practices:** a usage section leads with the synopsis, then one runnable example with its real output, so a reader can copy it and check they get the same result. Mark the example as a shell session (`console` fence, `$ ` before each command, output lines without it) so readers and GitHub's highlighter tell commands from output; keep the input inline (`printf ... > notes.txt`) rather than pointing at a file the reader lacks.
- **Framework docs:** no framework involved. GitHub renders `console` fences as a shell session; `text` fences render plainly, which suits the synopsis with its `(words|lines)` grammar.
- **Codebase context:** `README.md` is also the package long description (`pyproject.toml:9`, `readme = "README.md"`), so the section shows on any package page built from it; plain Markdown keeps that safe. The usage string to match is `tally/__init__.py:39`. The count is written with `f"{...}\n"` (`tally/__init__.py:46`), so each output line is a bare integer.
- **Git history:** `README.md` has one commit on `main` (`94cde5b`). The remote branch `origin/ab/docs-readme-add-a-short-usage-section-jd08kg7b` (commit `1775bf5`) holds an earlier, unmerged run of this same request that also documents exit codes; it is not on `main` and this plan does not build on it. **Flag for the implementer:** if both branches were merged they would conflict in `README.md` at the same spot; this run's PR is independent and the reviewer should pick one.

---

## Boundaries

- **Always do:** show output produced by actually running the commands; run `python3 -m unittest` before committing; keep the change itself to `README.md`; the only other files this run touches are its own records (this plan and `docs/context/DECISIONS.md`).
- **Ask first:** any change to the CLI, its messages or exit codes; any new dependency; any change to `pyproject.toml`.
- **Never do:** edit `BACKLOG.md` (the hosted demo leaves it out of pull requests); invent output; skip the test run; push or open a pull request (the root agent publishes).

## Review Focus

1. The numbers in the example (`9`, `2`) are what tally really prints for the exact `printf` input shown (Task 1, Steps 1 and 3).
2. The `lines` count for input ending in a newline is 2, not 3: the README must not imply a trailing newline adds a line (Task 1, Step 3; pinned by `test_lines_ignores_trailing_newline`).
3. The synopsis matches the CLI's own usage string `usage: tally (words|lines) FILE` (Task 1, Step 3).
4. The example uses the installed `tally` command only after the Install section, and names `python3 -m tally` for readers who have not installed (Task 1, Step 2).
