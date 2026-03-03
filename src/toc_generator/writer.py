from typing import List

from .markdown_utils import read_markdown_file, replace_toc
from .report import Report
from .toc import TOCFile, TOCFolder


def write_toc_file(node: TOCFile) -> Report:
    """
    Generate TOC markdown and inject it inside a file.
    """
    report = Report()

    lines: List[str] = ["## Table Of Contents"]

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
