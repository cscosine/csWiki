import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


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


def read_markdown_file(md_path: Path) -> Optional[str]:
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
    sections: List[str] = []
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
