# tally

A small command-line tool that counts words and lines in a text file. It uses only the Python
standard library and runs on Python 3.9 or later.

This repository is the sample the Agent Blueprint hosted demo works on: visitors ask the agent for a
small change here and get a pull request back.

## Install

```bash
pip install -e .
```

## Usage

Given a file `notes.txt`:

```text
alpha beta
gamma
```

Count its words:

```console
$ tally words notes.txt
3
```

Count its lines (a trailing newline does not add a line):

```console
$ tally lines notes.txt
2
```

Without installing, run `python3 -m tally` from the repository root in place of `tally`.

## Tests

```bash
python3 -m unittest
```

## License

MIT.
