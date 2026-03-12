from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

from .markdown_utils import (
    SectionWithAnchor,
    extract_level1_sections,
    read_markdown_file,
    sections_to_anchors,
)
from .report import Report


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


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------


def find_markdown_files(folder: Path, excluded_name: str) -> List[str]:
    """
    Return all markdown filenames inside a folder,
    excluding the specified one.
    """
    return sorted([f.stem for f in folder.glob("*.md") if f.name != excluded_name])


# ------------------------------------------------------------------
# tree construction
# ------------------------------------------------------------------


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
            result.report.warnings.append(f"Ignoring folder `{sub}` - missing `{sub.name}.md`")

    return result


def create_tree(rootPath: Path, main_filename: str) -> CreateTreeResult:
    """
    Build an in-memory representation of the docs folder.
    Extract headings, files and subfolders recursively.
    """

    report = Report()
    root_node = FolderNode(folder_name=Path(""), main_filename=main_filename)

    nodes_to_explore: List[Tuple[FolderNode, Path]] = [(root_node, rootPath)]

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


# ------------------------------------------------------------------
# debugging helpers
# ------------------------------------------------------------------


def print_tree(node: FolderNode, indent: str = "") -> None:
    """Debug utility to print the folder tree structure."""
    print(f"{indent}- folder: {node.folder_name} main_file: {node.main_filename}")
    for sa in node.main_file_sections:
        print(f"{indent}  * section: {sa.section} anchor: {sa.anchor}")
    for f in node.files:
        print(f"{indent}  - file: {f.file_name}")
        for sa in f.file_sections:
            print(f"{indent}    * section: {sa.section} anchor: {sa.anchor}")
    for s in node.subfolders:
        print_tree(s, indent + "  ")
