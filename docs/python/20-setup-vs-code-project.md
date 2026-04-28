<!-- TOC BEGIN -->
## Table Of Contents
- [../python](python.md)
<!-- TOC END -->

# Setup VS Code to Use Python Efficiently

How to configure a project configured for a smooth VS Code experience with pytest-based testing and debugging.

---

## 📦 Recommended Extensions

VS Code will prompt you to install recommended extensions automatically.

They are defined in:

```bash
.vscode/extensions.json
```

### 🔹 `extensions.json`

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.debugpy"
  ]
}
```

### What these do:

* **Python extension**
  Python extension for VS Code
  → Provides:

  * IntelliSense
  * Test Explorer
  * Virtual environment support
  * Debugging integration

* **debugpy**
  debugpy
  → Powers the debugging engine used by VS Code

---

## ⚙️ Project Configuration

All configuration lives in:

```bash
.vscode/
```

---

### 🔹 `settings.json`

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

* Enables pytest test discovery
* Disables unittest to avoid conflicts

---

### 🔹 `launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "▶ Debug all tests",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["-s", "--run-all"],
      "justMyCode": false
    }
  ]
}
```

* Used for full test-suite debugging
* Appears in **Run & Debug dropdown**

---

### 🔹 `tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Create venv",
      "type": "shell",
      "command": "python -m venv .venv"
    },
    {
      "label": "Install deps",
      "type": "shell",
      "command": "${command:python.interpreterPath} -m pip install -e .[dev]"
    }
  ]
}
```

* Used for environment setup and dependency installation
* Cross-platform (Windows/Linux/macOS)

---

## 🐍 Environment Setup

Recommended workflow:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install -e .[dev]
code .
```

---

## 🧪 Running Tests

### ▶ Run all tests (debug)

* Open **Run & Debug**
* Select:

  ```
  ▶ Debug all tests
  ```
* Press **F5**

---

### 🧪 Run individual tests

#### Option 1 — Test Explorer (recommended)

* Open Testing panel (flask icon)
* Click:

  * ▶ run
  * 🐞 debug

#### Option 2 — Terminal

```bash
pytest tests/test_file.py::test_name
```

---

## 🏁 Summary

* Install recommended extensions (one-click)
* Activate venv before opening VS Code
* Use Test Explorer for daily workflow
* Use Debug config for full-suite debugging

---
