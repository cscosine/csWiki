# csWiki

Visit [csWiki](https://cscosine.github.io/csWiki/) to browse the documentation.

---

## 📦 Project Overview

csWiki is a centralized documentation system for notes, tips & tricks, and useful commands.

Key principles:

- ✅ Keep it simple
- ✅ Use only `.md` files
- ✅ Organize documents freely in folders
- ✅ Automatically generate navigation tables via `generateTOC.py`

---

## 📁 Repository Structure

```
csWiki/
├── src/
│   └── toc_generator/          # Reusable TOC generator package
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── markdown_utils.py   # Markdown parsing and anchors
│       ├── report.py           # Reporting system
│       ├── tree.py             # Folder tree model and scanning
│       ├── toc.py              # TOC tree construction
│       └── writer.py           # TOC injection into files
├── tests/                      # Pytest test suites (excluded from linting)
│   ├── test_cli.py
│   ├── test_markdown_utils.py
│   ├── test_report.py
│   ├── test_toc.py
│   ├── test_tree.py
│   └── test_writer.py
├── docs/                       # Published documentation (Jekyll/GitHub Pages)
│   ├── index.md                # **Mandatory main entry file**
│   ├── _config.yml             # Jekyll configuration
│   └── ...                     # Other .md files and subfolders
├── conftest.py                 # Add src/ to python path to execute tests with `pytest`
├── generateTOC.py              # CLI entry point (thin wrapper)
├── pyproject.toml              # Project metadata & tool configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .github/workflows/ci.yml    # GitHub Actions CI pipeline
├── .gitignore                  # Git ignore patterns
├── .gitattributes              # Git attributes for line endings
└── README.md                   # This file
```

---

## 🚀 GitHub Pages Deployment

This project uses **GitHub Pages**.

At every push/commit to `main`:

- GitHub Actions builds the site
- The `docs/` folder is deployed automatically

Your Pages configuration should be:

- Repository → Settings → Pages
- Source: **Deploy from a branch**
- Branch: `main`
- Folder: `/docs`

---

## 🛠 Development Setup

### ⚡ Quick Start

```bash
# 1. Clone repository
git clone git@github.com:cscosine/csWiki.git
cd csWiki

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install package in editable mode with dev dependencies
pip install -e .[dev]

# 4. Run tests directly (package is now importable)
pytest

# 5. Or use pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### 🌍 Detailed Setup

If you prefer step-by-step instructions:

#### Clone Repository

``` bash
git clone git@github.com:cscosine/csWiki.git
```

or

``` bash
git clone https://github.com/cscosine/csWiki.git
```

---

### Create Virtual Environment

``` bash
python -m venv .venv
source .venv/bin/activate
```
_Note_: You may need `python3` instead of `python`.

On Windows:

``` bash
.venv\Scripts\activate
```

or for PowerShell

``` bash
.venv\Scripts\activate.ps1
```

### Install Development Dependencies

All development tools are listed as optional dependencies in `pyproject.toml`:

```bash
pip install -e .[dev]
```

This installs:
- `pytest` — Testing framework
- `mypy` — Static type checking
- `ruff` — Linting and formatting
- `black` — Code formatter
- `pre-commit` — Git hook automation

**Note:** The core package has **no runtime dependencies**; it only uses Python stdlib.

### Install Pre-Commit Hooks

``` bash
pre-commit install
```

Pre-commit hooks run automatically before each commit.

---

## 🔍 Run Pre-Commit Manually

``` bash
pre-commit run --all-files
```

---

## 📚 Add a New Document

1.  Create a `.md` file inside `docs/`
2.  Add TOC markers:

    ```
    <!-- TOC BEGIN -->
    <!-- TOC END -->
    ```

3.  Write content
4.  Run:

    ``` bash
    ./generateTOC.py
    ```

Or commit --- pre-commit updates TOC automatically.

---

## 📚 Add a New Folder

1.  Create a folder `<foldername>` inside `docs/`
1.  Create a file `<foldername>/<foldername>.md` too
2.  Add TOC markers to the file

    ```
    <!-- TOC BEGIN -->
    <!-- TOC END -->
    ```

3.  Write content
4.  Run:

    ``` bash
    ./generateTOC.py
    ```

Or commit --- pre-commit updates TOC automatically.

---

## 🔄 TOC Generation

The script:

-   Traverses `docs/` recursively
-   Extracts headings (only first level: `#`)
-   Builds a hierarchical table of contents
-   Injects it between TOC markers
-   _Note_: it assumes that each folder has `<foldername>/<foldername>.md` file that acts as main file for the folder. If this is not respected, a warning is generated and the folder is ignored

If markers are missing → a warning is generated.

---

## ✅ Toolchain

-   Formatting → Black
-   Linting → Ruff
-   Static typing → Mypy
-   Pre-commit enforcement → pre-commit
-   CI → GitHub Actions

---

## Precommits

Before every commit, the project runs automated checks to guarantee consistency, formatting, and repository integrity.

The following checks are enforced:

- ✅ **TOC Generation** – Automatically regenerates all Table of Contents inside `docs/` using `generateTOC.py`.
- 🎨 **Code Formatting** – Formats Python code using `black`.
- ⚡ **Linting & Auto-Fix** – Runs `ruff` for style checks, bug detection, and automatic fixes.
- 🧠 **Type Checking** – Validates static types with `mypy`.
- 🔒 **Repository Integrity** – Fails if unstaged changes remain after hooks run (`git diff --quiet`).

If any check fails, the commit is blocked until the issues are resolved.

---

## 💡 Philosophy

-   Keep documentation lightweight
-   Automate structure
-   Enforce consistency
-   Avoid manual maintenance
---

## 🧩 Reusable Module & Testing

The TOC-generation logic is a small, installable package in `src/toc_generator/`. This design allows the library to be used independently—either within this repo or published on PyPI.

### Package structure (src-layout)

```
src/toc_generator/
├── __init__.py           # Public API exports
├── cli.py                # Command-line entry point
├── markdown_utils.py     # File parsing and anchor generation
├── report.py             # Reporting and pretty-printing
├── tree.py               # Folder/file tree model and scanning
├── toc.py                # TOC tree construction and finalization
└── writer.py             # TOC generation and file injection
```

**Why src-layout?** It prevents import shadowing (ensures `import toc_generator` always loads the installed package, not a local directory) and makes the structure explicit.

### Using the package

After installation (`pip install -e .`), you can:

1. **Use as a library:**

    ```python
    from toc_generator import create_tree, create_toc_tree, write_toc_on_files
    
    root = create_tree(Path("./docs"), "index")
    toc_tree = create_toc_tree(Path("./docs"), root.root)
    write_toc_on_files(toc_tree)
    ```

2. **Use the CLI:**

    ```bash
    cstoc              # equivalent to ./generateTOC.py
    cstoc --quiet      # suppress debug output
    ```

### Running the tests

The `tests/` directory contains pytest suites for each module (excluded from linting/type-checking).

```bash
# After installation (`pip install -e .`):
pytest

# Or without installation, manually add src/:
PYTHONPATH=src pytest
```

**How imports work:** A `conftest.py` file at the project root is automatically loaded by pytest before running tests. It adds `src/` to Python's import path, ensuring tests can find and import `toc_generator` correctly. This is a standard pytest pattern for src-layout projects and requires no special setup.

All tests pass - the package works independently of the repository structure.

### Dependencies

- **Runtime:** None (stdlib only)
- **Development:** `pytest`, `mypy`, `ruff`, `black`, `pre-commit`

Install all with: `pip install -e .[dev]`
