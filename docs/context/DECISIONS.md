# Locked Decisions

_Decisions the user has settled. Planners and plan checkers read this file and follow what it locks; a plan that needs to break a decision raises the conflict instead of working around it. The ab-discuss skill appends one section per topic, with the decisions and why, the non-goals and the open questions. You can add a section by hand in the same shape. Change a decision here only when the user changes it._

## README usage section (2026-11-06)

_Locked by the ab-ship-pipeline skill in an unattended run; no person was asked. Each choice is the conservative default._

### Decisions

- **The two commands are `tally words FILE` and `tally lines FILE`.** They are the only commands the CLI has (`COMMANDS` in `tally/__init__.py`), so they are the two most common.
- **One new `## Usage` section in `README.md`, between `## Install` and `## Tests`.** Readers install, then use, then test; no other file changes.
- **The example output is real.** The section creates a two-line sample file with `printf` and shows the exact stdout each command prints for it (a bare integer and a newline), checked by running the commands before commit.
- **Keep it short.** A synopsis line, one example block with both commands and their output, and one line on running without installing (`python3 -m tally`). Exit codes and error messages stay out: the request asks for the common commands and their output.
- **No new automated test.** The change is documentation only and alters no behavior; the existing suite (`python3 -m unittest`) must still pass, and the README examples are verified by running them.

### Non-goals

- Changing the CLI, its messages or its exit codes.
- Documenting every flag or error case.

### Open questions

- None.
