<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [Manage Forked Repo And Update](#manage-forked-repo-and-update)
- [Recommended structure](#recommended-structure)
<!-- TOC END -->

# Manage Forked Repo And Update

Goal:

- Fork a repo
- Start from an upstream tag
- Add my small change as one commit
- Tag my patched version
- Later update to a newer upstream tag and replay my patch

---

## 1. Fork and clone

Fork the repository on GitHub/GitLab.

Clone your fork:

```bash
git clone git@github.com:YOURNAME/project.git
cd project
```

Add original repo as upstream:

```bash
git remote add upstream git@github.com:ORIGINAL/project.git
git remote -v
```

Result:

```
origin    -> my fork
upstream  -> original repo
```

---

## 2. Start from an upstream tag

Fetch upstream tags:

```bash
git fetch upstream --tags
```

List tags:

```bash
git tag
```

Create a branch from the desired upstream tag:

```bash
git checkout -b my-patch v1.2.3
```

Now the branch starts exactly at:

```
upstream v1.2.3
```

---

## 3. Add my small change

Edit files:

```bash
vim file
```

Commit the patch:

```bash
git add file
git commit -m "Apply my custom change"
```

History:

```
v1.2.3
  |
  +-- my custom change
```

---

## 4. Create my tag

Create an annotated tag:

```bash
git tag -a my-v1.2.3 -m "My patch on upstream v1.2.3"
```

Push branch and tag:

```bash
git push origin my-patch
git push origin my-v1.2.3
```

---

## Updating later to a newer upstream version

Example:

Upstream releases:

```
v1.3.0
```

Fetch:

```bash
git fetch upstream --tags
```

Rebase my patch on top of the new version:

```bash
git rebase v1.3.0
```

Git will replay:

```
old:

v1.2.3
  |
  +-- my change


new:

v1.3.0
  |
  +-- my change
```

If conflicts happen:

```bash
git status

# fix files

git add fixed_files

git rebase --continue
```

---

## Create new patched tag

Remove old local tag if needed:

```bash
git tag -d my-v1.2.3
```

Create new tag:

```bash
git tag -a my-v1.3.0 -m "My patch on upstream v1.3.0"
```

Push:

```bash
git push origin my-v1.3.0
```

---

# Recommended structure

Keep:

```
main
 |
 |-- follows upstream

my-patch
 |
 |-- one or more downstream commits

tags:

v1.2.3       upstream
my-v1.2.3    my patched release
v1.3.0       upstream
my-v1.3.0    my patched release
```

Update flow:

```bash
git fetch upstream --tags

git checkout my-patch

git rebase v1.3.0

git tag -a my-v1.3.0 -m "My patch on upstream v1.3.0"

git push origin my-patch --tags
```

This keeps your customization as a small replayable patch on top of upstream releases.
