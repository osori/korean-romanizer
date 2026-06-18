# korean-romanizer
korean-romanizer is a python module that romanizes Korean text in Hangul into its alphabet equivalent.

It currently follows the [Revised Romanization of Korean](https://www.korean.go.kr/front_eng/roman/roman_01.do) rule developed by the National Institute of Korean Language, the official romanization system being used in the Republic of Korea.


## Usage

### Installation
```bash
pip install korean_romanizer
```

### Basic Usage
```python
from korean_romanizer import romanize

romanize("안녕하세요")
# returns "annyeonghaseyo"
```

The existing class API remains supported for compatibility:

```python
from korean_romanizer import Romanizer

Romanizer("안녕하세요").romanize()
# returns "annyeonghaseyo"
```

The formerly documented module import path also remains supported:

```python
from korean_romanizer.romanizer import Romanizer
```

Use the `kroman` command for shell workflows:

```bash
kroman 안녕하세요
# annyeonghaseyo
```

Wildcard imports now follow the explicit public API in `__all__`:

```python
from korean_romanizer import *
```

This imports only `romanize`, `Romanizer`, `Pronouncer`, and `Syllable`.

`Pronouncer` and `Syllable` are also exported as lower-level compatibility
APIs. Constants, tables, and helper functions are internal implementation
details and should not be imported by application code.

## Development

Install the local development tools with the `dev` extra:

```bash
python3 -m pip install -e ".[dev]"
```

Useful checks:

```bash
python3 -m pytest
python3 -m pytest --cov=korean_romanizer
ruff check .
mypy korean_romanizer
python3 -m build
```

## Releasing

Publishing to PyPI is automated using GitHub Actions. Pushing a version tag or
creating a GitHub release triggers the workflow in
`.github/workflows/python-publish.yml` which builds and uploads the package using
the `PYPI_API_TOKEN` secret. The package version is derived from git tags using
`setuptools_scm`, so create a new tag or GitHub release when publishing a new
version.
