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

## Greeting script

The repository also includes a small standalone greeting script in `scripts/`, outside the `tally`
package, so it needs no install.

```bash
python3 scripts/greet.py       # prints: Hello, World!
python3 scripts/greet.py Ada   # prints: Hello, Ada!
```

## License

MIT.
