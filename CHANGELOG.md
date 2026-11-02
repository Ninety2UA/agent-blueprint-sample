# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing unreleased yet.

## [0.1.0] - 2026-10-29

### Added

- Initial release of `tally`, a command-line tool that counts whitespace-separated words and lines in a text file.
- `tally words FILE` and `tally lines FILE` commands, usable as a script (`python -m tally`) or via the `tally` console entry point after installing the package with `pip install -e .`.
- Line counting treats a trailing newline as ending the last line rather than starting a new one.
- Clear error messages and exit codes for bad usage (exit code 2) and missing files (exit code 1).
- Unit test suite covering the counting functions and the command-line interface, run with `python3 -m unittest`.
