# csWiki

The cscosine wiki: notes, tips and commands, with its table-of-contents generator

Visit [csWiki](https://cscosine.github.io/csWiki/) to browse the documentation.

---

<!-- cs-template:begin (this block is owned by cs-project-template: do not edit; the rest of the file is the project's) -->
## Getting started

Requires Python 3.11 or newer and Git.

```bash
./setup.sh                    # Windows: .\setup.ps1
source .venv/bin/activate     # Windows: .\.venv\Scripts\Activate.ps1
```

`setup.sh` creates `.venv`, installs the project with its development tools, and installs the
pre-commit hooks.

Checks and tests:

```bash
pre-commit run --all-files
pytest                        # --run-all: every test, as CI; --run=<marker>: an opt-in group (tests/conftest.py)
```

The shared files (setup, checks, CI, agent rules) come from
[cs-project-template](https://github.com/cscosine/cs-project-template); to bring them to its latest version, on a
branch: `copier update --defaults`.
<!-- cs-template:end -->

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

-   Formatting → Ruff (`ruff-format`)
-   Linting → Ruff
-   Static typing → Mypy
-   Pre-commit enforcement → pre-commit
-   CI → GitHub Actions

---

## Precommits

Before every commit, the project runs automated checks to guarantee consistency, formatting, and repository integrity.

The following checks are enforced:

- ✅ **TOC Generation** – Automatically regenerates all Table of Contents inside `docs/` using `generateTOC.py`.
- 🎨 **Code Formatting** – Formats Python code using `ruff-format` (Ruff's formatter).
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

The TOC-generation logic is a small, installable package in `src/toc_generator/`. This design allows the library to be used independently-either within this repo or published on PyPI.

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
    cstoc                      # equivalent to ./generateTOC.py
    cstoc --quiet              # suppress debug output
    cstoc --docs-path <dir>    # generate TOCs over a custom docs folder
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
- **Development:** `pytest`, `pytest-cov`, `mypy`, `ruff`, `pre-commit`

Install all with: `pip install -e .[dev]`
