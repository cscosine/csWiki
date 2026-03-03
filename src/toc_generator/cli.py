import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .report import Report
from .toc import create_toc_tree, print_toc_tree
from .tree import create_tree, print_tree
from .writer import write_toc_on_files


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Script entry point.

    Returns:
        0 on success
        1 on error
    """
    parser = argparse.ArgumentParser(description="Generate recursive TOCs for docs/")

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Run without printing debug information",
    )

    args = parser.parse_args(argv)

    quiet = args.quiet

    if not quiet:
        print("🚀 Generating full recursive TOCs...\n", flush=True)

    root = Path("./docs")

    # early exit if docs directory does not exist
    if not root.is_dir():
        r = Report()
        r.errors.append(f"docs directory not found: {root}")
        r.print()
        print("\033[31m❌ Errors during tree generation.\033[0m")
        return 1

    tree = create_tree(rootPath=root, main_filename="index")
    if not quiet:
        print_tree(tree.root, "")

    if tree.report.errors:
        tree.report.print()
        print("\033[31m❌ Errors during tree generation.\033[0m")
        return 1

    toc_tree = create_toc_tree(rootPath=root, node=tree.root)

    if not quiet:
        # Optional debug:
        print()
        print("📚 Generated TOC tree structure.\n")
        print_toc_tree(toc_tree)

    write_report = write_toc_on_files(toc_tree)
    tree.report.append(write_report)

    tree.report.print()

    if tree.report.errors:
        print("\033[31m❌ Errors during TOC write.\033[0m")
        return 1

    if not quiet:
        print("\033[32m✅ Execution completed successfully.\033[0m", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
