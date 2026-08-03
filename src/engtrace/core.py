"""Traceability checks for computational engineering repositories.

A pass from this module has a deliberately narrow meaning: declared JSON values are finite,
declared local Markdown links resolve, and declared artifacts still have the recorded bytes
and source files. None of those checks validates the equation that produced a result.

The failure paths matter as much as the clean path. In particular, a declared file pattern
that matches nothing is an error. Treating an empty check as success is how a misspelling turns
evidence into ceremony.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def sha256(path: Path) -> str:
    """Return the SHA-256 identity of a file without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def finite_json(path: Path) -> list[str]:
    """Report every NaN or infinity accepted by Python's permissive JSON reader."""
    failures: list[str] = []
    value = json.loads(path.read_text(encoding="utf-8"))

    def walk(item: Any, location: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                walk(child, f"{location}.{key}")
        elif isinstance(item, list):
            for index, child in enumerate(item):
                walk(child, f"{location}[{index}]")
        elif (
            isinstance(item, (int, float))
            and not isinstance(item, bool)
            and not math.isfinite(item)
        ):
            failures.append(f"non-finite value: {location}")

    walk(value, str(path))
    return failures


def relative_links(path: Path, root: Path) -> list[str]:
    """Report missing local Markdown targets; external URLs are outside this check."""
    failures: list[str] = []
    for raw in _MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
        target = raw.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (
            root / target.lstrip("/")
            if target.startswith("/")
            else path.parent / target
        )
        if not resolved.exists():
            failures.append(
                f"broken link: {path.relative_to(root)} -> {raw}"
            )
    return failures


def _matched(root: Path, pattern: str, kind: str, failures: list[str]) -> list[Path]:
    """Expand one declared pattern and fail closed if it selects no evidence."""
    paths = sorted(root.glob(pattern))
    if not paths:
        failures.append(f"no {kind} files matched: {pattern}")
    return paths


def run(config_path: str | Path) -> list[str]:
    """Run all checks declared by one `engtrace.json` file."""
    config_path = Path(config_path).resolve()
    root = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    for pattern in config.get("json", []):
        for path in _matched(root, pattern, "JSON", failures):
            failures.extend(finite_json(path))

    for pattern in config.get("markdown", []):
        for path in _matched(root, pattern, "Markdown", failures):
            failures.extend(relative_links(path, root))

    for item in config.get("artifacts", []):
        artifact = root / item["path"]
        if not artifact.is_file():
            failures.append(f"missing artifact: {item['path']}")
        elif sha256(artifact) != item["sha256"]:
            failures.append(f"artifact hash changed: {item['path']}")

        for source in item.get("sources", []):
            if not (root / source).is_file():
                failures.append(f"missing source: {source}")

    return failures
