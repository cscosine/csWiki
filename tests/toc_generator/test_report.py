def test_report_append_and_print(capfd):
    from toc_generator.report import Report

    r1 = Report()
    r1.errors.append("fail")
    r1.warnings.append("be careful")
    r1.infos.append("info")

    r2 = Report()
    r2.errors.append("another")
    r1.append(r2)

    # capture output
    r1.print()
    captured = capfd.readouterr()
    text = captured.out
    # remove ANSI escapes for easier assertions
    import re

    clean = re.sub(r"\x1b\[[0-9;]*m", "", text)

    assert "[ERROR] fail" in clean
    assert "[ERROR] another" in clean
    assert "[WARNING] be careful" in clean
    assert "[INFO] info" in clean

    # printing empty report should be silent
    empty = Report()
    empty.print()
    captured = capfd.readouterr()
    assert captured.out == ""
