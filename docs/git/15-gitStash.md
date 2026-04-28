<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [Partial commit workflow with stash (clean working tree)](#partial-commit-workflow-with-stash-(clean-working-tree))
<!-- TOC END -->

# Partial commit workflow with stash (clean working tree)

This workflow lets you commit only selected changes while temporarily stashing everything else.

## Step 1: Stage what you want to commit

```bash
git add -p
# interactive!
```

or do it in manually your IDE

## Step 2: Stash everything else (including untracked files, but keep staged changes)

```bash
git stash push --keep-index --include-untracked
```

## Step 3: Create your partial commit (only staged changes are included)

```bash
git commit -m "your partial commit message"
```

## Step 4: Restore stashed changes

```bash
git stash pop
```