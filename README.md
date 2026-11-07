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

Give `tally` a command, `words` or `lines`, and a file. It prints the count to standard output.

```bash
tally words FILE
tally lines FILE
```

For example, for a file `notes.txt` that holds these two lines:

```text
hello world
second line here
```

```bash
tally words notes.txt   # prints 5
tally lines notes.txt   # prints 2
```

To run it from the project root without installing, use `python3 -m tally words FILE`.

## Tests

```bash
python3 -m unittest
```

## License

MIT.
