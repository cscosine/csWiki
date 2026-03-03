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

- `README.md` → This file
- `docs/` → Folder containing all published documentation 
  - `index.md` → **Mandatory main entry file**
  - `_config.yml` → Jekyll configuration (mainly the `theme`)
  - other files and subfolders...
- `generateTOC.py` → Script that scans the `docs/` folder and automatically generates navigable TOC tables inside `.md` files
- `.github/workflows/ci.yml` → CI pipeline enforcing formatting, linting, and type safety
- `.pre-commit-config.yaml` → precommit hooks enforcing formatting, linting, and type safety
- `.gitignore` → ignored files/folder/patterns by git
- `.gitattributes` → specify type of files and avoid problems with CRLF/LF in Windows/Linux setup

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


### 🌍 Clone Repository

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

### Install Development Tools

``` bash
pip install black ruff mypy pre-commit
```

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

The TOC-generation logic is implemented into a
small installable package under `toc_generator/`.

### Package structure

```
csWiki/
├── toc_generator/
│   ├── __init__.py           # primary API
│   ├── cli.py                # command‑line driver
│   ├── markdown_utils.py     # file parsing and anchor helpers
│   ├── report.py             # lightweight reporting object
│   ├── tree.py               # workspace scanning/data model
│   ├── toc.py                # TOC tree builder & navigation logic
│   └── writer.py             # inject TOC into files
└── generateTOC.py            # thin wrapper that calls `toc_generator`
```

Consumers can now do e.g.::

    from toc_generator import create_tree, create_toc_tree, write_toc_on_files

and the same functionality can be published on PyPI or vendored elsewhere.

### Running the tests

A new `tests/` directory contains `pytest` suites covering each module.  To
execute them locally use:

```bash
pip install pytest
pytest
```

The tests exercise the various parsing, tree‑building and file‑writing helpers
and also include a minimal CLI smoke test.  This makes future refactoring much
easier and ensures the library works independently of the repository layout.

### Dependencies

The core library has **no external runtime dependencies**; it only uses
stdlib modules such as `pathlib`, `re` and `argparse`.  Development and CI
requirements are listed as an optional group in `pyproject.toml`, so you can
install them with::

    pip install -e .[dev]

which will pull in `pytest`, `mypy`, `ruff`, `black` and anything else needed
for tests and static analysis.  Production consumers need only `cswiki-toc`
itself.

### Running tests without setting PYTHONPATH

After installing with `pip install -e .` in the workspace root you can run
`pytest` directly; the package will be importable just like any other
installed library.  The `PYTHONPATH=$PWD` hack is only needed when running
against the code without installation.


### `src/` layout rationale

The code has been moved into `src/toc_generator` using the canonical
"src" layout.  This pattern is common in Python projects because it:

* prevents tests or other modules from importing the package using a
  shadowed local directory (i.e. `import toc_generator` will always load
  the installed package, not some subdirectory accidentally added to
  `sys.path`).
* makes it obvious where the actual importable code lives, which is
  helpful when the repo also contains other tooling or top‑level scripts.

If you execute the tests without installing the package, you'll need to
add `src` to `PYTHONPATH` (the previous instructions already suggested
`PYTHONPATH=$PWD pytest ...`).  After running `pip install -e .` the
layout becomes completely transparent and you can simply run `pytest`.

