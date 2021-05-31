# Kommt heute Aktenzeichen?

## Setting up Kommt heute Aktenzeichen?

To set up Kommt heute Aktenzeichen?, you need three things:

1. The Python version manager `pyenv`.

2. Python (any version).

3. The Python dependency manager `pipenv`.

### Installing pyenv

The Python version manager `pyenv` makes sure you can always keep
the exact Python version required by Kommt heute Aktenzeichen?,
regardless of your system Python.

To install `pyenv` on Windows, run:

```
python -m pip install pyenv
```

To install `pyenv` on macOS, run:

```
brew install pyenv
```

### Checking your system-wide Python installation

Make sure you have Python (any version) installed on your system.

To check, run:

```
pip --version
```

If that fails, try:

```
pip3 --version
```

Proceed after you’ve confirmed one of those to work.

### Installing pipenv

Install `pipenv` as described under https://pipenv.pypa.io/en/latest/install/#installing-pipenv.

### Finishing up the project setup

- Go to the kommtheuteaktenzeichen directory.

- Run the following command:

```
pipenv install -d
```


## Running kommtheuteaktenzeichen

To check whether Aktenzeichen runs today, run the following command line:

```
pipenv run kha check
```


## Contributing to kommtheuteaktenzeichen

### Running the tests

To execute the tests, run:

```
pipenv run tests
```

To execute a single test, run e. g.:

```
pipenv run tests -vv tests/kha/test_api.py::test_next_start
```

### Running the linter

To execute the linter, run:

```
pipenv run linter
```

### Running the static type check

To execute the static type check, run:

```
pipenv run typecheck
```


## Maintenance

### Refresh dependencies

If you get errors after a Git pull, refresh your dependencies:

```
pipenv install -d
```

### Checking dependencies for vulnerabilities

To check Kommt heute Aktenzeichen?’s dependencies for known vulnerabilities, run:

```
pipenv check
```

### Checking dependencies for compatible updates

To check Kommt heute Aktenzeichen?’s dependencies for compatible updates, run:

```
pipenv update --dry-run
```


## License

Copyright (c) 2021 The kommtheuteaktenzeichen authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
For a copy of the License, see [LICENSE](LICENSE).
