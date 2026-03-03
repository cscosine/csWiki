#!/usr/bin/env python3

"""
Recursively scans the `docs/` folder and automatically generates
a navigable Table Of Contents inside markdown files.

It:
- Extracts level-1 headings (# ...)
- Builds a folder/file tree
- Generates TOC entries with anchors
- Injects them between:

    <!-- TOC BEGIN -->
    <!-- TOC END -->

Used inside pre-commit and CI.

Command line usage:
    python generateTOC.py

    Arguments:
        -q / --quiet flag to suppress debug output and only print errors/warnings.
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

# ============================================================
# Report System
# ============================================================


@dataclass
class Report:
    """
    Collects messages produced during tree creation and TOC writing.

    Attributes:
        errors: Critical issues that stop execution.
        warnings: Non-fatal issues that should be reviewed.
        infos: Informational messages for debugging and transparency.
    """

    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    infos: List[str] = field(default_factory=list)

    def append(self, other: "Report") -> None:
        """Merge another report into this one."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.infos.extend(other.infos)

    # ANSI styling for terminal output
    _RED = "\033[31m"
    _YELLOW = "\033[33m"
    _BLUE = "\033[34m"
    _RESET = "\033[0m"
    _BOLD = "\033[1m"

    def print(self) -> None:
        """Pretty-print the report with colors."""
        if not (self.errors or self.warnings or self.infos):
            return

        print(f"{self._YELLOW}{self._BOLD}---------- REPORT ----------{self._RESET}")
        self._print_block("ERROR", self.errors, self._RED, bold=True)
        self._print_block("WARNING", self.warnings, self._YELLOW, bold=True)
        self._print_block("INFO", self.infos, self._BLUE)
        print(f"{self._YELLOW}{self._BOLD}----------------------------{self._RESET}")

    def _print_block(
        self,
        label: str,
        messages: List[str],
        color: str,
        bold: bool = False,
    ) -> None:
        """Print a block of messages under a category."""
        if not messages:
            return

        style = self._BOLD if bold else ""
        for msg in messages:
            print(f"{color}{style}[{label}]{self._RESET} {msg}")


# ============================================================
# Markdown Utilities
# ============================================================


def replace_toc(content: str, toc: str) -> Tuple[str, bool]:
    """
    Replace the TOC block between:

        <!-- TOC BEGIN -->
        <!-- TOC END -->

    Returns:
        (updated_content, success_flag)
    """

    TOC_BEGIN = "<!-- TOC BEGIN -->"
    TOC_END = "<!-- TOC END -->"

    if TOC_BEGIN not in content or TOC_END not in content:
        return content, False

    pattern = re.compile(
        rf"{re.escape(TOC_BEGIN)}.*?{re.escape(TOC_END)}",
        re.DOTALL,
    )

    # keep replacement in a variable to avoid issues with backreferences in re.sub on windows
    replacement = f"{TOC_BEGIN}\n{toc}\n{TOC_END}"
    updated_content = re.sub(pattern, lambda _: replacement, content)
    return updated_content, True


def read_markdown_file(md_path: Path) -> str | None:
    """
    Read a markdown file safely.
    Returns None if file cannot be read.
    """
    try:
        return md_path.read_text(encoding="utf-8")
    except OSError:
        return None


def extract_level1_sections(content: str) -> List[str]:
    """
    Extract all level-1 headings:

        # Section Title

    Ignoring fenced code blocks (```).
    """
    sections = []
    in_code_block = False

    for line in content.splitlines():
        stripped = line.strip()

        # Toggle code block state
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        match = re.match(r"^# (.+)", stripped)
        if match:
            sections.append(match.group(1))

    return sections


# ============================================================
# Tree Structures
# ============================================================


@dataclass
class SectionWithAnchor:
    """
    Represents a markdown section heading converted into
    a clickable anchor link.

    Attributes:
        section: The raw section title extracted from markdown.
        anchor: The generated markdown anchor for linking.
    """

    section: str
    anchor: str


def section_to_anchor(section: str) -> SectionWithAnchor:
    """Convert a section title into a markdown anchor."""
    anchor = section.lower().replace(" ", "-")
    return SectionWithAnchor(section=section, anchor=anchor)


