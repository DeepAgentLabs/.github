"""Exercise installed ecosystem wheels under python -I from an empty workspace."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import importlib.metadata
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MODULES = {
    "agenticlens": "agenticlens",
    "agentic-chaos": "agentic_chaos",
    "agentic-evals": "agentic_evals",
    "agentic-sidecar": "agentic_sidecar",
    "mcp-server": "deep_agentic_core_mcp",
    "agenticops-control-tower": "agenticops_control_tower",
}


def outcome_mcp(module, document):
    report = module.validate_artifact(document)
    if report.get("compatibility", {}).get("decision") == "reject":
        return "unsupported", ["AIOS-0.5-V03"]
    if report["schema_errors"]:
        rule = {
            "0.4-draft": "AIOS-0.4-P01",
            "0.6-draft": "AIOS-0.6-R01",
            "0.8-draft": "AIOS-0.8-R01",
        }[document["spec_version"]]
        return "schema-invalid", [rule]
    rules = sorted({issue["rule_id"] for issue in report["conformance"]["issues"]})
    return ("semantic-invalid", rules) if rules else ("valid", [])


def outcome_lens(function, document):
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "artifact.json"
        path.write_text(json.dumps(document))
        try:
            report = function(path)
        except ValueError as exc:
            if "AIOS-0.5-V03" not in str(exc) and "Unsupported" not in str(exc):
                raise
            return "unsupported", ["AIOS-0.5-V03"]
    outcome = (
        "schema-invalid"
        if not report.schema_valid
        else "semantic-invalid"
        if not report.semantic_valid
        else "valid"
    )
    return outcome, sorted({issue.rule_id for issue in report.issues})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--suite", type=Path)
    parser.add_argument("--package", choices=MODULES)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    selected = [args.package] if args.package else list(MODULES)
    for repo in selected:
        row = manifest["candidates"][repo]
        assert importlib.metadata.version(row["distribution"]) == row["version"], repo
        module = importlib.import_module(MODULES[repo])
        assert (
            Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
        ), (repo, module.__file__)
    if args.package:
        # Import the real public boundary, not only a package __init__.
        boundaries = {
            "agenticlens": "agenticlens.validation",
            "agentic-chaos": "agentic_chaos.hub",
            "agentic-evals": "agentic_evals",
            "agentic-sidecar": "agentic_sidecar.integrations.aios",
            "mcp-server": "deep_agentic_core_mcp.server",
            "agenticops-control-tower": "agenticops_control_tower.incidents.export",
        }
        importlib.import_module(boundaries[args.package])
        print(json.dumps({"standalone": args.package, "passed": True}))
        return

    from agenticlens.validation import resolve_provenance, validate_aios_artifact
    from deep_agentic_core_mcp.adapters import ai_operations_spec as mcp_spec

    suite_path = args.suite.resolve()
    suite_dir = suite_path.parent
    suite = json.loads(suite_path.read_text())
    assert sorted(manifest["contract_markers"]["aios"]) == mcp_spec.supported_versions()
    source_root = suite_path.parents[3]
    import agenticlens
    import deep_agentic_core_mcp

    for bundle in [
        Path(agenticlens.__file__).parent / "schemas/aios",
        Path(deep_agentic_core_mcp.__file__).parent / "resources/aios",
    ]:
        source = json.loads((bundle / "SOURCE.json").read_text())
        assert source["license"] == "MIT"
        for relative, checksum in source["files"].items():
            held = (bundle / relative).resolve()
            original = (source_root / relative).resolve()
            assert held.is_relative_to(bundle.resolve()) and original.is_relative_to(
                source_root.resolve()
            )
            assert hashlib.sha256(held.read_bytes()).hexdigest() == checksum
            assert held.read_bytes() == original.read_bytes(), relative

    assert len(suite["cases"]) >= 66 and len(suite["resolution_cases"]) >= 5
    for case in suite["cases"]:
        document = json.loads((suite_dir / case["path"]).read_text())
        expected = case["expected"], case["rules"]
        assert outcome_mcp(mcp_spec, document) == expected, ("mcp", case["id"])
        assert outcome_lens(validate_aios_artifact, document) == expected, (
            "lens",
            case["id"],
        )
    for case in suite["resolution_cases"]:
        record = json.loads((suite_dir / case["record"]).read_text())
        held = {
            key: (suite_dir / path).read_bytes()
            for key, path in case["subjects"].items()
        }
        assert resolve_provenance(record, held) == case["expected"], (
            "lens",
            case["id"],
        )
        assert mcp_spec.resolve_provenance(record, held) == case["expected"], (
            "mcp",
            case["id"],
        )

    from agentic_evals import Score
    from agentic_sidecar.core.provenance import (
        AuditRecord,
        DecisionRationale,
        DecisionTrigger,
    )
    from agentic_sidecar.integrations.aios import export_audit_event
    from agenticlens.exporters.verification import export_verification_signal
    from agenticops_control_tower.incidents.export import export_investigation_report
    from agenticops_control_tower.incidents.models import Incident, Investigation
    from agenticops_control_tower.models.evidence import (
        EvidenceLink,
        EvidenceRecord,
        EvidenceSummary,
    )
    from deep_agentic_core_mcp.services.access_evidence import (
        export_audit_event as export_access,
    )
    from deep_agentic_core_mcp.services.access_evidence import record

    now = datetime.now(timezone.utc)
    reference = {
        "id": "subject",
        "producer": "agenticlens",
        "artifact_id": "run-1",
        "format": "0.4-draft",
    }
    score = Score(
        name="judge",
        value=0.5,
        passed=False,
        explanation="private",
        evaluator_type="llm_judge",
        metadata={
            "judge_verdict": {
                "verdict": "partially_agree",
                "confidence": 0.8,
                "unsupported_claims": ["private"],
            }
        },
    )
    verification = export_verification_signal(
        score,
        source_id="judge-1",
        subject=reference,
        evidence=[reference],
        created_at=now,
        method_version="1",
    )
    unavailable = export_verification_signal(
        Score(
            name="judge",
            value=0,
            passed=False,
            explanation="unavailable",
            evaluator_type="llm_judge",
            metadata={"judge_status": "unavailable"},
        ),
        source_id="judge-2",
        subject=reference,
        evidence=[],
        created_at=now,
        method_version="1",
    )
    assert unavailable["verdict"] is None and unavailable["confidence"] is None
    native_audit = AuditRecord(
        decision_id="decision-1",
        timestamp=now,
        outcome="BLOCK",
        trigger=DecisionTrigger("tool_call", "tool", {"credential": "private"}),
        rationale=DecisionRationale(reason="private"),
    )
    audit = export_audit_event(native_audit, target=reference, created_at=now)
    assert audit["outcome"] == "denied"
    access = record(
        "denial",
        correlation_id="call-1",
        user="private",
        tool="private",
        reason="private",
    )
    access_audit = export_access(
        access, target=reference, created_at=datetime.now(timezone.utc)
    )
    detection = EvidenceRecord(
        record_id="e-1",
        ingested_at=now,
        ingested_by="operator",
        summary=EvidenceSummary(
            link=EvidenceLink(
                agent_id="a-1",
                source="agenticlens",
                source_version=manifest["candidates"]["agenticlens"]["version"],
                artifact_type="run",
                artifact_ref="run-1",
                observed_at=now,
            ),
            availability="available",
        ),
    )
    incident = Incident(
        incident_id="incident-1",
        agent_id="a-1",
        detection=detection,
        state="resolved",
        investigation=Investigation(
            finding="private",
            certainty="observed_failure",
            citations=["e-1"],
            missing=[],
            timeline=[detection],
        ),
    )
    investigation = export_investigation_report(incident, created_at=now)
    assert investigation["recovery"]["status"] == "unknown"
    for document in (verification, unavailable, audit, access_audit, investigation):
        assert "private" not in json.dumps(document)
        assert outcome_mcp(mcp_spec, document) == ("valid", [])
        assert outcome_lens(validate_aios_artifact, document) == ("valid", [])
    invalid = copy.deepcopy(unavailable)
    invalid["verdict"] = "supports"
    assert outcome_mcp(mcp_spec, invalid)[0] == "schema-invalid"
    assert outcome_lens(validate_aios_artifact, invalid)[0] == "schema-invalid"
    invalid = copy.deepcopy(investigation)
    invalid["recovery"] = {"status": "verified", "evidence_ids": []}
    assert outcome_mcp(mcp_spec, invalid) == ("semantic-invalid", ["AIOS-0.8-R06"])
    assert outcome_lens(validate_aios_artifact, invalid) == (
        "semantic-invalid",
        ["AIOS-0.8-R06"],
    )
    print(
        json.dumps(
            {
                "portable_cases": len(suite["cases"]),
                "resolution_cases": len(suite["resolution_cases"]),
                "producer_exports": 5,
                "negative_controls": 2,
                "passed": True,
            }
        )
    )


if __name__ == "__main__":
    main()
