# External review: start here

We need outside feedback on whether the specification is understandable, whether
other tools can exchange its data, and whether the documented runtime boundaries
hold in a real test environment. We need findings and reproducible examples,
including things that fail or are unclear. Agreement is not a requirement.

You do **not** need to review every project or complete every task.

## A few words used below

- **Artifact:** a JSON record describing an execution, observation or finding.
- **Producer / consumer:** a tool that writes / reads those records.
- **Validator:** a tool that checks a record's structure and meaning rules.
- **Provenance:** a record of which source data a finding came from.
- **Commit:** the exact source-code revision tested, rather than just a version label.
- **Acceptance gate:** a requirement maintainers need evidence for before declaring it complete.

## Start in three steps

1. Pick a track below that matches your experience. Tell us which task IDs you
   plan to cover; a partial review is welcome.
2. Record the package versions and full source commits you review. The current
   [candidate matrix](../release/candidate.json) is the starting baseline;
   maintainers should confirm the exact revision for your review.
3. Send a completed [short report](EXTERNAL_REVIEW_REPORT_TEMPLATE.md), with
   examples or test output. Mark anything you did not test as **not tested**.

These tasks can be used before or after a public launch. A release number does
not establish external acceptance. The [release policy](RELEASE_POLICY.md) and
[readiness plan](V1_READINESS.md) describe the current publication gates; this
checklist does not change them or record any task as completed.

## Choose a track

| Your experience | Tasks to start with | What we need back |
| --- | --- | --- |
| Agent/framework development | R1, R6 | Scenario mappings and examples of ambiguous or lost meaning |
| Telemetry / OpenTelemetry | R2 | Event, identity, time and measurement review |
| Schemas / SDKs / data interoperability | R3–R6 | Independently generated artifacts, validator results and round-trip examples |
| Application security | R7 | Scoped security findings and reproducible negative tests |
| Running services / operations | R8 | A staging installation, restart/recovery and rollback report |
| Model-provider integrations | R9 | Actual OpenAI and Anthropic smoke results |
| First-time adoption / documentation | R10 | Steps attempted, confusing instructions and missing information |

For acceptance that specifically requires **independence**, disclose whether
you authored AIOS, receive DeepAgentLabs funding, or have editorial control over
the work. Useful feedback from affiliated reviewers is still welcome; it is
recorded as affiliated feedback. Maintainers verify these relationships.

## Specification and interoperability tasks

### R1 — Can two people describe the same agent execution the same way?

