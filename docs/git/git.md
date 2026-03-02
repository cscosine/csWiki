<!-- TOC BEGIN -->
**Table Of Contents**
- [../index](../index.md)
- [Git Mini Cheat Sheet](git.md#git-mini-cheat-sheet)
- [File historyAndIdentity](historyAndIdentity.md)
  - [🔥 Git History Rewrite Procedure (Clean Identity Reset)](historyAndIdentity.md#🔥-git-history-rewrite-procedure-(clean-identity-reset))
- [File setup](setup.md)
  - [✅ Recommended Repository-Only Git Identity Configuration](setup.md#✅-recommended-repository-only-git-identity-configuration)
<!-- TOC END -->

# Git Mini Cheat Sheet

## Commit

```bash
# Commit all tracked changes
git commit -a -m "your message"

# Add everything (including untracked) and commit
git add .
git commit -m "your message"

# Amend last commit message
git commit --amend -m "new message"
```

---

## Push

```bash
# Push current branch
git push

# Push current branch explicitly to origin
git push origin HEAD

# Push specific branch
git push origin branch-name

# Safe force push (recommended)
git push --force-with-lease origin branch-name
```

---

## Pull

```bash
# Pull current branch
git pull

# Pull specific branch
git pull origin branch-name

# Pull using rebase instead of merge
git pull --rebase
```

---

## Fetch

```bash
# Fetch from origin
git fetch origin

# Fetch and prune deleted remote branches
git fetch --prune
```

---

## Clone

```bash
# Clone repository
git clone <repository-url>

# Clone specific branch only
git clone --branch branch-name --single-branch <repository-url>
```

---

## Branch

```bash
# List branches
git branch
git branch -a

# Create new branch
git branch new-branch

# Switch branch
git checkout branch-name
git checkout -b new-branch

# Modern alternative
git switch branch-name
git switch -c new-branch

# Delete local branch
git branch -d branch-name

# Force delete local branch
git branch -D branch-name

# Delete remote branch
git push origin --delete branch-name
```

---

## Rebase

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase last 3 commits
git rebase -i HEAD~3

# Interactive rebase from specific base branch
git rebase -i main
```

Common interactive options inside editor:

```
pick    use commit
reword  edit commit message
edit    amend commit
squash  combine commits
fixup   squash without keeping message
drop    remove commit
```

If something goes wrong:

```bash
# Abort rebase
git rebase --abort

# Continue after resolving conflicts
git rebase --continue
```

---

## Tags

Reusable Variable

```bash
# Define reusable tag variable
TAG="v1.0.0"
```
---

```bash
# Create lightweight tag
git tag $TAG

# Create annotated tag (recommended)
git tag -a $TAG -m "Release $TAG"

# Push single tag
git push origin $TAG

# Push all tags
git push origin --tags

# Delete local tag
git tag -d $TAG

# Delete remote tag
git push origin --delete $TAG
```

---

## Log & Status

```bash
# Status
git status

# Compact log view
git log --oneline --graph --decorate --all
```

---

## Reset

```bash
# Soft reset (keep staged changes)
git reset --soft HEAD~1

# Hard reset (discard changes)
git reset --hard HEAD~1
```