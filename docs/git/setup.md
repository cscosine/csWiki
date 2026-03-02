<!-- TOC BEGIN -->
**Table Of Contents**
- [../git](git.md)
- [✅ Recommended Repository-Only Git Identity Configuration](#✅-recommended-repository-only-git-identity-configuration)
<!-- TOC END -->

# ✅ Recommended Repository-Only Git Identity Configuration

This ensures your email/name are set **per repository only**, NOT globally.

## Set Identity for One Repository

Inside the repo:

```bash
git config user.name "Your Name"
git config user.email "your.email@gmail.com"
```

## Verify It

```bash
git config --local --list
```

Or check what Git will actually use:

```bash
git var GIT_AUTHOR_NAME
git var GIT_AUTHOR_EMAIL
```

---

## 🔥 Remove Global Identity (Optional – If You Want Strict Per-Repo Control)

Remove global config:

```bash
git config --global --unset user.name
git config --global --unset user.email
```

Check:

```bash
git config --global --list
```

---

## ✅ Optional: Remove System Identity

(System configs affect the whole machine)

```bash
sudo git config --system --unset user.name
sudo git config --system --unset user.email
```

---