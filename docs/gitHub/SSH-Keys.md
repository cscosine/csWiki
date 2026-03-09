<!-- TOC BEGIN -->
## Table Of Contents
- [../gitHub](gitHub.md)
- [Add an SSH Key to GitHub](#add-an-ssh-key-to-github)
<!-- TOC END -->

# Add an SSH Key to GitHub

This guide explains how to create an SSH key and add it to GitHub so you can access repositories without using a password.

---

## Linux / macOS

### 1. Check if you already have an SSH key

Open a terminal and run:

```bash
ls -al ~/.ssh
```

Look for files like:

```
id_ed25519
id_ed25519.pub
```

If they exist, you can reuse them. Otherwise create a new key.

---

### 2. Generate a new SSH key

Run:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Explanation:

- `-t ed25519` → modern secure key type  
- `-C` → comment (usually your GitHub email)

You’ll see prompts like:

```
Enter file in which to save the key:
/home/you/.ssh/id_ed25519
```

Press **Enter** to accept the default.

Then optionally enter a **passphrase** for extra security.

This creates:

```
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

---

### 3. (Optional) Start the SSH agent

This step is recommended but not always required.

Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Example output:

```
Agent pid 1234
```

---

### 4. Add the key to the SSH agent

```bash
ssh-add ~/.ssh/id_ed25519
```

This allows the key to be reused without entering the passphrase repeatedly.

---

### 5. Copy the public key

Display the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output.

Example:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

---

### 6. Add the key to GitHub

1. Go to **GitHub → Settings**
2. Select **SSH and GPG keys**
3. Click **New SSH key**
4. Fill in:

Title

```
My Laptop
```

Key

Paste your copied key.

5. Click **Add SSH key**

---

### 7. Test the connection

```bash
ssh -T git@github.com
```

Expected output:

```
Hi username! You've successfully authenticated...
```

---

### 8. Clone repositories using SSH

Instead of the HTTPS URL:

```
https://github.com/user/repo.git
```

Use the SSH URL:

```
git@github.com:user/repo.git
```

Example:

```bash
git clone git@github.com:user/repo.git
```

---

## Windows

The steps are similar but use **PowerShell** or **Git Bash**.

---

### 1. Check if you already have an SSH key

Open **PowerShell** and run:

```powershell
ls $env:USERPROFILE\.ssh
```

Look for:

```
id_ed25519
id_ed25519.pub
```

If they exist, you can reuse them.

---

### 2. Generate a new SSH key

Run:

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

When prompted for the file location:

```
C:\Users\YourUser\.ssh\id_ed25519
```

Press **Enter** to accept the default.

Optionally set a passphrase.

---

### 3. Start the SSH agent

Enable and start the Windows SSH agent:

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

---

### 4. Add the key to the SSH agent

```powershell
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

---

### 5. Copy the public key

Display the key:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub
```

Copy the entire output.

Example:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

---

### 6. Add the key to GitHub

1. Open GitHub in your browser
2. Go to **Settings**
3. Select **SSH and GPG keys**
4. Click **New SSH key**
5. Paste your copied key
6. Click **Add SSH key**

---

### 7. Test the connection

Run:

```powershell
ssh -T git@github.com
```

Expected output:

```
Hi username! You've successfully authenticated...
```

---

## Troubleshooting

Check if the SSH agent is running:

```bash
ssh-add -l
```

Possible outputs:

```
The agent has no identities.
```

or

```
Could not open a connection to your authentication agent.
```

If needed, start the agent and add the key again.

---