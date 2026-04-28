from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .tree import FolderNode


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


# ------------------------------------------------------------------
# construction
# ------------------------------------------------------------------


def create_toc_tree_impl(rootPath: Path, node: FolderNode) -> TOCFolder:
    """
    Recursively build TOC structure from folder tree.
    """
    nodeTOC = TOCFolder(main_file_toc=TOCFile(file_full_path=rootPath / f"{node.main_filename}.md"))

    # ---- Folder own sections ----

    for section in node.main_file_sections:
        nodeTOC.main_file_toc.toc_entries.append(
            SectionWithAnchorAndLevel(
                section.section,
                f"{node.main_filename}.md#{section.anchor}",
                0,
            )
        )

    # ---- Subfolders ----
    subfoldersToc: List[SectionWithAnchorAndLevel] = []

    for subfolder in node.subfolders:
        sTOC_folder_node = create_toc_tree_impl(
            rootPath / subfolder.folder_name,
            subfolder,
        )

        nodeTOC.subfolder_toc.append(sTOC_folder_node)

        subfoldersToc.append(
            SectionWithAnchorAndLevel(
                f"{subfolder.folder_name}",
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
                    0,
                )
            )

        nodeTOC.files_toc.append(sTOC_file_node)

    # ---- Append subfolder entries ----
    for st in subfoldersToc:
        nodeTOC.main_file_toc.toc_entries.append(st)

    return nodeTOC


# ------------------------------------------------------------------
# finalization
# ------------------------------------------------------------------


def finalize_toc_tree(node: TOCFolder, parent: Optional[TOCFolder]) -> None:
    """
    Inject parent navigation entries into TOC recursively.
    """

    if parent is not None:
        parentEntry = SectionWithAnchorAndLevel(
            f"← Back : {parent.main_file_toc.file_full_path.stem}",
            f"../{parent.main_file_toc.file_full_path.name}",
            0,
        )
        node.main_file_toc.toc_entries = [parentEntry] + node.main_file_toc.toc_entries

    parentEntry = SectionWithAnchorAndLevel(
        f"← Back : {node.main_file_toc.file_full_path.stem}",
        f"{node.main_file_toc.file_full_path.name}",
        0,
    )

    for file_toc in node.files_toc:
        file_toc.toc_entries = [parentEntry] + file_toc.toc_entries

    for subfolder in node.subfolder_toc:
        finalize_toc_tree(subfolder, node)


def create_toc_tree(rootPath: Path, node: FolderNode) -> TOCFolder:
    """
    Build full TOC tree and finalize navigation links.
    """
    root = create_toc_tree_impl(rootPath, node)
    finalize_toc_tree(root, None)
    return root


# ------------------------------------------------------------------
# debugging helpers
# ------------------------------------------------------------------


def print_toc_file(node: TOCFile) -> None:
    """Debug utility to print a TOC file structure."""
    print(f"{node.file_full_path}")
    for s in node.toc_entries:
        print(f"{'  ' * s.level}- section: {s.section} anchor: {s.anchor}")
    print()


def print_toc_tree(node: TOCFolder) -> None:
    """Debug utility to print the full TOC tree structure."""
    print_toc_file(node.main_file_toc)
    for file_toc in node.files_toc:
        print_toc_file(file_toc)
    for subfolder in node.subfolder_toc:
        print_toc_tree(subfolder)
