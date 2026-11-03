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

## FAQ

- **What does tally do?** It counts words or lines in a text file. Run `tally words FILE` or
  `tally lines FILE` to print the count.
- **Which Python versions are supported?** Python 3.9 or later. There are no third-party
  dependencies — only the standard library.
- **How do I run the tests?** `python3 -m unittest` from the repository root.

## License

MIT.
