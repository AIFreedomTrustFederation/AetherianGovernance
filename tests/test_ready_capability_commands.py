"""Regression checks for ready capability executable-path validation."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE_VERIFIER = Path(__file__).resolve().parents[1] / ".aift/commands/verify.sh"


class ReadyCapabilityCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aift-governance-verify-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        commands = self.root / ".aift/commands"
        commands.mkdir(parents=True)
        (self.root / "aift.repo.json").write_text(
            json.dumps({"name": "AetherianGovernance"}), encoding="utf-8"
        )
        (self.root / ".aift/events.json").write_text(
            json.dumps({"repo": "AetherianGovernance", "publishes": [], "subscribes": []}),
            encoding="utf-8",
        )
        (self.root / ".aift/services.json").write_text(
            json.dumps({"repo": "AetherianGovernance", "services": []}),
            encoding="utf-8",
        )
        self.capabilities = self.root / ".aift/capabilities.json"
        shutil.copyfile(SOURCE_VERIFIER, commands / "verify.sh")
        (commands / "verify.sh").chmod(0o755)
        (commands / "status.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        (commands / "status.sh").chmod(0o755)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "aift.repo.json", ".aift"], cwd=self.root, check=True)

    def verify(self, command):
        self.capabilities.write_text(
            json.dumps({"repo": "AetherianGovernance", "capabilities": [
                {"name": "status", "status": "ready", "command": command}
            ]}), encoding="utf-8"
        )
        return subprocess.run(
            ["sh", ".aift/commands/verify.sh"], cwd=self.root,
            capture_output=True, text=True, check=False,
        )

    def test_existing_ready_script_with_arguments_passes(self):
        self.assertEqual(self.verify(".aift/commands/status.sh --help").returncode, 0)

    def test_missing_ready_script_with_arguments_fails(self):
        result = self.verify(".aift/commands/missing.sh --help")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing capability command", result.stderr)

    def test_missing_root_relative_ready_script_fails(self):
        result = self.verify("./missing.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing capability command", result.stderr)

    def test_parent_traversal_with_arguments_fails(self):
        result = self.verify("../outside.sh --help")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe capability command path", result.stderr)

    def test_absolute_path_with_arguments_fails(self):
        result = self.verify("/tmp/outside.sh --help")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe capability command path", result.stderr)

    def test_bare_executable_command_remains_supported(self):
        self.assertEqual(self.verify("git status --short").returncode, 0)

    def test_compound_shell_command_remains_supported(self):
        self.assertEqual(
            self.verify("git remote -v && git status --short").returncode, 0
        )

    def test_malformed_quoted_command_fails(self):
        result = self.verify("./missing.sh 'unterminated")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed ready capability command", result.stderr)


if __name__ == "__main__":
    unittest.main()
