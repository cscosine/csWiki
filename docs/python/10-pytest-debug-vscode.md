<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : python](python.md)
- [Debugging pytest in VS Code](#debugging-pytest-in-vs-code)
<!-- TOC END -->

# Debugging pytest in VS Code

## Recommended setup (if tests are not yet configured in VS Code)

1. Install pytest in your environment:
```
   pip install pytest
```

2. In VS Code:
   - Open Command Palette (Ctrl + Shift + P)
   - Run: "Python: Configure Tests"
   - Select pytest as the test framework
   - Choose your tests folder (e.g. tests)

3. Verify tests appear in the Testing panel (beaker icon)

---

## Debugging pytest 
The most reliable way to debug pytest in VS Code is using a launch configuration.

Create or edit:
```
.vscode/launch.json
```

and add:
```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "-s",
        # other options you might need
      ],
      "justMyCode": false
    }
  ]
}
```

---

## How to use it

1. Open the Run & Debug panel in VS Code
2. Select "Debug pytest"
3. Click Start Debugging (or press F5)
4. Execution will stop at breakpoints inside tests or code

---

## Notes

- "-s" → shows print output in console
- You can add/remove pytest flags in "args" as needed (e.g. --ignore, -m, etc.)
- Breakpoints must be set before launching the debugger
- This method works even if the Testing UI does not detect tests correctly

---

## Optional

If the Testing panel works properly, you can also right-click a test and use:
- "Debug Test" (no launch.json required)

However, the launch configuration is the most consistent method for full control.