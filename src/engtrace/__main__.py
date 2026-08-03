from __future__ import annotations

import argparse
from pathlib import Path

from .core import run


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a declared computational-engineering evidence chain"
    )
    parser.add_argument("config", type=Path)
    args = parser.parse_args()

    failures = run(args.config)
    if failures:
        print("evidence checks failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("evidence checks hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
