<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [Git Worktree — Quick Reference](#git-worktree-—-quick-reference)
<!-- TOC END -->

# Git Worktree — Quick Reference

Multiple working directories attached to **one** Git repo. Each worktree has its own files on disk but shares the same `.git` history, remotes, and object database.

**Typical use:** keep `~/project` on branch A with a long build running, and open `~/project-review` on branch B for code review or a quick fix — no stash, no branch switch, no second full clone.

---

## Basics

```sh
# Create a new directory and check out an existing branch there.
# ../project-review = sibling folder; main = branch to check out.
git worktree add ../project-review main

# Create a NEW branch AND a worktree in one step.
# -b hotfix          → create branch "hotfix"
# origin/main        → start from this commit
# ../project-fix     → put files in this directory
git worktree add ../project-fix -b hotfix origin/main

# Check out a specific branch (e.g. a remote review branch) in a new folder.
git worktree add ../project-cl change-123456

# Show all worktrees: path, HEAD commit, branch name.
# The main checkout is always listed too.
git worktree list

# Remove a worktree when you're done.
# The directory must exist and ideally be clean (no uncommitted changes).
git worktree remove ../project-review

# Delete stale worktree records (e.g. after manually deleting the folder).
git worktree prune
```

---

## Common workflows

```sh
# --- Review while a build runs in your main checkout ---
cd ~/myproject
# Add a read-only/review checkout on main (or any branch)
git worktree add ../myproject-review origin/main
cd ../myproject-review
# Diff, read files, run small tests — ~/myproject keeps compiling untouched

# --- Quick fix without disturbing WIP on your main tree ---
# Create branch "fix/typo" from main, in a separate folder
git worktree add ../myproject-hotfix -b fix/typo main
cd ../myproject-hotfix
# Fix, commit, push, then: git worktree remove ../myproject-hotfix

# --- Compare two branches side-by-side in your editor ---
git worktree add ../myproject-a feature-a
git worktree add ../myproject-b feature-b
# Open both folders in separate editor windows
```

---

## Rules & gotchas

| Rule | Detail |
|------|--------|
| One branch per worktree | Git won't let the same branch be checked out in two places |
| Shared `.git` | Commits, remotes, tags, reflog — all shared across worktrees |
| Separate working files | Source files, build dirs, uncommitted edits — per worktree |
| Uncommitted changes | Stashing/switching in one worktree doesn't affect another |
| IDE / agents | Point each Cursor window or agent at the correct worktree path |
| Build caches | Often global/shared (`~/.cache/*`, npm, cargo, ccache) |
| Build outputs | Usually local per worktree (`build/`, `node_modules/`) |
| Concurrent builds | Safe, but two heavy builds may compete for CPU/GPU/RAM/disk |

---

## Useful flags

```sh
# Create a new branch AND a worktree in one command.
# NEW_BRANCH = name to create; START_POINT = commit/branch to branch from; PATH = folder.
git worktree add -b NEW_BRANCH START_POINT PATH

# Check out a specific commit without attaching a branch (detached HEAD).
# Good for reviewing a exact patchset — don't commit here unless you know why.
git worktree add --detach PATH COMMIT

# Force-add even if Git thinks the branch is already checked out elsewhere.
# Rare; usually means something is misconfigured — use with care.
git worktree add -f PATH BRANCH

# Prevent accidental removal (e.g. long-lived review worktree).
git worktree lock PATH

# Allow removal again after locking.
git worktree unlock PATH

# Move a worktree to a different directory (rename/relocate the folder properly).
git worktree move OLD_PATH NEW_PATH

# Remove even if there are uncommitted changes (discards uncommitted work in that tree).
git worktree remove --force PATH
```

---

## Cleanup

```sh
# See all active worktrees and which branch each is on.
git worktree list

# Remove a worktree cleanly (preferred).
git worktree remove PATH

# Remove even with uncommitted changes — those changes are lost.
git worktree remove --force PATH

# Clean up metadata for folders you deleted manually (rm -rf).
git worktree prune
```

---

## vs alternatives

| Approach | Best for |
|----------|----------|
| `git worktree` | Parallel branches, shared history, less disk than a second clone |
| Second `git clone` | Full isolation; simpler; uses more disk |
| `git stash` + `git switch` | Quick one-off switches; bad when a long build is running |
