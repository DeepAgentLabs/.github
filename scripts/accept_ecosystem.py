"""Build the exact candidate sources and validate isolated installed wheels.

Requires uv and network/cache access to package dependencies. Does not publish
packages, contact live model providers or satisfy independent acceptance gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from release_readiness import REPOSITORIES, validate_manifest


def run(command, **kwargs):
    subprocess.run(command, check=True, timeout=600, **kwargs)


def clean_commit(path, expected):
    actual = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=path, text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=path,
        text=True,
    )
    if actual != expected or dirty:
        raise ValueError(
            f"Candidate checkout is not clean at its pinned commit: {path.name}"
        )


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path, default=root / "release/candidate.json"
    )
    parser.add_argument("--workspace", type=Path, default=root.parent)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.workspace = args.workspace.resolve()
    manifest = json.loads(args.manifest.read_text())
    candidate_digest = validate_manifest(manifest)
    for repo, candidate in manifest["candidates"].items():
        clean_commit(args.workspace / repo, candidate["commit"])
    wheels = {}
    with tempfile.TemporaryDirectory(prefix="ecosystem-acceptance-") as temporary:
        temp = Path(temporary)
        wheel_dir = temp / "wheels"
        for repo, distribution in REPOSITORIES.items():
            if distribution is None:
                continue
            run(
                ["uv", "build", "--wheel", "--out-dir", str(wheel_dir)],
                cwd=args.workspace / repo,
            )
            version = manifest["candidates"][repo]["version"]
            matches = list(
                wheel_dir.glob(f"{distribution.replace('-', '_')}-{version}-*.whl")
            )
            if len(matches) != 1:
                raise ValueError(f"Expected one matching wheel for {repo}")
            wheels[repo] = matches[0]
        empty = temp / "empty-workspace"
        empty.mkdir()
        env = dict(os.environ, DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT=str(empty))
        env.pop("PYTHONPATH", None)
        isolated = {}
        for repo, wheel in wheels.items():
            venv = temp / f"base-{repo}"
            run(["uv", "venv", str(venv)])
            python = venv / "bin/python"
            run(
                [
                    "uv",
                    "pip",
                    "install",
                    "--python",
                    str(python),
                    str(wheel),
                    *(
                        [f"mcp=={manifest['runtime_pins']['mcp']}"]
                        if repo == "mcp-server"
                        else []
                    ),
                ]
            )
            run(
                [
                    str(python),
                    "-I",
                    str(root / "scripts/check_installed.py"),
                    "--manifest",
                    str(args.manifest.resolve()),
                    "--package",
                    repo,
                ],
                cwd=empty,
                env=env,
            )
            isolated[repo] = True
            if repo == "mcp-server":
                run(
                    [
                        str(python),
                        "-I",
                        str(args.workspace / "mcp-server/scripts/smoke_protocol.py"),
                    ],
                    cwd=empty,
                    env=env,
                )
        venv = temp / "combined"
        run(["uv", "venv", str(venv)])
        python = venv / "bin/python"
        run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(python),
                *map(str, wheels.values()),
                f"mcp=={manifest['runtime_pins']['mcp']}",
            ]
        )
        suite = (
            args.workspace
            / "ai-operations-spec/specification/v0.6/conformance-suite/suite.json"
        )
        run(
            [
                str(python),
                "-I",
                str(root / "scripts/check_installed.py"),
                "--manifest",
                str(args.manifest.resolve()),
                "--suite",
                str(suite),
            ],
            cwd=empty,
            env=env,
        )
        dependency_versions = json.loads(
            subprocess.check_output(
                [
                    str(python),
                    "-I",
                    "-c",
                    "import importlib.metadata,json; print(json.dumps({d.metadata['Name']:d.version for d in importlib.metadata.distributions()}))",
                ],
                text=True,
                cwd=empty,
                env=env,
            )
        )
        evidence = {
            "gate_id": "wheel-interoperability",
            "candidate_digest": candidate_digest,
            "scope": sorted(REPOSITORIES),
            "result": "passed",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "actor": {
                "name": "isolated-wheel-acceptance",
                "organization": "DeepAgentLabs",
            },
            "checks": {
                key: True
                for key in [
                    "isolated_wheels",
                    "portable_suite",
                    "native_exports",
                    "negative_controls",
                    "source_origins",
                ]
            },
            "standalone_packages": isolated,
            "runtime_dependencies": dependency_versions,
            "wheel_sha256": {
                repo: hashlib.sha256(path.read_bytes()).hexdigest()
                for repo, path in wheels.items()
            },
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2) + "\n")
    print(
        f"Recorded internal acceptance in {args.output}; independent/live/freeze gates remain separate."
    )


if __name__ == "__main__":
    main()
