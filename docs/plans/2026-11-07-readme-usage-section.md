# README Usage Section Implementation Plan

> **Status:** IN PROGRESS

> **For the executing agent:** use the ab-executing-plans skill to implement this plan task by task.

**Objective:** A reader of `README.md` can see, right after installing, how to run `tally` to count the words or lines in a file, and what it prints.

**Means:** One new `## Usage` Markdown section in `README.md`; no code change.

**Spec:** the request "Add a short Usage section to the README that shows how to run the tool", with the decisions under "README Usage section" in `docs/context/DECISIONS.md`.

**Architecture:** Docs only. Every command and output shown is taken from the CLI as it behaves today, so the section documents existing behavior and changes none.

**Tech Stack:** Markdown; the CLI is Python 3.9+ standard library only.

**Estimated tasks:** 1 task, ~10 minutes

---

## Codebase context

- `pyproject.toml` `[project.scripts]` declares `tally = "tally:main"`, so `pip install -e .` (the README's Install step) puts a `tally` command on the PATH.
- `tally/__init__.py` `main()` accepts exactly two arguments, `COMMANDS = ("words", "lines")` then a file path. It prints the count and a newline to stdout and exits 0. Wrong arguments print `usage: tally (words|lines) FILE` to stderr and exit 2; a missing file prints `tally: no such file: NAME` and exits 1.
- `count_words` splits on whitespace; `count_lines` does not count a trailing newline as an extra line.
- `tally/__main__.py` makes `python3 -m tally words FILE` work without installing.
- Checked by hand on a two-line file `hello world\nsecond line here\n`: `words` prints `5`, `lines` prints `2`.

## Assumptions (rigor probes, unattended default: plan with the gap written down)

- "Short" means a few lines of prose and one or two code blocks, not a reference of every error.
- The section sits between `## Install` and `## Tests`.

---

### Task 1: Add the Usage section to the README

**Files:**
- Modify: `README.md` (insert after the `## Install` block, before `## Tests`)

**Step 1: Write the section.** Heading `## Usage`. It must show:
- the command form `tally words FILE` and `tally lines FILE`, in one fenced `bash` block;
- one worked example on a named file, with the count the tool prints for it (the output must be what the tool really prints for the example's input, so the example states or shows the input);
- the `python3 -m tally words FILE` form for running from a checkout without installing;
- one sentence saying it prints the count to standard output.
Keep the existing sections' wording unchanged and the section under about 25 lines.

**Step 2: Verify every command in the section.** From the project root, recreate the example's input and run each command the section shows with `python3 -m tally` (the sandbox has no `pip`, so the installed `tally` script cannot be run here; the script and `-m` both call `tally:main`).
Run: e.g. `printf 'hello world\nsecond line here\n' > /tmp/notes.txt && python3 -m tally words /tmp/notes.txt && python3 -m tally lines /tmp/notes.txt` → Expected: `5` then `2`, matching the README exactly.

**Step 3: Run the project suite.**
Run: `python3 -m unittest` → Expected: `OK` (6 tests), with any failure named.

**Step 4: Check the diff is docs-only.**
Run: `git diff --stat` → Expected: only `README.md` changed.

**Step 5: Commit** `docs(readme): add a short Usage section`, body saying why (the README told readers how to install and test, but not how to run the tool).

### Research Notes

_Added by the ab-deepen-plan skill (researchers followed inline; no helper tool in this session)._

- **Prior solutions:** `docs/solutions/` holds only its README, and `docs/learnings/LEARNINGS.md` and `docs/research/` have no entry about the README or CLI usage. There is nothing to reuse.
- **Best practices:** a short CLI usage section usually gives the command synopsis first, then one copy-pasteable example with its output shown apart from the command (as a `# prints 5` comment or a separate output block), so a reader can paste the command without the output. Keep the synopsis's placeholder (`FILE`) the same as the tool's own usage message.
- **Framework docs:** the setuptools `[project.scripts]` entry (`tally = "tally:main"`) makes the console script on install (https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts). `python3 -m tally` runs `tally/__main__.py` (https://docs.python.org/3/library/__main__.html#main-py-in-python-packages). Without installing, it only works when the current directory is the project root, so the README should say "from the project root".
- **Codebase:** `run()` reads files as UTF-8 (`tally/__init__.py`, `path.read_text(encoding="utf-8")`). That is not needed in a short section and stays out of scope. The tests (`tests/test_tally.py`) pin the outputs the section shows, `words` and `lines` printing the count and a newline, so no new test is needed for a docs change.
- **Git history:** `README.md`, `tally/` and `pyproject.toml` all come from the single initial commit `94cde5b`. There are no earlier refactors or conventions for README sections beyond the existing `## Install` / `## Tests` / `## License` shape: one short sentence or a fenced `bash` block under each heading.

---

## Boundaries

- **Always do:** copy commands and output from the real CLI behavior; keep the README's other sections as they are; run the suite before committing.
- **Ask first:** any change to `tally/` code, `pyproject.toml` or the CLI's behavior; adding a dependency.
- **Never do:** document options the CLI does not have; edit `BACKLOG.md`; commit secrets or run-state files under `.agent-blueprint/run/`.

## Review Focus

1. The example's printed count matches what `python3 -m tally` prints for the example's input (Task 1, Step 2).
2. The command form matches `main()`'s usage line `tally (words|lines) FILE` exactly (Task 1, Step 2).
3. The `python3 -m tally` form works from the project root (Task 1, Step 2).
4. Only `README.md` changed, and the Install and Tests sections are untouched (Task 1, Step 4).
