<!-- TOC BEGIN -->
## Table Of Contents
- [../git](git.md)
<!-- TOC END -->

# Clean SSH + Git Multi-Account Setup (Delete Everything and Start Fresh)

This guide resets all SSH keys and rebuilds a clean **multi-account Git setup** (e.g., personal + work).  
It also includes how to **verify and fix repository remotes** to ensure the correct SSH identity is used.

---

## 1. Remove All Existing SSH Keys

First inspect your current SSH directory:

```bash
ls -al ~/.ssh
```

If you want a **complete reset**:

```bash
rm -rf ~/.ssh
mkdir ~/.ssh
chmod 700 ~/.ssh
```

This removes:

- all private keys
- all public keys
- old configs
- any conflicting SSH setup

---

## 2. Clear SSH Agent

Remove any keys currently loaded in the SSH agent:

```bash
ssh-add -D
```

Verify it's empty:

```bash
ssh-add -l
```

Expected result:

```
The agent has no identities.
```

---

## 3. Generate One SSH Key Per Git Account

Using **ed25519** is recommended.

### Personal account

```bash
ssh-keygen -t ed25519 -C "personal@email.com"
```

Save as:

```
~/.ssh/id_ed25519_personal
```

### Work account

```bash
ssh-keygen -t ed25519 -C "work@email.com"
```

Save as:

```
~/.ssh/id_ed25519_work
```

Resulting files:

```
~/.ssh/id_ed25519_personal
~/.ssh/id_ed25519_personal.pub
~/.ssh/id_ed25519_work
~/.ssh/id_ed25519_work.pub
```

---

## 4. Create SSH Config for Multiple Accounts

Edit the SSH config file:

```bash
nano ~/.ssh/config
```

Example configuration:

```ssh
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal
  IdentitiesOnly yes

Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
  IdentitiesOnly yes
```

Set proper permissions:

```bash
chmod 600 ~/.ssh/config
```

This creates **SSH aliases**:

- `github-personal`
- `github-work`

These force Git to use the correct key.

---

## 5. Add Keys to SSH Agent

```bash
ssh-add ~/.ssh/id_ed25519_personal
ssh-add ~/.ssh/id_ed25519_work
```

Verify:

```bash
ssh-add -l
```

You should see both keys listed.

---

## 6. Add Public Keys to Your Git Accounts

Print the public key:

```bash
cat ~/.ssh/id_ed25519_personal.pub
```

Add it to:

GitHub → **Settings → SSH and GPG keys**

Repeat for the work key:

```bash
cat ~/.ssh/id_ed25519_work.pub
```

Add it to the work account.

---

## 7. Test Authentication

Test each SSH identity.

### Personal

```bash
ssh -T git@github-personal
```

### Work

```bash
ssh -T git@github-work
```

Expected message:

```
Hi username! You've successfully authenticated.
```

---

## 8. Clone Repositories Using the Correct Host

Use the SSH aliases defined earlier.

### Personal repo

```bash
git clone git@github-personal:username/repo.git
```

### Work repo

```bash
git clone git@github-work:company/repo.git
```

This ensures Git uses the correct SSH key automatically.

---

## 9. Verify Current Repository Remote

Inside any repository, check the configured remote:

```bash
git remote -v
```

Example output:

```
origin  git@github.com:username/repo.git (fetch)
origin  git@github.com:username/repo.git (push)
```

If you see `git@github.com`, then **your SSH config alias is NOT being used**.

Correct multi-account setup should look like:

```
origin  git@github-personal:username/repo.git
```

or

```
origin  git@github-work:company/repo.git
```

---

## 10. Fix an Incorrect Remote

To update the remote URL:

### Personal repo

```bash
git remote set-url origin git@github-personal:username/repo.git
```

### Work repo

```bash
git remote set-url origin git@github-work:company/repo.git
```

Verify the fix:

```bash
git remote -v
```

---

## 11. Verify Which SSH Key Is Used (Debug)

If authentication problems occur, run:

```bash
ssh -vT git@github-personal
```

or

```bash
ssh -vT git@github-work
```

Look for the line:

```
Offering public key: ~/.ssh/id_ed25519_personal
```

This confirms the correct key is being used.

---

## 12. Optional: Set Git Identity

Global default:

```bash
git config --global user.name "Your Name"
git config --global user.email "personal@email.com"
```

For work repositories:

```bash
git config user.email "work@email.com"
```

Verify:

```bash
git config --list
```

---

## Result

You now have:

- a clean SSH setup
- separate keys for each account
- deterministic Git authentication
- correct repository remotes
- easier debugging if something breaks