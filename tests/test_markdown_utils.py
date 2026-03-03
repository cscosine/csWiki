from pathlib import Path

from toc_generator import markdown_utils as mu


def test_extract_level1_sections_and_ignore_code():
    content = """
# First
Some text
```
# not a heading
```
# Second
    """
    sections = mu.extract_level1_sections(content)
    assert sections == ["First", "Second"]


def test_replace_toc_missing_markers():
    content = "no markers here"
    updated, ok = mu.replace_toc(content, "foo")
    assert not ok
    assert updated == content


def test_replace_toc_success(tmp_path: Path):
    file = tmp_path / "doc.md"
    file.write_text("line1\n<!-- TOC BEGIN -->\nold\n<!-- TOC END -->\nline2")
    content = file.read_text()
    updated, ok = mu.replace_toc(content, "newtoc")
    assert ok
    assert "newtoc" in updated


def test_section_anchor_helpers():
    s = "My Section"
    anchor = mu.section_to_anchor(s)
    assert anchor.section == s
    assert anchor.anchor == "my-section"

    multiple = mu.sections_to_anchors(["A", "B"])
    assert [x.section for x in multiple] == ["A", "B"]
