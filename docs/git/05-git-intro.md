<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [A Gentle And Quick Git Introduction](#a-gentle-and-quick-git-introduction)
<!-- TOC END -->

# A Gentle And Quick Git Introduction

This page incorporates text and images from Pro Git by Scott Chacon and Ben Straub - https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control

Source: https://git-scm.com/book/en/v2
License: CC BY-NC-SA 3.0
https://creativecommons.org/licenses/by-nc-sa/3.0/

## Concepts

- Git is a `Distributed Version Control Systems (DVCS)`

  - When you `clone` the repo locally, you have a full copy
  - i.e., if the server dies, you still have your work!
  - therefore, supporting several `remotes` is a natural fact

  ![Git DVCS](images/git-distributed-system.png)
  *The Git DVCS model - from https://git-scm.com/book/en/v2/images/distributed.png*

- Linus Torvalds, the creator of Linux, developed it in 2005 after BitKeeper broke down.

- Goals:

  - Speed
  - Simple
  - Scalable (e.g. N > 1000 branches - large projects as Linux)
  - Fully distributed

- Git contains `snapshots`

  - every `commit` is a `picture` of the files
  - efficient: if file A never changes, it is just referenced

  ![Git snapshots](images/git-snapshots.png)
  *The Git Snapshots - from https://git-scm.com/book/en/v2/images/snapshots.png*

- Operations are (almost always) Local

  - no need for remote access / connection / server to operate on a git repo
  - it is fully available locally and all commands, apart the remote ones, works!
  - e.g. you can work in the train / airplane
  - all the story is available (*unless your copy is `shallow` [partial])

- Commit has a unique id: the SHA-1

  - is a `checksum`
  - if a single char changes, the checksum changes
  - SHA-1: 40 chars hex (0-9 a-f)
  - e.g. `24b9da6552252987aa493b52f8696cd6d3b00373`

- You can't loose data (... almost)

  - after a `commit`, obviously you loose if you do not commit
  - even better if you `push` remotely

- The three states: **the main git concept**

  each file can be in one of those 3 states

  - **Modified**: you edit it, but you haven't committed
  - **Staged**: the edits to the file are marked as part of the _next_ commit
  - **Committed**: safely stored, ready for next edits!

  Note: all _locally_, no remote involved so far

  ![Git 3 states](images/git-3states.png)
  *The Git 3 states - from https://git-scm.com/book/en/v2/images/areas.png*

  `working directory`

  - contains your files
  - and `.git` special folder

  `staging area`

  - the temporary location that contains what you want to go in your next commit

  `.git`

  - is where the git really is stored

  Typical workflow

  - edit files
  - mark them as `staged` (`add`)
  - then commit the staged elements

  note: can be partial, I can stage `fileA` but not `fileB`

  Again: note this is all local!

- File status

  ![Git File Status](images/git-file-status.png)
  *The Git File Status - from https://git-scm.com/book/en/v2/images/lifecycle.png*

  - Note: untracked (new) files are not added by default
  - Rename: normally detected automatically if file content is similar

- Branching

  - a `branch` is just a label attached to a commit (SHA)
  - it does not exist any special branch / branch name
  - a `branch` can be created everywhere

    - e.g. I can get the very first commit and attach a label (`branch`) `restartFromScratch` and branch out from there

  - `branch`es are convenient way of organizing work

    - different contributors
    - different efforts / features (e.g. `add-tests` `new-app`)

  - branch can be deleted, commits remains (with some caveats - delete a `leaf branch` is a bit dangerous )

  - `HEAD` is a special reference, it tells you what is the status of your working dir

## Branches and Branching

  *images from https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell*

  Note: history goes left (older) to right (newer) - arrows are somehow misleading, they indicate the parent commit

  - we are on `master` and we create a branch `testing`:

    - two labels attached to the same commit,
    - `HEAD` is on `master`, our current active branch

    ![Git File Status](images/git-branches-02.png)

  - we switch active branch to `testing` (`checkout`)

    - `HEAD` is on `testing`

    ![Git File Status](images/git-branches-03.png)

  - we do some work and we commit

    - `HEAD` is on `testing`, on a new commit

    ![Git File Status](images/git-branches-04.png)

  - we `checkout` again `master`

    - `HEAD` is on `master`, our current active branch
    - `testing` is stored, no risk

    ![Git File Status](images/git-branches-05.png)

  - we do some work and we commit

    - `HEAD` is on `master`, on a new commit,
    - and now is clear why we call it `branch`

    ![Git File Status](images/git-branches-06.png)

*Note*: omitting `DETACHED_HEAD` cases, not really interesting...

## Practical

## Setup

Not going to a full setup guide here, but only through concepts

- git requires you to provide a `name` and an `email` to annotate your commits

**TODO**: continue from https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History, note 3.1 branching already done
