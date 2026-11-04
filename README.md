# tally

A small command-line tool that counts words, lines and characters in a text file. It uses only
the Python standard library and runs on Python 3.9 or later.

This repository is the sample the Agent Blueprint hosted demo works on: visitors ask the agent for a
small change here and get a pull request back.

## Install

```bash
pip install -e .
```

## Usage

```bash
tally words FILE   # prints the number of whitespace-separated words
tally lines FILE   # prints the number of lines
tally chars FILE   # prints the number of characters (Unicode characters, whitespace and newlines included)
```

## Tests

```bash
python3 -m unittest
```

## License

MIT.