def sections_to_anchors(sections: List[str]) -> List[SectionWithAnchor]:
    """Convert multiple section titles into anchor objects."""
    return [section_to_anchor(s) for s in sections]


def find_markdown_files(folder: Path, excluded_name: str) -> List[str]:
    """
    Return all markdown filenames inside a folder,
    excluding the specified one.
    """
    return sorted([f.stem for f in folder.glob("*.md") if f.name != excluded_name])


@dataclass
class FindSubFoldersResult:
    """
    Result of scanning a folder for valid subfolders.

    Attributes:
        paths: List of valid subfolder paths.
        report: Messages generated during folder scanning.
    """

    paths: List[Path] = field(default_factory=list)
    report: Report = field(default_factory=Report)


def find_subfolders(folder: Path) -> FindSubFoldersResult:
    """
    Find valid subfolders.

    A subfolder is valid if:
    - It is not hidden (doesn't start with ".")
    - It contains a file named <folder_name>.md
    """
    result = FindSubFoldersResult()

    for sub in sorted(d for d in folder.iterdir() if d.is_dir()):
        if sub.name.startswith("."):
            result.report.infos.append(f"Ignoring hidden folder: `{sub.name}`")
            continue

        expected_md = sub / f"{sub.name}.md"

        if expected_md.is_file():
            result.paths.append(sub.relative_to(folder))
        else:
            result.report.warnings.append(f"Ignoring folder `{sub}` — missing `{sub.name}.md`")

    return result


@dataclass
class FileNode:
    """
    Represents a markdown file inside a folder.

    Attributes:
        file_name: Filename without extension.
        file_sections: Extracted level-1 sections from the file.
    """

    file_name: str
    file_sections: List[SectionWithAnchor] = field(default_factory=list)


@dataclass
class FolderNode:
    """
    Represents a folder in the docs tree.

    Each folder contains:
    - A mandatory main markdown file
    - Optional sibling markdown files
    - Optional subfolders (recursive)

    Attributes:
        folder_name: Relative folder path.
        main_filename: Name of the main markdown file.
        main_file_sections: Sections extracted from the main file.
        subfolders: Nested folder nodes.
        files: Markdown files inside this folder.
    """

    folder_name: Path
    main_filename: str
    main_file_sections: List[SectionWithAnchor] = field(default_factory=list)
    subfolders: List["FolderNode"] = field(default_factory=list)
    files: List[FileNode] = field(default_factory=list)


@dataclass
class CreateTreeResult:
    """
    Result of building the folder tree.

    Attributes:
        root: Root folder node of the docs tree.
        report: Messages produced during tree scanning.
    """

    root: FolderNode
    report: Report


# ============================================================
# Tree Construction
# ============================================================


def createTree(rootPath: Path, main_filename: str) -> CreateTreeResult:
    """
    Build an in-memory representation of the docs folder.
    Extract headings, files and subfolders recursively.
    """

    report = Report()
    root_node = FolderNode(folder_name=Path(""), main_filename=main_filename)

    nodes_to_explore = [(root_node, rootPath)]

    for node, current_path in nodes_to_explore:
        # ---- Main file ----
        main_file_path = current_path / f"{node.main_filename}.md"
        content = read_markdown_file(main_file_path)

        if content is None:
            report.errors.append(f"Cannot read {main_file_path}")
        else:
            node.main_file_sections = sections_to_anchors(extract_level1_sections(content))

        # ---- Sibling markdown files ----
        files = find_markdown_files(
            current_path,
            f"{node.main_filename}.md",
        )

        for filename in files:
            file_node = FileNode(file_name=filename)
            file_path = current_path / f"{filename}.md"

            content = read_markdown_file(file_path)

            if content is None:
                report.errors.append(f"Cannot read {file_path}")
            else:
                file_node.file_sections = sections_to_anchors(extract_level1_sections(content))

            node.files.append(file_node)

        # ---- Subfolders ----
        subfolders = find_subfolders(current_path)
        report.append(subfolders.report)

        for sub in subfolders.paths:
            folder_node = FolderNode(
                folder_name=Path(sub),
                main_filename=str(sub),
            )
            node.subfolders.append(folder_node)
            nodes_to_explore.append((folder_node, current_path / folder_node.folder_name))

    return CreateTreeResult(root_node, report)


