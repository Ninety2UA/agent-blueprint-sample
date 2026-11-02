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
the quick brown fox
jumps over
the lazy dog
```

Count its words:

```console
$ tally words notes.txt
9
```

Count its lines:

```console
$ tally lines notes.txt
3
```

## Tests

```bash
python3 -m unittest
```

## License

MIT.
