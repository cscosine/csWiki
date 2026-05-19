<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : vscode](vscode.md)
- [Source Control - Repositories: Settings](#source-control---repositories:-settings)
<!-- TOC END -->

# Source Control - Repositories: Settings

If the `Source Control - Repositories` panel does not show all repos in subfolders, try

- Open Settings `(Ctrl+,)` and search for `Git: Auto Repository Detection`

- Set it to

    ```
    "git.autoRepositoryDetection": true
    ```

- Search settings for `Git: Repository Scan Max Depth` and increase it if repos are nested deeper:

    ```
    "git.repositoryScanMaxDepth": 5
    ```
- Then Reload with `Ctrl+Shift+P`

    ```
    Developer: Reload Window
    ```
