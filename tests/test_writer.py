from pathlib import Path

from toc_generator.toc import SectionWithAnchorAndLevel, TOCFile, TOCFolder
from toc_generator.writer import write_toc_file, write_toc_on_files


def test_write_toc_file(tmp_path: Path):
    f = tmp_path / "doc.md"
    f.write_text("A\n<!-- TOC BEGIN -->\nold\n<!-- TOC END -->\nB")
    tocfile = TOCFile(file_full_path=f)
    tocfile.toc_entries.append(SectionWithAnchorAndLevel("sec", "#sec", 0))

    report = write_toc_file(tocfile)
    assert not report.errors
    content = f.read_text()
    assert "[sec](#sec)" in content


def test_write_toc_on_files(tmp_path: Path):
    # build minimal TOCFolder structure
    main = TOCFile(file_full_path=tmp_path / "main.md")
    sub = TOCFile(file_full_path=tmp_path / "sub.md")
    folder = TOCFolder(main_file_toc=main, files_toc=[sub])

    # create real files with markers
    (tmp_path / "main.md").write_text("X\n<!-- TOC BEGIN -->\nold\n<!-- TOC END -->")
    (tmp_path / "sub.md").write_text("Y\n<!-- TOC BEGIN -->\nold\n<!-- TOC END -->")

    report = write_toc_on_files(folder)
    assert not report.errors
