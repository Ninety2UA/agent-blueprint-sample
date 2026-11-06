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

```text
tally (words|lines) FILE
```

`words` prints the number of whitespace-separated words in `FILE`; `lines` prints the number of
lines (a trailing newline does not count as an extra line).

```bash
$ printf 'alpha beta\ngamma\n' > notes.txt
$ tally words notes.txt
3
$ tally lines notes.txt
2
```

Without installing, run it as `python3 -m tally words notes.txt`. It exits with status 0 on
success, 1 if `FILE` does not exist, and 2 on bad arguments (with a usage message on stderr).

## Tests

```bash
python3 -m unittest
```

## License

MIT.
