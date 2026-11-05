"""Check out the validated, immutable public candidate matrix into an empty workspace."""

import argparse
import json
import subprocess
from pathlib import Path

from release_readiness import validate_manifest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--manifest", type=Path, required=True)
parser.add_argument("--workspace", type=Path, required=True)
args = parser.parse_args()
manifest = json.loads(args.manifest.read_text())
validate_manifest(manifest)
args.workspace.mkdir(parents=True, exist_ok=True)
for name, entry in manifest["candidates"].items():
    path = args.workspace / name
    if path.exists() or path.is_symlink():
        raise SystemExit(f"Refusing to overwrite an existing checkout: {path}")
    path.mkdir()
    for command in [
        ["git", "init", "--quiet"],
        [
            "git",
            "remote",
            "add",
            "origin",
            f"https://github.com/{entry['repository']}.git",
        ],
        ["git", "fetch", "--depth", "1", "origin", entry["commit"]],
        ["git", "checkout", "--detach", "--quiet", "FETCH_HEAD"],
    ]:
        subprocess.run(command, cwd=path, check=True, timeout=120)
