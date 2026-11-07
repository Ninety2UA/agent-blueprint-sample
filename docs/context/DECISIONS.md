# Locked Decisions

_Decisions the user has settled. Planners and plan checkers read this file and follow what it locks; a plan that needs to break a decision raises the conflict instead of working around it. The ab-discuss skill appends one section per topic, with the decisions and why, the non-goals and the open questions. You can add a section by hand in the same shape. Change a decision here only when the user changes it._

## README Usage section (ship pipeline, 2026-11-07)

Recorded by the ab-ship-pipeline skill in an unattended run; each is a default taken without asking.

**Decisions**

- Add one `## Usage` section to `README.md`, placed after `## Install` and before `## Tests`, because a reader installs the tool before running it.
- Keep it short: the two commands the CLI accepts (`tally words FILE`, `tally lines FILE`), one example with its output, and the `python3 -m tally` form for running without installing. The commands and output come from `tally/__init__.py` (`main`, `COMMANDS`) and `pyproject.toml` (`[project.scripts] tally = "tally:main"`).
- Docs only: no change to code, tests or other files.

**Non-goals**

- No full reference of error messages or exit codes, no new options, no changes to other README sections.

**Open questions**

- None.
