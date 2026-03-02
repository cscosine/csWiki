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
- `.nojekyll` → Ensures GitHub Pages does not use Jekyll processing
- `generateTOC.py` → Script that scans the `docs/` folder and automatically generates navigable TOC tables inside `.md` files
- `.github/workflows/ci.yml` → CI pipeline enforcing formatting, linting, and type safety
- `.pre-commit-config.yaml` → precommit hooks enforcing formatting, linting, and type safety

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

### Create Virtual Environment

``` bash
python -m venv .venv
source .venv/bin/activate
```

(Windows)

``` bash
.venv\Scripts\activate
```

### Install Development Tools

``` bash
pip install black ruff mypy pre-commit
```

You may need `python3` instead of `python`.

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

## 🔄 TOC Generation

The script:

-   Traverses `docs/` recursively
-   Extracts headings (only first level: `#`)
-   Builds a hierarchical table of contents
-   Injects it between TOC markers

If markers are missing → a warning is generated.

---

## ✅ Toolchain

-   Formatting → Black
-   Linting → Ruff
-   Static typing → Mypy
-   Pre-commit enforcement → pre-commit
-   CI → GitHub Actions

### Precommits

Before every commit, the project runs automated checks to guarantee consistency, formatting, and repository integrity.

The following checks are enforced:

- ✅ **TOC Generation** – Automatically regenerates all Table of Contents inside `docs/` using `generateTOC.py`.
- 🎨 **Code Formatting** – Formats Python code using `black`.
- ⚡ **Linting & Auto-Fix** – Runs `ruff` for style checks, bug detection, and automatic fixes.
- 🧠 **Type Checking** – Validates static types with `mypy`.
- 🔒 **Repository Integrity** – Fails if unstaged changes remain after hooks run (`git diff --quiet`).

If any check fails, the commit is blocked until the issues are resolved.

---

## 🌍 Clone Repository

### SSH

``` bash
git clone git@github.com:cscosine/csWiki.git
```

### HTTPS

``` bash
git clone https://github.com/cscosine/csWiki.git
```

---

## 💡 Philosophy

-   Keep documentation lightweight
-   Automate structure
-   Enforce consistency
-   Avoid manual maintenance