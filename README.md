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

Count the words in a file:

```console
$ tally words sample.txt
3
```

Count the lines in a file:

```console
$ tally lines sample.txt
2
```

Given a `sample.txt` containing:

```text
alpha beta
gamma
```

Both commands print the count and exit with status 0. Bad arguments print a usage message to
stderr and exit with status 2; a missing file exits with status 1.

## Tests

```bash
python3 -m unittest
```

## License

MIT.
