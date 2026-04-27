<!-- TOC BEGIN -->
## Table Of Contents
- [../python](python.md)
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