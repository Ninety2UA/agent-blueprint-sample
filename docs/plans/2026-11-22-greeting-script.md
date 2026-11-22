# Greeting Script Implementation Plan

> **Status:** IN PROGRESS

> **For the executing agent:** use the ab-executing-plans skill to implement this plan task by task (under the ship pipeline, ab-orchestrate runs it).

**Objective:** Anyone with a checkout can run `python3 scripts/greet.py [NAME]` and see a friendly greeting, `Hello, NAME!`, or `Hello, World!` when no name is given.

**Means:** A standalone, standard-library Python script in `scripts/`, outside the `tally` package.

**Spec:** Locked assumptions in `docs/context/DECISIONS.md` § "Greeting script (2026-11-22, ship pipeline, unattended assumptions)".

**Architecture:** `scripts/greet.py` holds a pure `greet()` function and a `main()` entry point that mirrors `tally/__init__.py`'s CLI shape (manual argv handling, usage on stderr, exit code 2 on bad arguments). Tests load the script by file path with `importlib`, because `scripts/` is not a package and is not installed, and also run it once as a subprocess to prove the `python3 scripts/greet.py` invocation works end to end.

**Tech Stack:** Python 3.9+ standard library only (`sys`, `importlib.util`, `subprocess`, `unittest`).

**Estimated tasks:** 3 tasks, ~30 minutes.

---

## Codebase context

- `tally/__init__.py:35-47` is the pattern to follow for `main()`: `args = list(sys.argv[1:] if argv is None else argv)`, writes through `sys.stdout.write` / `sys.stderr.write`, returns an int exit code; `if __name__ == "__main__": raise SystemExit(main())`.
- `tally/__init__.py:3` uses `from __future__ import annotations` so `list[str] | None` annotations work on Python 3.9 (`pyproject.toml` says `requires-python = ">=3.9"`). Do the same.
- `tests/test_tally.py:29-33` shows the `run_main` helper (redirect stdout/stderr into `io.StringIO`, return `(code, out, err)`). Reuse that shape.
- Tests run with `python3 -m unittest` from the repository root; discovery finds `tests/test_*.py` because `tests/__init__.py` exists. Current baseline: 6 tests, OK.
- `pyproject.toml` packages only `tally` (`[tool.setuptools] packages = ["tally"]`), so a new top-level `scripts/` folder is not packaged and needs no packaging change.
- `scripts/` does not exist yet.

## Assumptions (unanswered rigor probes, headless run)

- "Greeting script" means a runnable script that prints a greeting, not a `tally` subcommand and not an installed console entry point. Recorded in `docs/context/DECISIONS.md`.
- Exact output is `Hello, <name>!` followed by one newline.

## Boundaries

- **Always do:** write each test first and watch it fail (the ab-test-driven-development skill); run `python3 -m unittest` before each commit; keep Python 3.9 compatibility; standard library only.
- **Ask first:** adding any dependency; changing `pyproject.toml` (packaging, entry points); changing `tally/`.
- **Never do:** commit secrets; modify or delete existing tests; skip verification; use `--no-verify`; create or edit `BACKLOG.md` (demo rule).

---

### Task 1: `greet()` function

**Files:**
- Create: `scripts/greet.py`
- Create: `tests/test_greet.py`

**Step 1: Write the failing tests** in `tests/test_greet.py`. At module top, load the script by path: `SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "greet.py"`, then `importlib.util.spec_from_file_location("greet", SCRIPT)`, `module_from_spec`, `spec.loader.exec_module`, and bind `greet = module.greet`. Class `GreetTests(unittest.TestCase)`:
- `test_greets_given_name` — `greet("Ada") == "Hello, Ada!"`.
- `test_defaults_to_world` — `greet() == "Hello, World!"` and `greet(None) == "Hello, World!"`.
- `test_blank_name_defaults_to_world` — `greet("") == "Hello, World!"` and `greet("   ") == "Hello, World!"`.
- `test_strips_surrounding_whitespace` — `greet("  Ada \n") == "Hello, Ada!"`.
- `test_keeps_inner_spaces_and_unicode` — `greet("Zoë Smith") == "Hello, Zoë Smith!"`.

**Step 2: Run them to verify they fail**
Run: `python3 -m unittest tests.test_greet -v` → now: ERROR (`FileNotFoundError` / no such file `scripts/greet.py`). Expected after Step 3: 5 tests OK.

**Step 3: Implement** in `scripts/greet.py`: a module docstring giving the usage line; `from __future__ import annotations`; constant `DEFAULT_NAME = "World"`; `greet(name: str | None = None) -> str` that strips the name and falls back to `DEFAULT_NAME` when the result is empty or the name is `None`, returning `f"Hello, {name}!"`. No `main()` yet beyond what Task 2 adds.

**Step 4: Run the project suite**
Run: `python3 -m unittest` → Expected: `Ran 11 tests`, `OK` (6 existing + 5 new). Name any failure, including ones this task didn't cause.

**Step 5: Commit** `feat(scripts): add greet() for the greeting script`

