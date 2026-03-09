<!-- TOC BEGIN -->
## Table Of Contents
- [../git](git.md)
- [✅ Recommended Repository-Only Git Identity Configuration](#✅-recommended-repository-only-git-identity-configuration)
<!-- TOC END -->

# ✅ Recommended Repository-Only Git Identity Configuration

This ensures your email/name are set **per repository only**, NOT globally.

_note_: see also [Multi-Account GitHub SSH Setup (Clean and Safe)](multiAccount.md#multi-account-github-ssh-setup-(clean-and-safe)) if you want to setup properly multiple accounts on the same machine

## Set Identity for One Repository

Inside the repo:

```bash
git config user.name "Your Name"
git config user.email "your.email@email.com"
```

## Verify It

```bash
git config --local --list
```

Or check what Git will actually use:

```bash
git var -l
git var GIT_COMMITTER_IDENT
git var GIT_AUTHOR_IDENT
```

---

## Additional Useful Settings

Those are ok to be global

```bash
git config --global color.ui=auto
git config --global core.editor=nano
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