"""Top-level package for TOC generation utilities."""

from .cli import main
from .markdown_utils import (
    SectionWithAnchor,
    extract_level1_sections,
    read_markdown_file,
    replace_toc,
    section_to_anchor,
    sections_to_anchors,
)
from .report import Report
from .toc import (
    SectionWithAnchorAndLevel,
    TOCFile,
    TOCFolder,
    create_toc_tree,
    create_toc_tree_impl,
    print_toc_file,
    print_toc_tree,
)
from .tree import (
    CreateTreeResult,
    FileNode,
    FindSubFoldersResult,
    FolderNode,
    create_tree,
    find_markdown_files,
    find_subfolders,
    print_tree,
)
from .writer import write_toc_file, write_toc_on_files

__all__ = [
    "main",
    "Report",
    "replace_toc",
    "read_markdown_file",
    "extract_level1_sections",
    "SectionWithAnchor",
    "section_to_anchor",
    "sections_to_anchors",
    "FileNode",
    "FolderNode",
    "CreateTreeResult",
    "FindSubFoldersResult",
    "find_markdown_files",
    "find_subfolders",
    "create_tree",
    "print_tree",
    "SectionWithAnchorAndLevel",
    "TOCFile",
    "TOCFolder",
    "create_toc_tree_impl",
    "create_toc_tree",
    "print_toc_file",
    "print_toc_tree",
    "write_toc_file",
    "write_toc_on_files",
]
