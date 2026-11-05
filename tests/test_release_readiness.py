import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location(
    "readiness", ROOT / "scripts/release_readiness.py"
)
readiness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readiness)


def manifest():
    return {
        "schema_version": "ecosystem.candidate/1",
        "runtime_pins": {"mcp": "2.0.0"},
        "candidates": {
            repo: {
                "repository": f"DeepAgentLabs/{repo}",
                "distribution": dist,
                "commit": "a" * 40,
                "version": "0.1.0",
            }
            for repo, dist in readiness.REPOSITORIES.items()
        },
        "evidence": {},
        "contract_markers": {"aios": ["1.0"]},
    }


class ReleaseReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "release/evidence").mkdir(parents=True)
        self.matrix = manifest()

    def tearDown(self):
        self.temp.cleanup()

    def add(self, gate, **changes):
        kind, scope = readiness.GATES[gate]
        record = {
            "gate_id": gate,
            "candidate_digest": readiness.validate_manifest(self.matrix),
            "result": "passed",
            "scope": sorted(scope),
            "recorded_at": "2026-01-01T00:00:00Z",
            "actor": {
                "name": "reviewer",
                "organization": "Independent Example",
                "independence": {
                    "aios_authorship": False,
                    "deepagentlabs_funding": False,
                    "editorial_control": False,
                },
            },
            "review_reference": "held external review",
            "findings": ["Accepted within documented scope"],
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
            "wheel_sha256": {
                repo: "b" * 64 for repo, dist in readiness.REPOSITORIES.items() if dist
            },
            "providers": {
                name: {"status": "passed", "model": "explicit-model"}
                for name in ["openai", "anthropic"]
            },
            "approved_contracts": self.matrix["contract_markers"],
        }
        record.update(changes)
        raw = (json.dumps(record) + "\n").encode()
        path = f"release/evidence/{gate}.json"
        (self.root / path).write_bytes(raw)
        self.matrix["evidence"][gate] = {
            "path": path,
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        return record

    def test_absence_cannot_pass(self):
        report = readiness.assess(self.matrix, self.root)
        self.assertFalse(report["ready"])
        self.assertEqual(len(report["gates"]), len(readiness.GATES))

    def test_complete_matching_evidence_is_recorded(self):
        for gate in readiness.GATES:
            self.add(gate)
        self.assertTrue(readiness.assess(self.matrix, self.root)["ready"])

    def test_omitting_or_changing_candidates_is_rejected(self):
        for mutation in [
            lambda m: m["candidates"].pop("agenticlens"),
            lambda m: m["candidates"]["agenticlens"].update(commit="main"),
            lambda m: m["candidates"]["mcp-server"].update(repository="other/repo"),
        ]:
            value = copy.deepcopy(self.matrix)
            mutation(value)
            with self.assertRaises(ValueError):
                readiness.assess(value, self.root)

    def test_internal_tests_cannot_close_independent_review(self):
        gate = "aios-independent-review"
        self.add(
            gate,
            actor={
                "name": "internal editor",
                "organization": "DeepAgentLabs",
                "independence": {
                    "aios_authorship": False,
                    "deepagentlabs_funding": False,
                    "editorial_control": False,
                },
            },
        )
        row = next(
            row
            for row in readiness.assess(self.matrix, self.root)["gates"]
            if row["id"] == gate
        )
        self.assertEqual(row["status"], "invalid")

    def test_affiliated_organization_spelling_variants_are_rejected(self):
        for organization in [
            "DeepAgentLabs, Inc.",
            "Deep-AgentLabs",
            "Deep Agent Labs LLC",
        ]:
            with self.subTest(organization=organization):
                record = self.add("aios-independent-review")
                actor = record["actor"]
                actor["organization"] = organization
                self.add("aios-independent-review", actor=actor)
                row = next(
                    row
                    for row in readiness.assess(self.matrix, self.root)["gates"]
                    if row["id"] == "aios-independent-review"
                )
                self.assertEqual(row["status"], "invalid")

    def test_unrun_providers_do_not_pass(self):
        self.add(
            "live-provider-smoke",
            providers={
                "openai": {"status": "not_run", "model": "model"},
                "anthropic": {"status": "passed", "model": "model"},
            },
        )
        self.assertEqual(
            next(
                row
                for row in readiness.assess(self.matrix, self.root)["gates"]
                if row["id"] == "live-provider-smoke"
            )["status"],
            "invalid",
        )

    def test_evidence_is_bound_to_candidate_bytes(self):
        gate = "aios-independent-review"
        self.add(gate)
        self.matrix["candidates"]["agenticlens"]["commit"] = "c" * 40
        self.assertEqual(
            next(
                row
                for row in readiness.assess(self.matrix, self.root)["gates"]
                if row["id"] == gate
            )["status"],
            "invalid",
        )

    def test_tampering_and_traversal_are_rejected(self):
        gate = "contract-freeze"
        self.add(gate)
        (self.root / self.matrix["evidence"][gate]["path"]).write_text("{}")
        self.assertEqual(
            next(
                row
                for row in readiness.assess(self.matrix, self.root)["gates"]
                if row["id"] == gate
            )["status"],
            "invalid",
        )
        self.matrix["evidence"][gate]["path"] = "../../outside.json"
        self.assertFalse(readiness.assess(self.matrix, self.root)["ready"])

    def test_internal_check_names_are_required(self):
        self.add("wheel-interoperability", checks={"arbitrary": True})
        self.assertEqual(
            readiness.assess(self.matrix, self.root)["gates"][0]["status"], "invalid"
        )

    def test_draft_contracts_cannot_be_frozen_by_a_label(self):
        self.matrix["contract_markers"] = {"aios": ["0.8-draft"]}
        self.add("contract-freeze")
        row = next(
            row
            for row in readiness.assess(self.matrix, self.root)["gates"]
            if row["id"] == "contract-freeze"
        )
        self.assertEqual(row["status"], "invalid")

    def test_naive_times_and_unknown_gates_are_rejected(self):
        self.add("contract-freeze", recorded_at="2026-01-01T00:00:00")
        self.assertFalse(readiness.assess(self.matrix, self.root)["ready"])
        self.matrix["evidence"]["fake"] = {}
        with self.assertRaises(ValueError):
            readiness.assess(self.matrix, self.root)


if __name__ == "__main__":
    unittest.main()
