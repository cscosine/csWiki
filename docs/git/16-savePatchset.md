<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : git](git.md)
- [Save And Apply Patchsets](#save-and-apply-patchsets)
<!-- TOC END -->

# Save And Apply Patchsets

In case, for example, you are unable to push a commit, you can save your last (or more) commit(s) to patchset (diff) and apply it later

generate the patchset for the last commit

```bash
git format-patch -1 HEAD --stdout > last-commit.patch
```

re-apply it with

```bash
git am last-commit.patch
```
