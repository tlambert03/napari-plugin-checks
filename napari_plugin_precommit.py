import argparse
from typing import Optional, Sequence, Set, Tuple


def format_file(
    filename: str,
    *,
    min_py3_version: Tuple[int, int],
    max_py_version: Tuple[int, int],
) -> bool:
    ...


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--min-py3-version", type=str, default=(3, 6))
    parser.add_argument("--max-py-version", type=str, default=(3, 10))
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        if format_file(
            filename,
            min_py3_version=args.min_py3_version,
            max_py_version=args.max_py_version,
        ):
            print(f"Rewriting {filename}")
            retv = 1
    return retv


if __name__ == "__main__":
    raise SystemExit(main())
