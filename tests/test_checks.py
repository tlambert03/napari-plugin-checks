from pathlib import Path

import pytest
from napari_plugin_checks import check_file, main

BAD = Path(__file__).parent / "bad_examples"
GOOD = Path(__file__).parent / "good_examples"


def test_setup_cfg(capsys):
    assert check_file(str(BAD / "setup.cfg"))
    captured = capsys.readouterr()
    assert "Forbidden dependency detected" in captured.out


def test_requirements(capsys):
    assert check_file(str(BAD / "requirements.txt"))
    captured = capsys.readouterr()
    assert "Forbidden dependency detected" in captured.out


def test_fine_file():
    assert check_file(str(GOOD / "boring.py")) is False


def test_unknown_file():
    assert check_file("asdfkjfadsf.asdf") is False


@pytest.mark.parametrize("fname", ["imports_pyqt5.py", "imports_pyside2.py"])
def test_bad_imports(fname, capsys):
    assert check_file(str(BAD / fname))
    captured = capsys.readouterr()
    assert "Forbidden import detected" in captured.out


def test_main():
    assert main([str(BAD), str(GOOD)]) == len(list(BAD.iterdir()))
