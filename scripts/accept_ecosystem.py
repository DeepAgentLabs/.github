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
import tarfile
import tempfile
from datetime import UTC, datetime
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


def materialize_commit(path, expected, destination):
    """Build from committed bytes only; ignored workspace files cannot enter."""
    destination.mkdir()
    archive = destination.with_suffix(".tar")
    run(["git", "archive", "--format=tar", f"--output={archive}", expected], cwd=path)
    with tarfile.open(archive) as source:
        source.extractall(destination, filter="data")
    archive.unlink()
    return {
        item.relative_to(destination): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in destination.rglob("*")
        if item.is_file()
    }


def verify_source_snapshot(destination, snapshot):
    for relative, expected in snapshot.items():
        path = destination / relative
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != expected
        ):
            raise ValueError(f"Build mutated committed source: {relative}")


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path, default=root / "release/candidate.json"
    )
    parser.add_argument("--workspace", type=Path, default=root.parent)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--record-evidence",
        action="store_true",
        help="Record the held receipt digest in this manifest after success",
    )
    args = parser.parse_args()
    args.workspace = args.workspace.resolve()
    manifest = json.loads(args.manifest.read_text())
    candidate_digest = validate_manifest(manifest)
    manifest_before = args.manifest.read_bytes()
    receipt_relative = None
    if args.record_evidence:
        receipt_relative = args.output.resolve().relative_to(
            args.manifest.resolve().parents[1]
        )
        if not args.output.resolve().is_relative_to(
            args.manifest.resolve().parents[1] / "release/evidence"
        ):
            raise ValueError("Recorded evidence must be held under release/evidence")
    for repo, candidate in manifest["candidates"].items():
        clean_commit(args.workspace / repo, candidate["commit"])
    wheels = {}
    with tempfile.TemporaryDirectory(prefix="ecosystem-acceptance-") as temporary:
        temp = Path(temporary)
        wheel_dir = temp / "wheels"
        sources = temp / "sources"
        sources.mkdir()
        snapshots = {}
        for repo, candidate in manifest["candidates"].items():
            snapshots[repo] = materialize_commit(
                args.workspace / repo, candidate["commit"], sources / repo
            )
        for repo, distribution in REPOSITORIES.items():
            if distribution is None:
                continue
            run(
                ["uv", "build", "--wheel", "--out-dir", str(wheel_dir)],
                cwd=sources / repo,
            )
            verify_source_snapshot(sources / repo, snapshots[repo])
            clean_commit(args.workspace / repo, manifest["candidates"][repo]["commit"])
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
                        str(sources / "mcp-server/scripts/smoke_protocol.py"),
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
            sources
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
            "recorded_at": datetime.now(UTC).isoformat(),
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
        for repo, candidate in manifest["candidates"].items():
            verify_source_snapshot(sources / repo, snapshots[repo])
            clean_commit(args.workspace / repo, candidate["commit"])
        if args.manifest.read_bytes() != manifest_before:
            raise ValueError("Candidate manifest changed during acceptance")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2) + "\n")
        if args.record_evidence:
            manifest.setdefault("evidence", {})["wheel-interoperability"] = {
                "path": receipt_relative.as_posix(),
                "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
            }
            args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        f"Recorded internal acceptance in {args.output}; independent/live/freeze gates remain separate."
    )


if __name__ == "__main__":
    main()
