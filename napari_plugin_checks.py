"""Set of sanity checks for napari plugin

use as a pre-commit hook, or command line interface.
"""

import argparse
import logging
import re
from configparser import ConfigParser
from fnmatch import fnmatch
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Set, Tuple


logging.getLogger("grimp").setLevel(logging.ERROR)

Str2Bool = Callable[[str], bool]
CHECKERS: List[Tuple[Str2Bool, Str2Bool]] = []
BASE_NAME_REGEX = re.compile(r"[^!=><\s@~]+")
REQ_REGEX = re.compile(r"(===|==|!=|~=|>=?|<=?|@)\s*([^,]+)")
qtpy_message = "use Qt compatibility library, like qtpy"
FORBIDDEN_REQUIRES = {
    "pyqt": qtpy_message,
    "pyqt5": qtpy_message,
    "pyside": qtpy_message,
    "pyside2": qtpy_message,
    "pyside6": qtpy_message,
    "pyqt6": qtpy_message,
}
FORBIDDEN_IMPORTS = {
    "PyQt5": qtpy_message,
    "PyQt6": qtpy_message,
    "PySide2": qtpy_message,
    "PySide6": qtpy_message,
}


def match(pattern: str) -> Callable[[Str2Bool], Str2Bool]:
    """decorator that declares a checker for a filepattern:

    Examples
    --------
        @match("setup.cfg")
        def check_setup_cfg(fname: str) -> bool:
            ...
    """

    def deco(f: Str2Bool) -> Str2Bool:
        def _check_name(fname: str) -> bool:
            if "/" not in pattern and "*" not in pattern:
                return fname.endswith(pattern)
            return fnmatch(fname, pat=pattern)

        CHECKERS.append((_check_name, f))
        return f

    return deco


def _req_base(req: str) -> str:
    basem = re.match(BASE_NAME_REGEX, req.split(";")[0])
    return basem.group(0).strip() if basem else ""


@match("setup.cfg")
def check_setup_cfg(fname: str) -> bool:
    cfg = ConfigParser()
    cfg.read(fname)

    retv = False
    requires = cfg.get("options", "install_requires", fallback="").strip().splitlines()
    if requires:

        # check for Forbidden dependencies, like PyQt5, etc...
        for req in requires:
            lib = _req_base(req)
            err = FORBIDDEN_REQUIRES.get(lib.lower())
            if err:
                print(f"Forbidden dependency detected in setup.cfg ({lib!r}): {err}")
                retv = True

    return retv


@match("requirements.txt")
def check_requirements_txt(fname: str) -> bool:
    retv = False
    for line in Path(fname).read_text().strip().splitlines():
        lib = _req_base(line)
        err = FORBIDDEN_REQUIRES.get(lib.lower())
        if err:
            print(f"Forbidden dependency detected in requirements.txt ({lib!r}): {err}")
            retv = True
    return retv


@match("*.py")
def check_py(fname: str) -> bool:
    return _check_imports(fname)


def _check_imports(fname: str) -> bool:
    from grimp.adaptors import filesystem, importscanner
    from grimp.domain.valueobjects import Module

    p = Path(fname)
    if not p.parent or str(p.parent) == ".":
        return False
    root = p.parent
    module = Module(f"{p.parent.name}.{p.name[:-3]}")
    fs = filesystem.FileSystem()
    scanner = importscanner.ImportScanner({root: {module}}, fs, True)

    imports = scanner.scan_for_imports(module=module)
    retv = False
    for imp in imports:
        err = FORBIDDEN_IMPORTS.get(imp.imported.name)
        if err:
            print(
                f"Forbidden import detected ({imp.imported.name!r}) in {fname!r}: {err}"
            )
            retv = True

    return retv


def check_file(filename: str) -> bool:
    for checker, function in CHECKERS:
        if checker(filename):
            # the first checker wins, and must dispatch to others manually if desired.
            return function(filename)
    return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", default=["."])
    args = parser.parse_args(argv)

    for name in list(args.filenames):
        p = Path(name)
        if p.is_dir():
            args.filenames.remove(name)
            args.filenames.extend(
                [
                    str(f)
                    for f in p.glob("**/*")
                    if f.is_file()
                    if not str(f).startswith(".")
                ]
            )

    return sum(check_file(filename) for filename in args.filenames)


if __name__ == "__main__":
    raise SystemExit(main())