#### Research Notes
- **Framework docs (Python stdlib):** the documented recipe for loading a source file by path is `spec_from_file_location(name, path)` → `module_from_spec(spec)` → `spec.loader.exec_module(module)` (https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly). The recipe also puts the module in `sys.modules`; that is optional here, since nothing imports `greet` by name. The name `greet` does not clash with a stdlib module.
- **Gotcha:** `exec_module` writes bytecode to `scripts/__pycache__/`; the root `.gitignore` already ignores `__pycache__/`, so nothing extra is needed.
- **Gotcha:** while `scripts/greet.py` is missing (Step 2), the module-level load raises `FileNotFoundError` and unittest reports the module as failing to import (`ImportError`/`FileNotFoundError` in the output) rather than 5 failed tests. That is the expected failure.
- **Learnings:** no prior art in `docs/solutions/`, `docs/learnings/`, `docs/decisions/` or `docs/research/` (only scaffold examples). `docs/context/CONVENTIONS.md` is the unfilled template; its "One-off scripts in `scripts/`" and `snake_case.py` lines are the only applicable conventions.

### Task 2: Command-line entry point

Depends on Task 1 (same files).

**Files:**
- Modify: `scripts/greet.py`
- Modify: `tests/test_greet.py`

**Step 1: Write the failing tests** in `tests/test_greet.py`, class `CommandLineTests(unittest.TestCase)`, with a `run_main(*args)` helper shaped like `tests/test_tally.py:29-33` that calls the loaded module's `main(list(args))`:
- `test_prints_greeting_for_name` — `run_main("Ada")` returns `(0, "Hello, Ada!\n", "")`.
- `test_prints_default_greeting_without_args` — `run_main()` returns `(0, "Hello, World!\n", "")`.
- `test_usage_on_too_many_arguments` — `run_main("Ada", "Lovelace")` returns code `2`, empty stdout, and stderr equal to `"usage: greet.py [NAME]\n"`.
- `test_runs_as_a_script` — `subprocess.run([sys.executable, str(SCRIPT), "Ada"], capture_output=True, text=True, check=False)` has `returncode == 0` and `stdout == "Hello, Ada!\n"`. (Proves the `if __name__ == "__main__"` wiring.)

**Step 2: Run them to verify they fail**
Run: `python3 -m unittest tests.test_greet -v` → now: 4 errors (`AttributeError: module 'greet' has no attribute 'main'`; the subprocess test fails with empty stdout). Expected after Step 3: 9 tests OK.

**Step 3: Implement** `main(argv: list[str] | None = None) -> int` in `scripts/greet.py`: `args = list(sys.argv[1:] if argv is None else argv)`; more than one arg → `sys.stderr.write("usage: greet.py [NAME]\n")`, return `2`; otherwise write `greet(args[0] if args else None) + "\n"` to `sys.stdout`, return `0`. Add `if __name__ == "__main__": raise SystemExit(main())`.

**Step 4: Run the project suite and the script**
Run: `python3 -m unittest` → Expected: `Ran 15 tests`, `OK`.
Run: `python3 scripts/greet.py` → Expected: `Hello, World!`. Run: `python3 scripts/greet.py Ada` → Expected: `Hello, Ada!`. Run: `python3 scripts/greet.py a b; echo $?` → Expected: usage line on stderr, `2`.

**Step 5: Commit** `feat(scripts): add greet.py command-line entry point`

#### Research Notes
- **Framework docs:** `subprocess.run(..., capture_output=True, text=True)` is available since Python 3.7, so it is safe for the 3.9 floor. Use `sys.executable` rather than the string `python3` so the test runs under the same interpreter as the suite.
- **Codebase:** `main()` must look up `sys.stdout`/`sys.stderr` at call time (as `tally/__init__.py:39,46` do with `sys.stderr.write`/`sys.stdout.write`), not bind them at import, or `redirect_stdout` in the `run_main` helper captures nothing.
- **Best practice:** keep the subprocess test's argument ASCII (`Ada`) so the result does not depend on the console's locale encoding; the non-ASCII case is covered in-process by Task 1.
- **Git history:** the repository has one content commit (`94cde5b`), so there are no past refactors of these files to honor.

### Task 3: README section

Independent of the code; can run after or alongside Task 2.

**Files:**
- Modify: `README.md` (insert a new `## Greeting script` section after the `## Tests` section, before `## License`)

**Step 1: Write the section**: one sentence saying the repository includes a small standalone greeting script, outside the `tally` package, plus a `bash` block showing `python3 scripts/greet.py` (prints `Hello, World!`) and `python3 scripts/greet.py Ada` (prints `Hello, Ada!`).

**Step 2: Verify**
Run: `grep -c "scripts/greet.py" README.md` → now `0`, Expected: `2` or more. Run each command shown in the section and confirm the output matches what the README says.
Run: `python3 -m unittest` → Expected: `Ran 15 tests`, `OK` (guard).

**Step 3: Commit** `docs(readme): document the greeting script`

---

## Review Focus

1. Blank or whitespace-only name falls back to `World`, not `Hello, !` — pinned by `test_blank_name_defaults_to_world` (Task 1).
2. Too many arguments exits 2 with the usage line on stderr and nothing on stdout — pinned by `test_usage_on_too_many_arguments` (Task 2).
3. The file actually runs as `python3 scripts/greet.py` (the `__main__` guard is present and correct) — pinned by `test_runs_as_a_script` (Task 2).
4. Non-ASCII names pass through unchanged — pinned by `test_keeps_inner_spaces_and_unicode` (Task 1).
