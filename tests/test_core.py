import json
import tempfile
import unittest
from pathlib import Path

from engtrace import run
from engtrace.core import sha256


class EvidenceTests(unittest.TestCase):
    def project(self, root: Path):
        (root / "result.json").write_text('{"x": 1.0}')
        (root / "source.txt").write_text('input')
        (root / "report.md").write_text('# Report\n\n[Source](source.txt)\n')
        config = {
            "json": ["*.json"], "markdown": ["*.md"],
            "artifacts": [{"path": "report.md", "sha256": sha256(root / "report.md"), "sources": ["source.txt"]}],
        }
        (root / "engtrace.json").write_text(json.dumps(config))
        return root / "engtrace.json"

    def test_valid_project_holds(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run(self.project(Path(temp))), [])

    def test_changed_artifact_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            (Path(temp) / "report.md").write_text('changed')
            self.assertTrue(any('artifact hash changed' in item for item in run(config)))

    def test_broken_link_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            config = self.project(Path(temp))
            (Path(temp) / "report.md").write_text('[Missing](missing.txt)')
            data = json.loads(config.read_text())
            data["artifacts"] = []
            config.write_text(json.dumps(data))
            self.assertTrue(any('broken link' in item for item in run(config)))
