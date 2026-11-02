# Contributing to tally

Thanks for taking the time to contribute! This is a small, standard-library-only
Python project, so getting set up is quick. Python 3.9 or later is required.

## Setting up

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/Ninety2UA/agent-blueprint-sample.git
cd agent-blueprint-sample
pip install -e .
```

The install is only needed to run the `tally` command; the test suite runs from
the repository root without it.

## Running the tests

The project uses the Python standard library's `unittest` framework — no extra
dependencies are needed.

Run the full test suite from the repository root:

```bash
python3 -m unittest
```

Run with per-test output:

```bash
python3 -m unittest discover -v
```

Run a single test module:

```bash
python3 -m unittest tests.test_tally
```

Run a single test case (module, class, then method):

```bash
python3 -m unittest tests.test_tally.CountTests.test_words_splits_on_whitespace
```

### Writing tests

Tests live in `tests/` and mirror the layout of the source, one `test_<module>.py`
file per module in `tally/`. Use the `unittest.TestCase` style the existing tests
use, and test the behavior of the public functions rather than their
implementation.

## Making a change

1. Create a branch from `main` (for example `fix/short-description`).
2. Make your change, adding or updating tests to cover it.
3. Run the full test suite and make sure everything passes before committing.
4. Commit with a message in the form `type(scope): brief description`, where
   type is one of `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `style`,
   `perf` — for example `fix(tally): count an empty file as zero lines`.
5. Open a pull request against `main`.

## License

By contributing, you agree that your contributions will be licensed under the
project's MIT license (see [LICENSE](LICENSE)).
