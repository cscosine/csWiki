from dataclasses import dataclass, field
from pathlib import Path

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
    toc_entries: list[SectionWithAnchorAndLevel] = field(default_factory=list)


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
    files_toc: list[TOCFile] = field(default_factory=list)
    subfolder_toc: list["TOCFolder"] = field(default_factory=list)


# ------------------------------------------------------------------
# construction
# ------------------------------------------------------------------


def create_toc_tree_impl(root_path: Path, node: FolderNode) -> TOCFolder:
    """
    Recursively build TOC structure from folder tree.
    """
    node_toc = TOCFolder(main_file_toc=TOCFile(file_full_path=root_path / f"{node.main_filename}.md"))

    # ---- Folder own sections ----

    for section in node.main_file_sections:
        node_toc.main_file_toc.toc_entries.append(
            SectionWithAnchorAndLevel(
                section.section,
                f"{node.main_filename}.md#{section.anchor}",
                0,
            )
        )

    # ---- Subfolders ----
    subfolders_toc: list[SectionWithAnchorAndLevel] = []

    for subfolder in node.subfolders:
        subfolder_toc = create_toc_tree_impl(
            root_path / subfolder.folder_name,
            subfolder,
        )

        node_toc.subfolder_toc.append(subfolder_toc)

        subfolders_toc.append(
            SectionWithAnchorAndLevel(
                f"{subfolder.folder_name}",
                Path(subfolder.folder_name / f"{subfolder.main_filename}.md").as_posix(),
                0,
            )
        )

        for te in subfolder_toc.main_file_toc.toc_entries:
            subfolders_toc.append(
                SectionWithAnchorAndLevel(
                    te.section,
                    Path(subfolder.folder_name / te.anchor).as_posix(),
                    te.level + 1,
                )
            )

    # ---- Sibling files ----
    for nf in node.files:
        file_toc = TOCFile(file_full_path=root_path / f"{nf.file_name}.md")

        for s in nf.file_sections:
            file_toc.toc_entries.append(
                SectionWithAnchorAndLevel(
                    s.section,
                    f"#{s.anchor}",
                    0,
                )
            )

            node_toc.main_file_toc.toc_entries.append(
                SectionWithAnchorAndLevel(
                    s.section,
                    f"{nf.file_name}.md#{s.anchor}",
                    0,
                )
            )

        node_toc.files_toc.append(file_toc)

    # ---- Append subfolder entries ----
    for st in subfolders_toc:
        node_toc.main_file_toc.toc_entries.append(st)

    return node_toc


# ------------------------------------------------------------------
# finalization
# ------------------------------------------------------------------


def finalize_toc_tree(node: TOCFolder, parent: TOCFolder | None) -> None:
    """
    Inject parent navigation entries into TOC recursively.
    """

    if parent is not None:
        parent_entry = SectionWithAnchorAndLevel(
            f"← Back : {parent.main_file_toc.file_full_path.stem}",
            f"../{parent.main_file_toc.file_full_path.name}",
            0,
        )
        node.main_file_toc.toc_entries = [parent_entry] + node.main_file_toc.toc_entries

    parent_entry = SectionWithAnchorAndLevel(
        f"← Back : {node.main_file_toc.file_full_path.stem}",
        f"{node.main_file_toc.file_full_path.name}",
        0,
    )

    for file_toc in node.files_toc:
        file_toc.toc_entries = [parent_entry] + file_toc.toc_entries

    for subfolder in node.subfolder_toc:
        finalize_toc_tree(subfolder, node)


def create_toc_tree(root_path: Path, node: FolderNode) -> TOCFolder:
    """
    Build full TOC tree and finalize navigation links.
    """
    root = create_toc_tree_impl(root_path, node)
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
