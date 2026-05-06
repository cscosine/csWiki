import os
from pathlib import Path

import pytest

from toc_generator import cli


def test_cli_no_docs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # run the CLI in an empty directory, should produce an error but return 1
    cwd = tmp_path / "empty"
    cwd.mkdir()
    # create an empty docs folder so the command does not crash
    (cwd / "docs").mkdir()

    # monkeypatch cwd

    oldcwd = os.getcwd()
    try:
        os.chdir(cwd)
        ret = cli.main([])
        # there is no index.md so the command returns an error
        assert ret == 1
        captured = capsys.readouterr()
        assert "Cannot read" in captured.out
    finally:
        os.chdir(oldcwd)
