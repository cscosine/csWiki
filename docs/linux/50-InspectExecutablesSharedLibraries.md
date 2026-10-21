<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : linux](linux.md)
- [Inspect Executables For Shared Libraries](#inspect-executables-for-shared-libraries)
<!-- TOC END -->

# Inspect Executables For Shared Libraries

Verify used libraries and where are them

```bash
EXEC=path-to-your-executable

ldd $EXEC

ldd $EXEC | grep 'not found'
```

Inspect the executable's embedded paths:

```bash
EXEC=path-to-your-executable

readelf -d $EXEC | grep -E 'RPATH|RUNPATH'

readelf -d $EXEC
```
