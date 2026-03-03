from pathlib import Path

from toc_generator import tree


def make_file(path: Path, text: str):
    path.write_text(text)


def test_find_markdown_files(tmp_path: Path):
    d = tmp_path
    (d / "a.md").write_text("# A")
    (d / "b.md").write_text("# B")
    files = tree.find_markdown_files(d, "a.md")
    assert files == ["b"]


def test_find_subfolders(tmp_path: Path, capsys):
    # create good and bad subfolders
    good = tmp_path / "good"
    bad = tmp_path / "bad"
    hidden = tmp_path / ".hidden"
    good.mkdir()
    bad.mkdir()
    hidden.mkdir()
    (good / "good.md").write_text("# Good")
    (bad / "something.md").write_text("# nope")

    res = tree.find_subfolders(tmp_path)
    assert Path("good") in res.paths
    assert any("Ignoring hidden" in msg for msg in res.report.infos)
    assert any("missing" in msg for msg in res.report.warnings)


def test_create_tree(tmp_path: Path):
    # build simple hierarchy
    root = tmp_path / "docs"
    root.mkdir()
    # index.md
    (root / "index.md").write_text("# Root")
    # sibling file
    (root / "other.md").write_text("# Other")
    # subfolder with its own file
    sub = root / "sub"
    sub.mkdir()
    (sub / "sub.md").write_text("# Sub")

    result = tree.create_tree(root, "index")
    assert result.root.main_filename == "index"
    assert any(f.file_name == "other" for f in result.root.files)
    assert any(sf.folder_name == Path("sub") for sf in result.root.subfolders)

    # error when main file missing
    missing = tmp_path / "nodocs"
    missing.mkdir()
    res2 = tree.create_tree(missing, "index")
    assert res2.report.errors
