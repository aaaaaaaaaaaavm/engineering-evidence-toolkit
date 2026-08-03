from __future__ import annotations

import argparse
from .core import run


def main() -> int:
    parser = argparse.ArgumentParser(description="Check computational engineering evidence")
    parser.add_argument("config")
    args = parser.parse_args()
    failures = run(args.config)
    if failures:
        print("evidence checks failed")
        for failure in failures: print(f"- {failure}")
        return 1
    print("evidence checks hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
