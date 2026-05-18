<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : pre-commit](pre-commit.md)
- [pre-commit (quick start)](#pre-commit-(quick-start))
<!-- TOC END -->
# pre-commit (quick start)

## What it is
pre-commit runs automated checks before each commit to keep changes consistent and clean.

---

## Install (once per repo)
```bash
pip install pre-commit
pre-commit install
```

---

## Daily usage

Normal commit runs precommit:
```bash
git add .
git commit -m "message"
```

Run checks manually:
```bash
pre-commit run --all-files
```

---

## Skip hooks (WIP / emergency save)

Skip all hooks:
```bash
git commit --no-verify -m "wip"
```

Skip a specific hook:
```bash
SKIP=hook-id git commit -m "message"
```

---

## Clean / reinstall

Clean environments:
```bash
pre-commit clean
```

Reinstall hooks:
```bash
pre-commit install
```