def printTree(node: FolderNode, indent: str) -> None:
    """Debug utility to print the folder tree structure."""
    print(f"{indent}- folder: {node.folder_name} main_file: {node.main_filename}")
    for sa in node.main_file_sections:
        print(f"{indent}  * section: {sa.section} anchor: {sa.anchor}")
    for f in node.files:
        print(f"{indent}  - file: {f.file_name}")
        for sa in f.file_sections:
            print(f"{indent}    * section: {sa.section} anchor: {sa.anchor}")
    for s in node.subfolders:
        printTree(s, indent + "  ")


# ============================================================
# TOC Generation & Writing
# ============================================================


@dataclass
class SectionWithAnchorAndLevel:
    section: str
    anchor: str
    level: int


@dataclass
class TOCFile:
    """
    Represents the TOC of a single markdown file.

    Attributes:
        file_full_path: Absolute path to the file.
        toc_entries: List of generated TOC entries.
    """

    file_full_path: Path
    toc_entries: List[SectionWithAnchorAndLevel] = field(default_factory=list)


@dataclass
class TOCFolder:
    """
    Represents the TOC of a folder.

    Attributes:
        main_file_toc: TOC for the folder main file.
        files_toc: TOCs for sibling markdown files.
        subfolder_toc: Nested folder TOCs.
    """

    main_file_toc: TOCFile
    files_toc: List[TOCFile] = field(default_factory=list)
    subfolder_toc: List["TOCFolder"] = field(default_factory=list)


def createTOCTreeImpl(rootPath: Path, node: FolderNode) -> TOCFolder:
    """
    Recursively build TOC structure from folder tree.
    """

    nodeTOC = TOCFolder(main_file_toc=TOCFile(file_full_path=rootPath / f"{node.main_filename}.md"))

    # ---- Folder own sections ----
    nodeTOC.main_file_toc.toc_entries.append(
        SectionWithAnchorAndLevel(
            f"Main file {node.main_filename}",
            Path(f"{node.main_filename}.md").as_posix(),
            0,
        )
    )

    for section in node.main_file_sections:
        nodeTOC.main_file_toc.toc_entries.append(
            SectionWithAnchorAndLevel(
                section.section,
                f"{node.main_filename}.md#{section.anchor}",
                1,
            )
        )

    # ---- Subfolders ----
    subfoldersToc = []

    for subfolder in node.subfolders:
        sTOC_folder_node = createTOCTreeImpl(
            rootPath / subfolder.folder_name,
            subfolder,
        )

        nodeTOC.subfolder_toc.append(sTOC_folder_node)

        subfoldersToc.append(
            SectionWithAnchorAndLevel(
                f"Subfolder {subfolder.folder_name}",
                Path(subfolder.folder_name / f"{subfolder.main_filename}.md").as_posix(),
                0,
            )
        )

        for te in sTOC_folder_node.main_file_toc.toc_entries:
            subfoldersToc.append(
                SectionWithAnchorAndLevel(
                    te.section,
                    Path(subfolder.folder_name / te.anchor).as_posix(),
                    te.level + 1,
                )
            )

    # ---- Sibling files ----
    for nf in node.files:
        sTOC_file_node = TOCFile(file_full_path=rootPath / f"{nf.file_name}.md")

        nodeTOC.main_file_toc.toc_entries.append(
            SectionWithAnchorAndLevel(
                f"File {nf.file_name}",
                f"{nf.file_name}.md",
                0,
            )
        )

        for s in nf.file_sections:
            sTOC_file_node.toc_entries.append(
                SectionWithAnchorAndLevel(
                    s.section,
                    f"#{s.anchor}",
                    0,
                )
            )

            nodeTOC.main_file_toc.toc_entries.append(
                SectionWithAnchorAndLevel(
                    s.section,
                    f"{nf.file_name}.md#{s.anchor}",
                    1,
                )
            )

        nodeTOC.files_toc.append(sTOC_file_node)

    # ---- Append subfolder entries ----
    for st in subfoldersToc:
        nodeTOC.main_file_toc.toc_entries.append(st)

    return nodeTOC


