"""Regression tests for the federation manifest's advertised verify command."""

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ManifestVerifyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        (self.repo / ".aift/commands").mkdir(parents=True)
        shutil.copy2(ROOT / ".aift/commands/verify.sh", self.repo / ".aift/commands/verify.sh")
        os.chmod(self.repo / ".aift/commands/verify.sh", 0o755)
        self.manifest = json.loads((ROOT / "aift.repo.json").read_text(encoding="utf-8"))
        self.write_json("aift.repo.json", self.manifest)
        self.write_json(".aift/repo.json", {"name": "AetherianGovernance"})
        self.write_json(".aift/capabilities.json", {
            "repo": "AetherianGovernance",
            "capabilities": [{"name": "verify", "status": "ready", "command": ".aift/commands/verify.sh"}],
        })
        self.write_json(".aift/events.json", {"publishes": [], "subscribes": []})
        self.write_json(".aift/services.json", {"services": []})
        self.write_json(".aift/manual.json", {})
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", ".aift/commands/verify.sh"], cwd=self.repo, check=True)

    def write_json(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def run_advertised_verify(self):
        return subprocess.run(
            shlex.split(self.manifest["commands"]["verify"]),
            cwd=self.repo,
            capture_output=True,
            text=True,
            timeout=20,
        )

    def test_manifest_dispatches_actual_verifier(self):
        self.assertEqual(self.manifest["commands"]["verify"], ".aift/commands/verify.sh")

    def test_valid_contract_passes(self):
        result = self.run_advertised_verify()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_duplicate_json_keys_fail(self):
        (self.repo / ".aift/services.json").write_text('{"services":[],"services":[]}\n', encoding="utf-8")
        result = self.run_advertised_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_ready_capability_command_fails(self):
        self.write_json(".aift/capabilities.json", {
            "repo": "AetherianGovernance",
            "capabilities": [{"name": "verify", "status": "ready", "command": ".aift/commands/missing.sh"}],
        })
        result = self.run_advertised_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_tracked_shell_script_fails(self):
        (self.repo / "broken.sh").write_text("echo 'unterminated\n", encoding="utf-8")
        subprocess.run(["git", "add", "broken.sh"], cwd=self.repo, check=True)
        result = self.run_advertised_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
