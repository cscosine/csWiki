<!-- TOC BEGIN -->
**Table Of Contents**
- [../git](git.md)
- [🔥 Git History Rewrite Procedure (Clean Identity Reset)](#🔥-git-history-rewrite-procedure-(clean-identity-reset))
<!-- TOC END -->

# 🔥 Git History Rewrite Procedure (Clean Identity Reset)

⚠️ WARNING:
This rewrites commit history.
All commit SHAs will change.
Force push is required.

---

## 1️⃣ Work on a Mirror Clone

```bash
git clone --mirror git@github.com:USER/REPO.git
cd REPO.git
```

---

## 2️⃣ Rewrite Author + Committer Identity + Remove Signatures

Install:

```bash
pip install git-filter-repo
```

Run:

```bash
git filter-repo \
  --name-callback 'return b"Your Name"' \
  --email-callback 'return b"your.email@gmail.com"' \
  --commit-callback '
    commit.gpgsig = None
  '
```

This rewrites:

- Author name
- Author email
- Committer name
- Committer email
- Annotated tags
- Removes GPG signatures

---

## 3️⃣ Verify Clean History

Check metadata:

```bash
git log --all --pretty=format:"%an %ae | %cn %ce"
```

Search for unwanted strings:

```bash
git log --all --grep=OLD_STRING -i
git grep -i OLD_STRING $(git rev-list --all)
```

Check signatures:

```bash
git log --show-signature
```

---

## 4️⃣ Force Push Clean History

```bash
git push --force --all
git push --force --tags
```

---

## ✅ Optional: Absolute Clean Reset

For maximum cleanup:

1. Delete repository from GitHub
2. Recreate it
3. Push cleaned mirror again

This removes:

- PR history
- Issue references
- Tags
- Workflow metadata

---

## ✅ Result

After this procedure:

- No legacy email remains
- No legacy identity remains
- No GPG signatures remain
- All commits reflect the new identity
- History is fully sanitized