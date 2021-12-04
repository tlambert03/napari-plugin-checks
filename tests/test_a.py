from pathlib import Path
from napari_plugin_checks import check_file
import pytest


def test_setup_cfg(capsys):
    setup_cfg = Path(__file__).parent / "bad_examples" / "setup.cfg"
    assert check_file(str(setup_cfg))
    captured = capsys.readouterr()
    assert "Forbidden dependency detected" in captured.out


def test_requirements(capsys):
    reqtxt = Path(__file__).parent / "bad_examples" / "requirements.txt"
    assert check_file(str(reqtxt))
    captured = capsys.readouterr()
    assert "Forbidden dependency detected" in captured.out


@pytest.mark.parametrize("fname", ["imports_pyqt5.py", "imports_pyside2.py"])
def test_bad_imports(fname, capsys):
    file = Path(__file__).parent / "bad_examples" / fname
    assert check_file(str(file))
    captured = capsys.readouterr()
    assert "Forbidden import detected" in captured.out
