"""Validate coordinated v1 acceptance evidence; never infer independent approval.

Diagnostics exit zero with ready=false. --require-ready exits 2 while any
required gate is missing, invalid or failed. No evidence URI is ever fetched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPOSITORIES = {
    "ai-operations-spec": None,
    "agenticlens": "agenticlens",
    "agentic-chaos": "agentic-chaos",
    "agentic-evals": "agentic-evals",
    "agentic-sidecar": "agentic-sidecar",
    "mcp-server": "deep-agentic-core-mcp",
    "agenticops-control-tower": "agenticops-control-tower",
}
GATES = {
    "wheel-interoperability": ("internal", set(REPOSITORIES)),
    "aios-independent-review": ("independent", {"ai-operations-spec"}),
    "aios-independent-implementations": ("independent", {"ai-operations-spec"}),
    "security-deployment-acceptance": (
        "independent",
        {"agenticlens", "mcp-server", "agenticops-control-tower"},
    ),
    "live-provider-smoke": ("provider", {"agentic-sidecar"}),
    "contract-freeze": ("maintainer", set(REPOSITORIES)),
}


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def validate_manifest(manifest):
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version") != "ecosystem.candidate/1"
    ):
        raise ValueError("Unknown candidate manifest contract")
    candidates = manifest.get("candidates", {})
    if not isinstance(candidates, dict) or set(candidates) != set(REPOSITORIES):
        raise ValueError(
            "Candidate matrix must include exactly the seven ecosystem repositories"
        )
    for repo, row in candidates.items():
        if not isinstance(row, dict):
            raise ValueError("Each candidate must be an object")
        if (
            row.get("repository") != f"DeepAgentLabs/{repo}"
            or row.get("distribution") != REPOSITORIES[repo]
        ):
            raise ValueError(f"Unexpected repository/distribution: {repo}")
        if not re.fullmatch(r"[a-f0-9]{40}", row.get("commit", "")):
            raise ValueError(f"An immutable full commit is required: {repo}")
        if not re.fullmatch(r"0\.[0-9]+\.[0-9]+", row.get("version", "")):
            raise ValueError(
                "Pre-1.0 candidate versions are required until acceptance closes"
            )
    if not isinstance(manifest.get("evidence", {}), dict) or set(
        manifest.get("evidence", {})
    ) - set(GATES):
        raise ValueError("Unknown acceptance gate")
    runtime = manifest.get("runtime_pins")
    if (
        not isinstance(runtime, dict)
        or set(runtime) != {"mcp"}
        or not re.fullmatch(r"2\.[0-9]+\.[0-9]+", runtime.get("mcp", ""))
    ):
        raise ValueError("An explicit supported MCP SDK runtime pin is required")
    markers = manifest.get("contract_markers")
    if (
        not isinstance(markers, dict)
        or "aios" not in markers
        or any(
            not isinstance(values, list)
            or not values
            or any(not isinstance(value, str) or not value for value in values)
            for values in markers.values()
        )
    ):
        raise ValueError(
            "Explicit nonempty candidate contract marker lists are required"
        )
    return digest(
        {"candidates": candidates, "contract_markers": markers, "runtime_pins": runtime}
    )


def read_evidence(root, entry):
    relative = Path(entry["path"])
    evidence_root = (root / "release/evidence").resolve()
    path = root / relative
    if relative.is_absolute() or not path.resolve().is_relative_to(evidence_root):
        raise ValueError("Evidence must be held inside release/evidence")
    if any(
        parent.is_symlink() for parent in [path, *path.parents] if parent != root.parent
    ):
        raise ValueError("Evidence symlinks are not accepted")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise ValueError("Evidence content digest differs from the reviewed manifest")
    document = json.loads(raw)
    if not isinstance(document, dict):
        raise ValueError("Evidence must be a JSON object")
    return document


def assess(manifest, root):
    candidate_digest = validate_manifest(manifest)
    results = []
    for gate, (kind, scope) in GATES.items():
        row = {
            "id": gate,
            "kind": kind,
            "status": "missing",
            "reason": "No acceptance evidence recorded",
        }
        entry = manifest.get("evidence", {}).get(gate)
        if entry is not None:
            try:
                document = read_evidence(root, entry)
                if (
                    document.get("gate_id") != gate
                    or document.get("candidate_digest") != candidate_digest
                ):
                    raise ValueError(
                        "Evidence does not name this gate and exact candidate matrix"
                    )
                if document.get("result") != "passed" or not scope <= set(
                    document.get("scope", [])
                ):
                    raise ValueError(
                        "Acceptance failed or does not cover the required scope"
                    )
                at = datetime.fromisoformat(
                    document["recorded_at"].upper().replace("Z", "+00:00")
                )
                if (
                    at.tzinfo is None
                    or at.utcoffset() is None
                    or at > datetime.now(timezone.utc)
                ):
                    raise ValueError(
                        "Evidence needs an observed timezone-aware recording time"
                    )
                actor = document.get("actor", {})
                if not actor.get("name") or not actor.get("organization"):
                    raise ValueError("Evidence author attribution is required")
                if kind == "independent":
                    declaration = actor.get("independence", {})
                    if not all(
                        declaration.get(key) is False
                        for key in (
                            "aios_authorship",
                            "deepagentlabs_funding",
                            "editorial_control",
                        )
                    ):
                        raise ValueError(
                            "Independent acceptance requires explicit unaffiliated-review declarations"
                        )
                    if re.sub(
                        r"[^a-z0-9]", "", actor["organization"].casefold()
                    ).startswith("deepagentlabs"):
                        raise ValueError(
                            "DeepAgentLabs cannot supply independent acceptance"
                        )
                    if not document.get("review_reference") or not document.get(
                        "findings"
                    ):
                        raise ValueError(
                            "A review reference and acceptance findings are required"
                        )
                elif kind == "internal":
                    checks = document.get("checks", {})
                    if not all(
                        checks.get(key) is True
                        for key in (
                            "isolated_wheels",
                            "portable_suite",
                            "native_exports",
                            "negative_controls",
                            "source_origins",
                        )
                    ):
                        raise ValueError(
                            "Executable wheel acceptance checks are incomplete"
                        )
                    if set(document.get("wheel_sha256", {})) != {
                        repo for repo, dist in REPOSITORIES.items() if dist
                    }:
                        raise ValueError("All six wheel digests are required")
                    if any(
                        not re.fullmatch(r"[a-f0-9]{64}", value)
                        for value in document["wheel_sha256"].values()
                    ):
                        raise ValueError("Wheel digests must be SHA-256 values")
                elif kind == "provider":
                    providers = document.get("providers", {})
                    if set(providers) != {"openai", "anthropic"} or any(
                        value.get("status") != "passed" or not value.get("model")
                        for value in providers.values()
                    ):
                        raise ValueError(
                            "Both selected live providers need observed passing results and models"
                        )
                elif document.get("approved_contracts") != manifest.get(
                    "contract_markers"
                ):
                    raise ValueError(
                        "Maintainer freeze must approve the exact candidate contract markers"
                    )
                elif any(
                    value.endswith(("-draft", "-candidate"))
                    for values in manifest["contract_markers"].values()
                    for value in values
                ):
                    raise ValueError(
                        "Draft/candidate contract markers cannot close the coordinated stable freeze"
                    )
                row.update(
                    status="recorded",
                    reason="Held evidence matches the candidate matrix; provenance/independence still requires human review",
                )
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
                row.update(status="invalid", reason=str(exc))
        results.append(row)
    return {
        "schema_version": "ecosystem.readiness/1",
        "candidate_digest": candidate_digest,
        "ready": all(row["status"] == "recorded" for row in results),
        "gates": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "release/candidate.json",
    )
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    try:
        report = assess(
            json.loads(args.manifest.read_text()), args.manifest.resolve().parents[1]
        )
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"Invalid release manifest: {exc}\n")
    print(json.dumps(report, indent=2))
    if args.require_ready and not report["ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