- [ ] Read the [AIOS reviewer worksheet](https://github.com/DeepAgentLabs/ai-operations-spec/blob/main/reviews/EXTERNAL_REVIEW_TASKS.md).
- [ ] Classify the shared customer-support, retry/recovery and safety/incident
  scenarios using your own framework or independent judgment. Do this before
  reading other reviewers' answers.
- [ ] Identify unclear boundaries: Run vs Workflow, Step vs model/tool call,
  retry vs a new action, evaluation vs safety, and incident vs runtime failure.
- [ ] Submit the AIOS mapping template with explanations and disagreements.

**Completion evidence:** two independent mappings covering the same scenario
set, plus a maintainer record of agreements and unresolved differences. One
partial mapping is useful progress, but does not close the whole gate.

### R2 — Do the telemetry conventions make sense?

- [ ] Review AIOS event names, lifecycle, identifiers, timestamps, correlation,
  units, privacy and extension naming against OpenTelemetry design principles.
- [ ] Compare the pinned, non-normative OTel binding with how your system emits
  telemetry. Identify dropped meaning, duplicate events or incompatible units.
- [ ] Record the upstream OTel revision you compared and examples of any mismatch.

**Send back:** a short compatibility assessment with concrete mappings and
changes requested. A span mapping alone does not establish full AIOS acceptance.

### R3 — Can an outside validator reach the expected results?

- [ ] Use a validator implementation outside DeepAgentLabs. Describe its code,
  dependencies and which semantic rules it implements.
- [ ] Run the portable suite: currently 66 artifact cases and five held-byte
  provenance-resolution cases. Use the counts in your pinned suite if it changes.
- [ ] Compare schema failures, semantic failures, unsupported versions and rule
  IDs with the expected outcomes. Report mismatches and unimplemented checks.
- [ ] Check valid records too: unknown namespaced extensions should survive;
  invalid closed-enum values and unsupported marker/type pairs should fail.

**Send back:** implementation/revision, commands and a case-by-case result file.
Running Lens, MCP or the AIOS repository's own checks is reproduction of our
implementation; it does not establish an independent validator. A JSON Schema
library alone does not evaluate the semantic or provenance-resolution rules.

### R4 — Can independently built tools exchange artifacts?

- [ ] Have at least two independent implementations produce Workflow/Run
  artifacts for the same agreed scenario; validate both without importing a
  DeepAgentLabs runtime package.
- [ ] Have two independent producers emit provenance about the **same exact
  subject bytes**, then have a consumer resolve both records from held bytes.
- [ ] Test missing bytes, changed bytes, invalid subject content and incorrect
  subject identity. Keep these outcomes distinct.
- [ ] Add an unfamiliar namespaced extension containing nested values. Pass it
  through a consumer and re-export it; compare the values before and after.
- [ ] Exercise migration/transport guidance and report any lost information or
  changes in meaning. Do not fetch reference URIs just to resolve held evidence.

**Send back:** producer/consumer identities and source revisions, sanitized input
and output artifacts, subject hashes, validation results and a round-trip diff.

### R5 — Do operational companions preserve what actually happened?

- [ ] Independently produce or review `verification_signal`, `audit_event` and
  `investigation_report` against their native source observations.
- [ ] Check unavailable judgments retain unknown/null results, permission to
  proceed is not reported as execution success, and closing an incident alone
  is not reported as verified recovery.
- [ ] Check attribution, citations, event order and unknown extensions. Use fake
  secret markers to confirm private rationale, arguments and operator details
  do not leak into the exported artifact.

**Send back:** one source-to-export example per family reviewed, including a
negative or unavailable case, and the independent consumer's output.

### R6 — Is the specification usable outside our ecosystem?

- [ ] Review concepts, relationships, events, schemas, versioning, examples,
  extensions, provenance and operational companions in dependency order.
- [ ] Flag assumptions that force you to adopt a DeepAgentLabs package or that
  cannot represent your framework accurately.
- [ ] Assess the separate provenance companion (decision D-006) and operational
  companion boundaries (D-007). Propose alternatives where needed.
- [ ] Propose a real schema/version transition from your implementation. Check
  whether the versioning rules correctly classify additive vs breaking changes
  and tell an older consumer when to accept or reject the result.

**Send back:** decisions you support or challenge, affected sections, and a
small example showing each requested change. The AIOS worksheet links the
authoritative per-layer acceptance criteria.

## Runtime and real-environment tasks

### R7 — Do the security boundaries hold?

Use an environment and accounts you are authorized to test. Start with Lens,
MCP and Tower; include Sidecar/Chaos boundaries when your scenario uses them.
Read the affected project's security policy first, for example
[MCP's policy and private reporting instructions](https://github.com/DeepAgentLabs/mcp-server/blob/main/SECURITY.md).

- [ ] Confirm valid access works. Then try missing, invalid, expired/revoked and
  wrong-role credentials where that credential lifecycle is supported.
- [ ] Try reading or changing another user's/task's data across boundaries that
  the product promises to separate. Test reader vs writer permissions.
- [ ] Test approval replay, altered approved requests and tool/path restrictions
  where those controls are documented.
- [ ] Verify exported evidence and logs do not disclose fake secret markers.
- [ ] Check the documented limits: hosted arbitrary Chaos execution is disabled;
  task controls need explicit host bindings; revocation does not cancel work
  that has already started. Flag behavior that exceeds the documented authority.

**Send back:** threat model, tested components/versions, positive and negative
cases, impact, reproduction and untested areas. Report vulnerabilities privately
using the affected repository's `SECURITY.md` / GitHub security reporting path.
Use public issues for ordinary documentation and compatibility feedback.

### R8 — Can an operator install and recover the supported system?

Start with the [Lens service guide](https://github.com/DeepAgentLabs/agenticlens/blob/main/docs/production-readiness.md),
[MCP support/rollback guide](https://github.com/DeepAgentLabs/mcp-server/blob/main/docs/release-readiness.md)
and [Tower setup guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/getting-started.md).

- [ ] Install the documented local/single-node configuration in a fresh staging
  environment. Record OS, Python, storage, package versions and configuration
  with credentials removed.
- [ ] Run a small workflow through the components you chose, inspect evidence,
  and exercise a documented failure and recovery path.
- [ ] Restart services and confirm the documented persistence behavior. Exercise
  backup/restore where supported, and upgrade/rollback with the relevant guide.
- [ ] Measure a realistic workload: describe traffic/concurrency, latency, errors
  and resource use, and compare with your stated acceptance threshold.
- [ ] Record what worked, what failed and which deployment assumptions were
  necessary. This review does not claim distributed tenancy or high availability.

**Send back:** an operator acceptance report for the tested environment. A local
test cannot certify every production configuration.

### R9 — Do the live provider integrations actually work?

- [ ] Configure explicit OpenAI and Anthropic models and credentials in your
  own approved test environment; calls may incur provider charges.
- [ ] In a Sidecar checkout, follow its provider setup guide and run
  `uv run python scripts/smoke_judge_providers.py --require-all`.
- [ ] Record each actual model, observation time, provider status and sanitized
  output. Both providers need an observed passing result for this gate.
- [ ] Report authentication/rate-limit/timeout/unavailable behavior if tested.
  `not_run`, mocks and skipped calls are not passing live evidence.

**Send back:** sanitized command/output and model selections, never API keys.
This task can be performed by an authorized operator; it does not itself supply
independent security review or prove judgment quality.
See [Sidecar judge/provider setup](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md)
and the [required-provider command and environment variables](V1_READINESS.md#remaining-required-acceptance).

### R10 — Can a newcomer follow the documentation? (Helpful feedback)

- [ ] Pick one project, follow its quickstart in a clean environment, and try
  its first example without unpublished instructions from a maintainer.
- [ ] List missing steps, broken links, confusing terms and expected vs actual
  output. Record time spent and your environment.

**Send back:** a short adoption report. This helps improve the launch but does
not substitute for R1–R9 or add a new mandatory release gate.

## Optional: reproduce the existing internal baseline

This helps orient a technical reviewer. It builds six wheels and runs our own
checks; it makes no live model calls and does not replace independent tests.
Install Git, Python 3.12+ and `uv` first. Choose an unused workspace directory.

```bash
git clone https://github.com/DeepAgentLabs/.github.git review-manager
cd review-manager
git rev-parse HEAD
python3 scripts/checkout_candidates.py --manifest release/candidate.json --workspace /tmp/aios-review-candidates
python3 scripts/accept_ecosystem.py --workspace /tmp/aios-review-candidates --output /tmp/aios-review-baseline.json
python3 scripts/release_readiness.py
```

Keep the manifest and output with your report. The readiness command can
successfully print `ready: false`: it reports missing acceptance evidence, not
just whether the internal tests pass.

## Submit your work and know what happens next

Open an issue or PR in the affected project and link this checklist's task IDs.
Cross-project reports can go to [the organization repository](https://github.com/DeepAgentLabs/.github/issues).
For AIOS mappings, submit the completed worksheet under its
`reviews/framework-mappings/` directory. Use the private security path for
vulnerabilities. Ask about attribution before sharing confidential evidence.

Maintainers then:

- [ ] Confirm reviewer attribution, independence where required, tested scope
  and exact source revisions. Preserve the original report and its reference.
- [ ] Triage each finding; link the fix, explain any disagreement, and identify
  untested or unresolved areas. Do not mark an entire gate passed for a partial review.
- [ ] Update the AIOS evidence matrix/decision log for the layers actually
  covered; prerequisite gates still apply.
- [ ] Create candidate-bound evidence receipts using the
  [readiness evidence contract](V1_READINESS.md#evidence-receipt-contract).
  Reviewers can submit ordinary Markdown and test files; maintainers handle JSON
  receipts and manifest hashes. Passing receipts require actual passing evidence.
- [ ] Decide supported scope and the stable API/schema freeze, make changes,
  rerun compatibility checks and follow the current release policy. Freezing
  contracts and publishing versions are maintainer responsibilities.

For tracking: R1/R2/R6 inform independent specification review; R3–R5 supply
independent implementation evidence; R7/R8 inform security/deployment acceptance;
R9 supplies live-provider evidence. The final stable freeze is a separate
maintainer decision. Existing per-layer criteria remain authoritative.
