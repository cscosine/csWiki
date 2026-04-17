<!-- TOC BEGIN -->
## Table Of Contents
- [../git](git.md)
<!-- TOC END -->

# Setup Meld as Default Git Merge Tool on Ubuntu/Debian

## 1️⃣ Install Meld
```bash
sudo apt update
sudo apt install meld
```

## 2️⃣ Configure Git to use Meld
```bash
git config --global merge.tool meld
git config --global mergetool.meld.path meld
git config --global mergetool.keepBackup false
git config --global mergetool.prompt false
git config --global diff.tool meld
git config --global difftool.prompt false
```

## 3️⃣ Usage

### Merge conflicts
```bash
git mergetool
```
Opens Meld with LOCAL, BASE, REMOTE, MERGED view

### Viewing diffs
```bash
git difftool
```
Opens Meld to compare changes between commits or branches