<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [Multi-Account GitHub SSH Setup (Clean and Safe)](#multi-account-github-ssh-setup-(clean-and-safe))
<!-- TOC END -->

# Multi-Account GitHub SSH Setup (Clean and Safe)

This guide explains how to configure multiple GitHub accounts on the same machine using SSH so that each repository pushes with the correct account.

Example accounts:
- personal: `personal_name`
- organization: `organization_name`

This prevents accidental pushes with the wrong identity and ensures GitHub Actions shows the correct actor.

## 1. Generate a Separate SSH Key for Each Account

Create one SSH key per GitHub account.

Personal account:

```bash
ssh-keygen -t ed25519 -C "personal_name"
```

Save as:

```
~/.ssh/id_ed25519_personal
```

Organization account:

```bash
ssh-keygen -t ed25519 -C "organization_name"
```

Save as:

```
~/.ssh/id_ed25519_organization
```

Resulting directory structure:

```
~/.ssh/
  id_ed25519_personal
  id_ed25519_personal.pub
  id_ed25519_organization
  id_ed25519_organization.pub
```

## 2. Add Each Key to the Correct GitHub Account

Copy the public keys:

```bash
cat ~/.ssh/id_ed25519_personal.pub
cat ~/.ssh/id_ed25519_organization.pub
```

Add them to GitHub:

Account `personal_name`  
Settings → SSH and GPG keys → New SSH key  
Paste:

```
id_ed25519_personal.pub
```

Account `organization_name`  
Settings → SSH and GPG keys → New SSH key  
Paste:

```
id_ed25519_organization.pub
```

## 3. Configure SSH Aliases

Edit or create:

```
~/.ssh/config
```

Example configuration:

```
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal
  IdentitiesOnly yes

Host github-organization
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_organization
  IdentitiesOnly yes
```

This creates two SSH aliases:
- `github-personal`
- `github-organization`

Each alias uses a different SSH key.

## 4. Test Authentication

Verify each account works.

Test personal account:

```bash
ssh -T github-personal
```

Expected output:

```
Hi personal_name! You've successfully authenticated
```

Test organization account:

```bash
ssh -T github-organization
```

Expected output:

```
Hi organization_name! You've successfully authenticated
```

## 5. Configure Repository Remotes

Set the repository remote to the correct SSH alias.

Repositories that should push as `personal_name`:

```bash
git remote set-url origin git@github-personal:OWNER/REPO.git
```

Repositories that should push as `organization_name`:

```bash
git remote set-url origin git@github-organization:OWNER/REPO.git
```

Example:

```bash
git remote set-url origin git@github-organization:organization_name/myrepo.git
```

## 6. Set Commit Identity Per Repository (Recommended)

This controls commit metadata (author name/email).

For organization repositories:

```bash
git config user.name "organization_name"
git config user.email "organization_email@example.com"
```

For personal repositories:

```bash
git config user.name "personal_name"
git config user.email "personal_email@example.com"
```

## 7. Verify the Setup

Check the configured remote:

```bash
git remote -v
```

Example output:

```
origin git@github-organization:organization_name/repo.git
```

Push a commit and verify on GitHub:

- commit author matches configured git user
- GitHub Actions actor matches the SSH account used for the push

## Result

| Repository type | SSH alias | Push actor |
|-----------------|-----------|-----------|
| personal repos | github-personal | personal_name |
| organization repos | github-organization | organization_name |

This setup ensures:
- correct authentication per repository
- consistent GitHub Actions actors
- no accidental cross-account pushes