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

`words` prints the number of whitespace-separated words in `FILE`, and `lines` prints the number
of lines (a trailing newline does not add a line). Each prints a bare number on stdout.

```console
$ printf 'the quick brown fox\njumps over the lazy dog\n' > notes.txt
$ tally words notes.txt
9
$ tally lines notes.txt
2
```

Without installing, run the same commands from the repository root as
`python3 -m tally words notes.txt`.

## Tests

```bash
python3 -m unittest
```

## License

MIT.