def finalizeTOCTree(node: TOCFolder, parent: TOCFolder | None) -> None:
    """
    Inject parent navigation entries into TOC recursively.
    """

    if parent is not None:
        parentEntry = SectionWithAnchorAndLevel(
            f"../{parent.main_file_toc.file_full_path.stem}",
            f"../{parent.main_file_toc.file_full_path.name}",
            0,
        )
        node.main_file_toc.toc_entries = [parentEntry] + node.main_file_toc.toc_entries

    parentEntry = SectionWithAnchorAndLevel(
        f"../{node.main_file_toc.file_full_path.stem}",
        f"{node.main_file_toc.file_full_path.name}",
        0,
    )

    for file_toc in node.files_toc:
        file_toc.toc_entries = [parentEntry] + file_toc.toc_entries

    for subfolder in node.subfolder_toc:
        finalizeTOCTree(subfolder, node)


def createTOCTree(rootPath: Path, node: FolderNode) -> TOCFolder:
    """
    Build full TOC tree and finalize navigation links.
    """
    root = createTOCTreeImpl(rootPath, node)
    finalizeTOCTree(root, None)
    return root


def printTOCFile(node: TOCFile) -> None:
    """Debug utility to print a TOC file structure."""
    print(f"{node.file_full_path}")
    for s in node.toc_entries:
        print(f"{'  ' * s.level}- section: {s.section} anchor: {s.anchor}")
    print()


def printTOCTree(node: TOCFolder) -> None:
    """Debug utility to print the full TOC tree structure."""
    printTOCFile(node.main_file_toc)
    for file_toc in node.files_toc:
        printTOCFile(file_toc)
    for subfolder in node.subfolder_toc:
        printTOCTree(subfolder)


# ============================================================
# Writing TOC to Files
# ============================================================


def write_toc_file(node: TOCFile) -> Report:
    """
    Generate TOC markdown and inject it inside a file.
    """
    report = Report()

    lines = ["## Table Of Contents"]

    for s in node.toc_entries:
        indent = "  " * s.level
        lines.append(f"{indent}- [{s.section}]({s.anchor})")

    toc_string = "\n".join(lines)

    existing_content = read_markdown_file(node.file_full_path)

    if existing_content is None:
        report.errors.append(f"Error reading {node.file_full_path}")
    else:
        updated_content, success = replace_toc(
            existing_content,
            toc_string,
        )

        if not success:
            report.warnings.append(f"No TOC section found in {node.file_full_path}")

        try:
            node.file_full_path.write_text(
                updated_content,
                encoding="utf-8",
            )
        except OSError:
            report.errors.append(f"Error writing to {node.file_full_path}")

    return report


def write_toc_on_files(node: TOCFolder) -> Report:
    """
    Recursively write TOCs for:
    - Main file
    - Sibling files
    - Subfolders
    """

    report = write_toc_file(node.main_file_toc)

    for f in node.files_toc:
        report.append(write_toc_file(f))

    for subfolder in node.subfolder_toc:
        report.append(write_toc_on_files(subfolder))

    return report


# ============================================================
# Main Entry Point
# ============================================================


def main() -> int:
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

    args = parser.parse_args()

    quiet = args.quiet

    if not quiet:
        print("🚀 Generating full recursive TOCs...\n", flush=True)

    root = Path("./docs")

    tree = createTree(rootPath=root, main_filename="index")
    if not quiet:
        printTree(tree.root, "")

    if tree.report.errors:
        tree.report.print()
        print("\033[31m❌ Errors during tree generation.\033[0m")
        return 1

    toc_tree = createTOCTree(rootPath=root, node=tree.root)

    if not quiet:
        # Optional debug:
        print()
        print("📚 Generated TOC tree structure.\n")
        printTOCTree(toc_tree)

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
