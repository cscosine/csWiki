<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : python](python.md)
- [Configure pytest to skip some tests (e.g. _slow_)](#configure-pytest-to-skip-some-tests-(e.g.-_slow_))
<!-- TOC END -->

# Configure pytest to skip some tests (e.g. _slow_)

## 📁 Project structure

```bash
.
├── pyproject.toml
├── conftest.py
└── tests/
   └── test_example.py
```

## 📄 `pyproject.toml`

```bash
[tool.pytest.ini_options]
addopts = "-m 'not slow'"  # makes this the default: `pytest` == `pytest -m "not slow"` (skip tests marked slow)
markers = [
  "slow: marks tests as slow",
]
```

## 📄 `conftest.py`

```py
import pytest

def pytest_addoption(parser):
  parser.addoption("--run-slow", action="store_true", default=False)

def pytest_collection_modifyitems(config, items):
  if config.getoption("--run-slow"):
    return
  
  skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
  
  for item in items:
    if "slow" in item.keywords:
      item.add_marker(skip_slow)
```

## 📄 `tests/test_example.py`

```py
import pytest

def test_fast():
assert True

@pytest.mark.slow
def test_slow():
assert True
```

## ▶️ Usage

```bash
pytest
# Runs all tests EXCEPT slow ones (because of addopts default)

pytest --run-slow
# Runs everything (overrides skipping logic from `conftest.py`)

pytest -m "not slow"
# -m filters by markers (here: exclude tests marked `"slow"`)

pytest -k "fast"
# -k filters by test names (runs tests whose names contain "fast")
```

## 📌 Multiple markers (tags)

You can assign more than one marker to a test, and combine them using `-m`.

### 📄 Example: multiple markers on a test

```python
import pytest

@pytest.mark.slow
@pytest.mark.git
def test_something():
    assert True
```

### 📄 Register markers (pyproject.toml)

```bash
[tool.pytest.ini_options]
markers = [
  "slow: marks tests as slow",
  "git: marks tests that require git",
]
```

### ▶️ Running tests with multiple markers

```bash
# run tests that are BOTH slow AND git-related
pytest -m "slow and git"

# run tests that are slow OR git-related
pytest -m "slow or git"

# exclude multiple markers
pytest -m "not slow and not git"
```

### 💡 Tip

Markers can be freely combined using boolean logic (`and`, `or`, `not`, parentheses).