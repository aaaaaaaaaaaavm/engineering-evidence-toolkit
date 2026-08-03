"""Traceability checks for computational engineering repositories."""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def finite_json(path: Path) -> list[str]:
    failures: list[str] = []
    value = json.loads(path.read_text(encoding="utf-8"))
    def walk(item, location):
        if isinstance(item, dict):
            for key, child in item.items(): walk(child, f"{location}.{key}")
        elif isinstance(item, list):
            for index, child in enumerate(item): walk(child, f"{location}[{index}]")
        elif isinstance(item, (int, float)) and not isinstance(item, bool) and not math.isfinite(item):
            failures.append(f"non-finite value: {location}")
    walk(value, str(path))
    return failures


def relative_links(path: Path, root: Path) -> list[str]:
    failures = []
    for raw in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        target = raw.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = root / target.lstrip("/") if target.startswith("/") else path.parent / target
        if not resolved.exists(): failures.append(f"broken link: {path.relative_to(root)} -> {raw}")
    return failures


def run(config_path: str | Path) -> list[str]:
    config_path = Path(config_path).resolve()
    root = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    for pattern in config.get("json", []):
        for path in root.glob(pattern): failures.extend(finite_json(path))
    for pattern in config.get("markdown", []):
        for path in root.glob(pattern): failures.extend(relative_links(path, root))
    for item in config.get("artifacts", []):
        artifact = root / item["path"]
        if not artifact.is_file(): failures.append(f"missing artifact: {item['path']}")
        elif sha256(artifact) != item["sha256"]: failures.append(f"artifact hash changed: {item['path']}")
        for source in item.get("sources", []):
            if not (root / source).is_file(): failures.append(f"missing source: {source}")
    return failures
