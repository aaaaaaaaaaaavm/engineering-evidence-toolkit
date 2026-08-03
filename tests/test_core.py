import json
import tempfile
import unittest
from pathlib import Path

from engtrace import run
from engtrace.core import sha256


class EvidenceTests(unittest.TestCase):
    def project(self, root: Path) -> Path:
        (root / "result.json").write_text('{"x": 1.0}', encoding="utf-8")
        (root / "source.txt").write_text("input", encoding="utf-8")
        (root / "report.md").write_text(
            "# Report\n\n[Source](source.txt)\n",
            encoding="utf-8",
        )
        config = {
            "json": ["result.json"],
            "markdown": ["report.md"],
            "artifacts": [
                {
                    "path": "report.md",
                    "sha256": sha256(root / "report.md"),
                    "sources": ["source.txt"],
                }
            ],
        }
        (root / "engtrace.json").write_text(
            json.dumps(config),
            encoding="utf-8",
        )
        return root / "engtrace.json"

    def test_valid_project_holds(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run(self.project(Path(temp))), [])

    def test_changed_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            (Path(temp) / "report.md").write_text("changed", encoding="utf-8")
            self.assertTrue(
                any("artifact hash changed" in item for item in run(config))
            )

    def test_broken_link_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            (Path(temp) / "report.md").write_text(
                "[Missing](missing.txt)",
                encoding="utf-8",
            )
            self.assertTrue(any("broken link" in item for item in run(config)))

    def test_non_finite_json_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            (Path(temp) / "result.json").write_text(
                '{"x": NaN}',
                encoding="utf-8",
            )
            self.assertTrue(
                any("non-finite value" in item for item in run(config))
            )

    def test_missing_declared_source_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            data = json.loads(config.read_text(encoding="utf-8"))
            data["artifacts"][0]["sources"] = ["missing-source.txt"]
            config.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(
                any("missing source" in item for item in run(config))
            )

    def test_empty_pattern_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            data = json.loads(config.read_text(encoding="utf-8"))
            data["json"] = ["results/*.json"]
            config.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(
                any("no JSON files matched" in item for item in run(config))
            )
