# tally

A small command-line tool that counts words and lines in a text file. It uses only the Python
standard library and runs on Python 3.9 or later.

This repository is the sample the Agent Blueprint hosted demo works on: visitors ask the agent for a
small change here and get a pull request back.

## Install

```bash
pip install -e .
```

## Tests

```bash
python3 -m unittest
```

## Troubleshooting

- **`tally: command not found`** — the `tally` command only exists after `pip install -e .`. If you
  installed with `--user`, make sure the user scripts directory (for example `~/.local/bin` on
  Linux) is on your `PATH`. You can also skip installing and run `python3 -m tally words FILE`.
- **`usage: tally (words|lines) FILE`** — tally accepts exactly two arguments: the command `words`
  or `lines`, and one file path. Check the spelling and count of your arguments.
- **`tally: no such file: FILE`** — the path you passed does not exist (or is a directory). Check
  the path, or quote it if it contains spaces.
- **`pip install -e .` fails with a Python version error** — the package requires Python 3.9 or
  later. Check with `python3 --version`; if you have several Pythons installed, install against
  the right one with `python3 -m pip install -e .`.
- **`python3 -m unittest` finds no tests** — run it from the repository root, where the `tests`
  directory lives.

## License

MIT.
