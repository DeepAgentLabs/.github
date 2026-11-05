# Coordinated v1.0 readiness plan

The implementation baseline is a pre-1.0 candidate, not a stable release.
Supported scope follows each repository's current guides: local/single-node
services, explicit authenticated HTTP boundaries, host-bound supervision and
access controls, source-attributed native evidence and bounded staging recovery.
Distributed tenancy/HA, production remediation connectors, remote sandboxed
Chaos and hosted account/billing expansions remain explicitly deferred where
those guides put them outside the supported candidate. Final scope and contract
freezing require maintainer acceptance after the independent reviews.

## Delivered engineering work

| Component | Candidate | Engineering acceptance |
| --- | --- | --- |
| AIOS | 0.8.1 | MIT licensing; unchanged 0.4/0.6/0.8 draft schemas and 66-case portable suite with 5 held-byte resolution cases |
| Lens | 0.14.0 | All draft families validated offline from notice-preserving pinned assets; native judge verification exports |
| MCP | 0.8.0 | All draft families and provenance resolution; packaged standalone schemas and native access audit exports |
| Sidecar | 0.11.0 | Privacy-preserving native audit exports; required-provider smoke mode rejects missing results |
| Tower | 0.11.0 | Native incident investigations with explicit citations, redacted text and independent closure/recovery states |
| Evals | 0.12.0 | Existing report/gate/scoring contracts, including unavailable judgments |
| Chaos | 0.11.0 | Existing native resilience/containment evidence and ChaosHub |

The exact source pins and contract markers are in [candidate.json](../release/candidate.json).
New companion exporters preserve source identity, native outcomes and unknown
states; they grant no authority and do not authenticate imported artifacts.
Raw credentials, arguments, private rationale/context and operator details are
not copied by the projections. Hosts must supply public opaque identifiers.
Schema/semantic validation is separate from truth, integrity and completeness.

## Executable acceptance

Use Python 3.12+ and `uv` (CI installs Python 3.12). From the organization
repository checkout, with sibling repositories at the manifest's exact clean commits:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/accept_ecosystem.py --output /tmp/wheel-acceptance.json
python3 scripts/release_readiness.py
python3 scripts/release_readiness.py --require-ready
```

To replace reviewed internal evidence deliberately, run
`python3 scripts/accept_ecosystem.py --output release/evidence/wheel-acceptance.json --record-evidence`.
This records the new receipt SHA-256 in the manifest only after all checks pass;
review and commit both files together. Ordinary reproductions write to `/tmp`
and leave the held receipt unchanged. CI records a separate manifest/receipt pair
and reports readiness against that exact run, uploading both for inspection.

The acceptance runner materializes committed source bytes into fresh temporary
build trees, excluding ignored workspace files, and rejects source mutation
during builds before checking the resulting wheels. It builds six wheels, tests each in a fresh isolated base
environment, then installs the combined candidate matrix in another environment.
Python `-I`, empty working directories and imported-source-origin checks prevent
sibling source/virtualenv fallbacks. Both validators run every portable case and
all held-byte resolution cases from packaged schemas. Real native objects feed
the companion exporters; negative controls reject unavailable-as-pass and
uncited recovery. MCP additionally runs its installed-wheel stdio protocol smoke.
Checksums compare bundled schema/license bytes to the pinned specification.
No deployment or live model call is made by this runner.

To reproduce from remote commits rather than existing local checkouts:

```bash
python3 scripts/checkout_candidates.py --manifest release/candidate.json --workspace /tmp/v1-candidates
python3 scripts/accept_ecosystem.py --workspace /tmp/v1-candidates --output /tmp/wheel-acceptance.json
```

The workflow uploads internal acceptance and readiness reports; it never
publishes. Diagnostic readiness exits zero and can report ready=false.
`--require-ready` exits 2 until every fixed required gate has matching evidence.
Internal tests and bot reviews cannot close independent gates.

## Remaining required acceptance

Reviewers start with the [single reviewer entry page](EXTERNAL_REVIEW_CHECKLIST.md),
choose one area, and submit the linked report. The [detailed task requirements](EXTERNAL_REVIEW_DETAILS.md)
remain available for specialists and acceptance tracking.

| Gate | What closes it | Current owner/input |
| --- | --- | --- |
| Independent AIOS review | Recorded outside review of prerequisite layers and operational mappings | An unaffiliated reviewer; none supplied |
| Independent implementations | External validator/producer/consumer evidence, including extension preservation and provenance resolution | Non-DeepAgentLabs implementers; none supplied |
| Security/deployment acceptance | Independent findings plus operator-environment acceptance within the supported scope for Lens, MCP and Tower | Reviewers/deployment owners; none supplied |
| Live provider smoke | Both explicit OpenAI and Anthropic models return authenticated passing observations | Credentials and model selections; currently not configured |
| Final stable freeze | Maintainer approves final contracts after review; stable schemas replace draft/candidate markers and matching consumers pass | Maintainers, after preceding gates |

Sidecar's command is:

```bash
uv run python scripts/smoke_judge_providers.py --require-all
```

Configure `OPENAI_API_KEY`/`SIDECAR_OPENAI_MODEL` and
`ANTHROPIC_API_KEY`/`SIDECAR_ANTHROPIC_MODEL` through the operator environment.
Keys are never printed. Missing credentials/models produce not_run and exit 2;
failed calls exit 1. The recorded local attempt in
[provider-attempt.json](../release/evidence/provider-attempt.json) is diagnostic,
not passing evidence and is intentionally not accepted by the manifest.

Use AIOS's existing external review packet and scenario worksheets; no reviewer
is contacted automatically. Record substantive findings and the review's actual
source reference, rather than renaming an internal test as an outside review.

## Evidence receipt contract

A manifest evidence entry names a held file beneath release/evidence plus its
SHA-256. Its JSON contains gate_id, candidate_digest, result (passed), scope,
recorded_at and actor attribution. The candidate digest binds both all seven
source pins, declared contract markers and the explicit MCP SDK runtime pin. Changed candidates or altered
receipt bytes invalidate old evidence. Paths outside the evidence directory,
symlinks, missing scope, naive/future dates, unrun providers and incomplete
internal checks are rejected. References are not fetched.

Independent receipts additionally contain review_reference, substantive findings
and explicit false declarations for AIOS authorship, DeepAgentLabs funding and
editorial control. A DeepAgentLabs organization is rejected for independent
acceptance. This validates the recorded declarations; it cannot prove that a
self-authored name or independence claim is true. Maintainers must verify the
review provenance and reviewer relationship before accepting/merging receipts.
No cryptographic reviewer authentication or third-party certification is claimed.

The stable freeze cannot pass while approved markers still end in -draft or
-candidate. Do not create 1.0 tags as a substitute for closing that obligation.

## Publication sequence

1. Land/test the licensing and implementation increments through minor/patch
   releases, preserving public compatibility and optional dependencies.
2. Pin their reviewed source commits in the coordinated matrix and record the
   internal installed-wheel result. No unchanged sibling needs a patch release
   for documentation-only alignment.
3. Obtain and review the missing external, deployment and provider evidence.
4. Resolve review findings, approve final supported scope and implement the
   stable schema/API freeze with migration/rollback and consumer compatibility.
5. Rebuild/retest the exact resulting candidates; run the mandatory readiness
   gate before any coordinated 1.0 publication.

Publishing the current minor releases does not deploy AWS or certify a cluster.
The coordinated launch remains gated; it is not an atomic registry transaction.
