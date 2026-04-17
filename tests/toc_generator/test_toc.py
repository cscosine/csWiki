from pathlib import Path

from toc_generator import toc
from toc_generator.tree import FolderNode


def make_dummy_foldernode():
    root = FolderNode(folder_name=Path(""), main_filename="index")
    root.main_file_sections = []
    # add one file
    child = FolderNode(folder_name=Path("sub"), main_filename="sub")
    root.subfolders.append(child)
    return root


def test_toc_tree_basic(tmp_path: Path):
    rootdir = tmp_path / "docs"
    rootdir.mkdir()
    # create files on filesystem only to compute paths later
    (rootdir / "index.md").write_text("# root")
    sub = rootdir / "sub"
    sub.mkdir()
    (sub / "sub.md").write_text("# sub")

    node = make_dummy_foldernode()
    toc_tree = toc.create_toc_tree(rootdir, node)
    # basic structure should include root and sub
    assert toc_tree.main_file_toc.file_full_path.name == "index.md"
    assert toc_tree.subfolder_toc

    # parent entries are prefixed
    assert any("../" in e.anchor for e in toc_tree.subfolder_toc[0].main_file_toc.toc_entries)
