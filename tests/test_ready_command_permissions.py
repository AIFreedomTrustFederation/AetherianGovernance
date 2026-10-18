"""Regression tests for ready federation capability executable paths."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

VERIFY_SOURCE = Path(__file__).resolve().parents[1] / ".aift/commands/verify.sh"


class ReadyCapabilityPermissionsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "governance fixture"
        commands = self.root / ".aift/commands"
        commands.mkdir(parents=True)
        shutil.copyfile(VERIFY_SOURCE, commands / "verify.sh")
        (commands / "verify.sh").chmod(0o755)
        self.status = commands / "status.sh"
        self.status.write_text("#!/bin/sh\nprintf 'ready\\n'\n", encoding="utf-8")
        self.status.chmod(0o755)
        self.write_json("aift.repo.json", {"name": "AetherianGovernance"})
        self.write_json(".aift/capabilities.json", {
            "repo": "AetherianGovernance",
            "capabilities": [
                {"name": "status", "status": "ready", "command": ".aift/commands/status.sh"},
                {"name": "verify", "status": "ready", "command": ".aift/commands/verify.sh"},
                {"name": "test", "status": "planned"},
            ],
        })
        self.write_json(".aift/events.json", {"repo": "AetherianGovernance", "publishes": [{"name": "repo.changed"}], "subscribes": []})
        self.write_json(".aift/services.json", {"repo": "AetherianGovernance", "services": [{"name": "service", "events": ["repo.changed"]}]})
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)

    def write_json(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def run_verify(self):
        return subprocess.run(
            ["sh", str(self.root / ".aift/commands/verify.sh")],
            cwd=Path(self.temporary.name),
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_executable_ready_commands_pass(self):
        result = self.run_verify()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("and 3 capabilities", result.stdout)

    def test_nonexecutable_ready_command_is_rejected(self):
        self.status.chmod(0o644)
        result = self.run_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("not executable", result.stdout + result.stderr)

    def test_missing_ready_command_is_rejected(self):
        self.status.unlink()
        result = self.run_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("missing capability command", result.stdout + result.stderr)

    def test_symlink_escaping_repository_is_rejected(self):
        external = Path(self.temporary.name) / "external.sh"
        external.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        external.chmod(0o755)
        self.status.unlink()
        self.status.symlink_to(external)
        result = self.run_verify()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("outside repository", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
