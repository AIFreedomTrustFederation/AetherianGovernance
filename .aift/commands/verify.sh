#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$repo_root"

python3 - <<'PY'
import json
import subprocess
from pathlib import Path, PurePosixPath

root = Path.cwd()
manifest_paths = [Path("aift.repo.json"), *sorted(Path(".aift").glob("*.json"))]

if not manifest_paths:
    raise SystemExit("no federation manifests found")

documents = {}
for path in manifest_paths:
    with path.open(encoding="utf-8") as handle:
        documents[path.as_posix()] = json.load(handle)

expected_repo = root.name
declared_names = {
    document[key]
    for document in documents.values()
    for key in ("name", "repo")
    if key in document
}
if declared_names != {expected_repo}:
    raise SystemExit(
        f"repository identity mismatch: expected {expected_repo!r}, found {sorted(declared_names)!r}"
    )

capabilities = documents[".aift/capabilities.json"].get("capabilities", [])
names = [capability.get("name") for capability in capabilities]
if len(names) != len(set(names)):
    raise SystemExit("capability names must be unique")

for capability in capabilities:
    if capability.get("status") != "ready":
        continue
    command = capability.get("command")
    if not isinstance(command, str) or not command.strip():
        raise SystemExit(f"ready capability {capability.get('name')!r} has no command")

    candidate = PurePosixPath(command)
    if len(candidate.parts) == 1 or any(token in command for token in " &;|<>"):
        continue
    if candidate.is_absolute() or ".." in candidate.parts:
        raise SystemExit(f"unsafe capability command path: {command!r}")
    command_path = root.joinpath(*candidate.parts)
    if not command_path.is_file():
        raise SystemExit(f"missing capability command: {command}")

print(f"validated {len(documents)} federation manifests and {len(capabilities)} capabilities")

tracked = subprocess.run(
    ["git", "ls-files", "-z", "*.sh"],
    check=True,
    capture_output=True,
).stdout.split(b"\0")
scripts = [name.decode("utf-8") for name in tracked if name]
if not scripts:
    raise SystemExit("no tracked shell scripts found")
for script in scripts:
    subprocess.run(["sh", "-n", script], check=True)
print(f"validated {len(scripts)} tracked shell scripts")
PY
