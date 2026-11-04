<h1 align="center">DeepAgentLabs</h1>

## Minor releases until the coordinated v1.0 launch

Final local roadmap phases continue as minor releases: AIOS v0.7, Chaos
v0.11, Evals v0.12, Sidecar v0.10, Lens v0.13, MCP v0.7 and Tower v0.10.
Reserve v1.0 for one coordinated ecosystem release after every project's
readiness, compatibility and independent-review gates pass. No package version,
schema marker or completion status changes in this documentation update.
See the [release policy and readiness gate](RELEASE_POLICY.md).


<p align="center"><strong>Open, modular infrastructure for building, observing, evaluating, and governing AI agents in production.</strong></p>

<p align="center">
  <a href="https://deepagentlabs.io">Website</a> ·
  <a href="https://github.com/DeepAgentLabs/ai-operations-spec">Specification</a> ·
  <a href="https://mcp.deepagentlabs.io">Hosted MCP</a> ·
  <a href="ROADMAP.md">Roadmap</a>
</p>

---

## What we're building

DeepAgentLabs is a specification-first ecosystem for operating AI agents: a shared **AI Operations Specification (AIOS)** defines a vendor-neutral contract for what happens when an agent runs, and each project below is a reference implementation of that contract — observing, evaluating, supervising, stress-testing, or exposing it through a common interface.

Every component is independently usable. None of them require each other, and any team can implement the specification without depending on our Python packages.

<p align="center">
  <img src="./assets/deepagentlabs-ecosystem.webp" alt="DeepAgentLabs Ecosystem Architecture" width="100%">
</p>

## Projects

| Project | What it does |
| --- | --- |
| [**ai-operations-spec**](https://github.com/DeepAgentLabs/ai-operations-spec) | The AIOS specification: a vendor-neutral contract and shared vocabulary for runs, steps, model/tool calls, retrieval, memory, evaluations, and incidents, with draft provenance records and a portable conformance suite. |
| [**AgenticLens**](https://github.com/DeepAgentLabs/agenticlens) (`agenticlens`) | Observability, evaluation, and operational intelligence for production AI systems — what ran, why, at what cost, and how to improve it, with failure diagnosis and faulty-step attribution (0.7.0), reviewed, immutable regression suites built from traces and feedback (0.8.0), and evidence-backed model recommendations per task category (0.9.0), and advisory runtime routing from that evidence (0.10.0), and evidence-backed optimization recommendations with post-adoption outcome tracking (0.11.0). |
| [**Agentic Evals**](https://github.com/DeepAgentLabs/agentic-evals) (`agentic-evals`) | A standalone, framework-agnostic scoring engine for LLM and agent outputs, with declarative suite/live evaluation, release gates, and JSON/JUnit/Markdown CI output (0.8.0), plus judge cost, bounded retries, unavailable-judge gating, sampling agreement, and live-target timeouts and async runs (0.9.0), and AIOS evaluation evidence export (0.10.0). |
| [**Agentic Sidecar**](https://github.com/DeepAgentLabs/agentic-sidecar) (`agentic-sidecar`) | A real-time supervision layer that checks an agent's plans and actions against intent, policy, risk, and budget before they execute. |
| [**Agentic Chaos**](https://github.com/DeepAgentLabs/agentic-chaos) (`agentic-chaos`) | A fault-injection toolkit that deliberately breaks agent workflows to measure resilience and recovery, with circuit breakers and dry-run previews (0.5.2), AgenticLens diagnosis span markers (0.5.3), a pytest plugin with fail-closed resilience contracts (0.6.0), cascades, threshold search, synthetic response poisoning and cost estimates (0.7.0), gated multi-stage chaos workflows, linted declarative experiments, explosion-radius scopes and topology fuzzing (0.8.0), and pre/during/post resilience probes with a 0–100 resilience score, bounded score trends and a `--min-score` CI gate (0.9.0). |
| [**MCP Server**](https://github.com/DeepAgentLabs/mcp-server) (`deep-agentic-core-mcp`) | A single MCP interface that exposes workflow inspection, evaluation, and chaos/resilience tooling to AI clients. |
| [**AgenticOps Control Tower**](https://github.com/DeepAgentLabs/agenticops-control-tower) | An operations control plane for inventory, evidence posture, cited MCP investigation and approved verified staging recovery (0.6.0), plus approved fleet desired settings and bounded stop/MCP-revocation coordination (0.7.0), periodic local detection, durable alerts and joined incident console views (0.8.0), and versioned runbooks with exact-digest approval, bounded steps, compensation and verified recovery (0.9.0). |

See the [roadmap](ROADMAP.md) for how these pieces fit together and what's being built next.

**Sidecar v0.8: Shared & Exclusive context/intent and guardrails.** Users may choose
context only, guardrails only, or both, independently Shared across a system/task
or Exclusive to designated agent(s). Each agent receives shared plus assigned
exclusive context; shared guardrails remain mandatory alongside exclusive rules.
v0.8 provides scoped configuration, delivery and composition; v0.9 validates
privacy, authority and lifecycle behavior; v0.10 prepares contracts for the coordinated ecosystem v1.0 freeze. Explicit host context delivery is implemented; automatic prompt rewriting and
end-to-end private-context isolation are not claimed. Lens 0.7.1 reads correlated
decisions; Semantica export remains conditional.

See the [Sidecar acceptance criteria](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/ROADMAP.md#shared--exclusive-context-and-guardrails).

## Principles

- **Specification-first** — the contract comes before SDK ergonomics, dashboards, or integrations.
- **Modular** — each project is independently installable and useful on its own.
- **Runtime and framework agnostic** — works alongside LangGraph, CrewAI, the OpenAI Agents SDK, AutoGen, LlamaIndex, and custom agent stacks.
- **Open source** — released under permissive licenses; see each repository for its license.

## Get involved

Found a bug or have an idea? Open an issue or discussion on the relevant repository above. Most projects also publish to PyPI — search for the package name shown next to each project.

## AgenticLens 0.11.0: optimization intelligence

[AgenticLens 0.11.0](https://github.com/DeepAgentLabs/agenticlens/releases/tag/v0.11.0) is released. Roadmap v0.9 turns recorded traces into recommendations you can act on and then check:

- `agenticlens optimize analyze` ranks opportunities across prompts (caching, compression), retrieval (top-k pruning, reranking), memory (summarization, retention), tools (result caching, non-retryable errors), workflows (redundant steps, handoffs that add no work) and models (quality-cost trade-offs between variants). Each cites the runs and spans it came from.
- Projected benefit (with its basis), confidence (with reasons) and quality risks are separate fields and never netted. Cost stays unavailable when any span lacks a recorded cost.
- An append-only ledger tracks accepted, rejected, adopted and reverted recommendations, and `agenticlens optimize outcome` reports projected and observed results side by side after adoption, failing CI when quality regressed.

[MCP 0.4.3](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.3) adds read-only `lens.optimization_analyze` and pins hosted Lens 0.11.0. Sidecar's locked integration CI moves to Lens 0.11.0. Evals, Chaos, Tower and the spec need documentation only; optimization artifacts are Lens-local. Next for Lens is v0.13, production and enterprise readiness, ahead of the coordinated ecosystem v1.0 release. See the [optimization guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.11.0/docs/optimization.md).

## Tower 0.6.0: investigation to verified recovery

Phase 6 and Phase 6A ship as one release, paired with MCP 0.3.6. The supported
first runtime is a deterministic staging dependency fixture: detect, investigate
with cited Lens evidence, preview, obtain separate human approval, execute once
and verify fresh Lens/Evals evidence plus a probe. Failed recovery escalates.
Thin Sidecar stop/restart and native MCP revocation adapters preserve runtime
ownership. Production orchestration and hosted tenant credential binding remain
planned. [Walkthrough and scope](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/incident-recovery.md).

## MCP 0.4.0: unified release checks

[MCP 0.4.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.0) completes Phase 4 with its unified workflows, so a host can ask "is this ready?" across packages in one call:

- **`core.release_check`** gates a Lens baseline/candidate comparison, a native Evals report and a Chaos run report. It **fails closed**: each gate is `passed`, `failed`, `invalid` or `missing`. Malformed or failed-call evidence blocks the release, as does missing evidence of a required kind (all three by default; `required_evidence` narrows that).
- **Evals judges the evaluation** through its own release gate (every `GateConfig` threshold, strict by default, unknown keys rejected). Lens validates the comparison, and Chaos crashes or timeouts block the release while injected faults alone do not.
- **`core.incident_summary`** reports only failure signals, and **`core.export_report`** returns the session's evidence as an MCP-local envelope, not an AIOS artifact.
- **`core.compare_runs`** shares the `lens.compare_runs` path.

All four work on the hosted server; hosted callers pass a locally produced chaos report because remote chaos execution stays disabled. No sibling runtime change, dependency bump or patch release is needed, and Tower's `>=0.3.6,<1` range already admits 0.4.0. MCP 0.5.0 (Phase 5) adds hosted access control: per-key tool permissions, revocation at dispatch and correlated denial evidence. See the [unified workflows guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.4.0/docs/unified-workflows.md).

## Evals 0.10.0: AIOS evaluation evidence export

[Evals 0.10.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.10.0) is released. Evaluation results now travel with the run they judged:

- `to_aios_evidence` turns every score, case verdict and gate decision into an AI Operations Specification `0.4-draft` `evaluation` with criterion, method, result and score, plus an `evaluates` link to the Step or object each case is mapped to. `attach_aios_evidence` merges it into an existing Run, such as a Chaos `to_aios_run` export. `agentic-evals aios export` is the CLI path.
- Nothing is guessed. A missing mapping, an unmapped case or a target missing from the Run fails loudly. Skipped scores are `skipped`, undelivered judgments are `unavailable`, and cases with no observed output are reported rather than exported.
- Merged Runs pass MCP's `spec.validate_artifact` with `conformance.aligned = true`, and Lens's `agenticlens validate` agrees.

Native report schema 1.0 is unchanged. [MCP 0.4.2](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.2) pins Evals 0.10.0 in its hosted images and tests the export with `spec.validate_artifact`. Tower moves its development pin. Lens, Sidecar, Chaos and the spec need documentation only, and the spec now holds an Evals-produced review artifact. Evals v0.11 adversarial containment scoring is now released as 0.11.0 with bounded authenticated observations. See the [AIOS evidence guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.10.0/docs/aios-evidence.md).

## Evals 0.9.0: judge reliability, cost and live-target resilience

[Evals 0.9.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.9.0) is released. LLM-judged and live evaluations now report what they cost and whether they actually happened:

- **Judge cost and latency** on every judge score, under the `judge_*` keys AgenticLens already reads, totalled in `summary.judge` and kept apart from the agent's own cost.
- **Bounded retries and an explicit unavailable outcome.** A judge that fails after its retries never passes, and the default gate fails and names the affected cases.
- **Repeated judging** (`samples=N`) with per-case agreement, so a flaky judge is detected (`min_judge_agreement`) instead of averaged away.
- **Live-target resilience:** retries with backoff, and per-case `timed_out` / `error` kept apart from wrong answers (`summary.live`, JUnit `<error>`, gate limits).
- **Async** evaluators and targets: `aevaluate_suite` and `arun_live_suite`.

Report schema 1.0 gains optional fields only. [MCP 0.3.14](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.14) and [Control Tower 0.7.1](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.7.1) bundle the 0.9.0 schemas. Tower also projects judge and live outcomes into evaluation evidence, and MCP's hosted images pin Evals 0.9.0. Lens 0.10.0 passes unchanged on its existing `>=0.7.1,<1` range. Chaos, Sidecar and the spec need documentation only. Next is v0.10, AIOS evaluation evidence export. See the [judge reliability guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.9.0/docs/judge-reliability.md).

## Evals 0.8.0: declarative evaluation and release gates

[Evals 0.8.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.8.0) is released: `evaluate` handles YAML/JSON
suites and JSON/JSONL samples, `live` calls Python/HTTP targets with concurrency,
`gate` applies release policy, and `pack list/show` discovers built-in packs.
CI can retain native JSON evidence and produce JUnit XML or Markdown summaries.
Evaluation writes evidence even for failures; gate exit codes are 0 pass,
1 failed policy and 2 invalid input/usage. A worked GitHub Actions workflow and
the voice-agent example exercise this path.

Lens approved suite exports remain compatible. MCP and Tower validate native
JSON with their existing 0.7.2 schemas; report schema 1.0 is unchanged. Chaos
and Sidecar remain independent producers, and native reports do not imply AIOS
conformance. No sibling runtime dependency bump or patch release is required.
See the [CLI guide and compatibility matrix](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.8.0/docs/cli.md).

The published native report/gate contract introduced in 0.7.2 remains
supported. v0.9 judge reliability, cost and live-target resilience shipped in
0.9.0; AIOS evaluation evidence export remains planned for v0.10.

## Native Evals contract adoption

MCP 0.3.8 exposes offline `evals.validate_artifact` and validates native reports
in Lens analysis/audit/SLO tools. Tower 0.6.1 validates full Evals reports and
gates before evidence projection; malformed evidence is unavailable. Bundled
upstream 0.7.2 schemas keep both consumers independent of runtime sibling
installations. This is native structural validation, not AIOS conformance.

## AgenticLens 0.9.0: ModelFit

AgenticLens 0.9.0 recommends a model per task category from recorded
experiment reports. Hard constraints on quality, cost, latency, safety,
provider and deployment fail closed, so a limit the evidence cannot verify
rejects the candidate. Each recommendation carries a confidence level with
reasons, an explanation, alternatives, a fallback (on a different provider
when one is feasible),
savings against a reference model tied to the experiment report's SHA-256, and
the quality risks of switching, plus a task-level model matrix. MCP 0.3.11 adds
read-only `lens.modelfit_recommend`; Sidecar 0.8.4 widens its optional Lens
extra to `<1`. ModelFit recommends; runtime routing is Lens v0.8. See the
[guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.9.0/docs/modelfit.md).

## AgenticLens 0.8.0: test-suite and dataset management

AgenticLens 0.8.0 builds regression suites from CSV/JSON imports, production
traces and user feedback. It masks PII by default before storage, flags duplicates and
conflicting labels, adds synthetic variations and stable splits, and records
reviews. Approved suites become immutable, hash-verified versions that CI
verifies, exports and evaluates. Suites stay plain agentic-evals `TestSuite`
files. MCP 0.3.9 adds read-only `lens.suite_from_traces` and `lens.suite_check`;
Sidecar 0.8.2 widens its optional Lens extra to 0.8. PII detection is pattern
based and approvals are not authenticated. See the
[guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.8.0/docs/suite-management.md).

## Chaos 0.7.0 interoperability

Chaos 0.7.0 adds sequential fault cascades, deterministic monotonic breaking-point
search, synthetic response poisoning (including prompt/tool-response instruction
and policy-bypass payloads), and explicit-price retry cost estimates. Native
child event IDs and fault types remain intact; cascade IDs/stages and poisoning
strategy/payload/seed are additive event detail. Existing report readers and
AIOS exports remain compatible.

See the [v0.7 guide and offline synthetic example](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.7.0/docs/v0.7.md).
The example includes observed synthetic dispatches and a bypassed negative
control. Injection or recovery alone does not prove containment. No new shared
schema, automatic adapter, hosted execution capability or containment guarantee
is introduced.

Chaos 0.7.0 ships this milestone; Sidecar 0.8.3 admits its optional dependency and MCP 0.3.10 updates published image pins. Lens, Evals, Tower and AIOS need no runtime releases.

## Control Tower 0.7.0 fleet operations

Tower 0.7.0 adds frozen environment/capability targeting, bulk desired settings,
separate approval, durable per-target results and bounded stop/MCP-revocation
acknowledgement through Python, HTTP and CLI. No fleet atomicity or automatic
rollback/resume is claimed. Timed-out/requested commands need host reconciliation.

Tower owns fleet coordination, Sidecar owns dispatch enforcement, issuers own credential revocation, Lens owns analysis, Evals owns scoring and Chaos owns controlled faults. AIOS remains the shared-semantics authority.

Existing optional dependency ranges remain sufficient. No sibling runtime or
native evidence schema changes are required; this documentation alignment needs
no patch release. See the [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.7.0/docs/fleet-operations.md).

See the [local Tower compatibility guide](tower-0.7-fleet-operations.md) for the operator workflow and package boundaries.

## AgenticLens 0.10.0 routing compatibility

AgenticLens 0.10.0 implements roadmap v0.8: evidence-based runtime model
selection, fail-closed routing constraints, bounded provider failover,
confidence/escalation handoffs, shadow/canary modes and a local routing journal.
The default is advisory; execution uses explicit caller-owned callbacks.
MCP 0.3.12 exposes read-only `lens.routing_decide` and pins hosted Lens 0.10.0.
See the [routing guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/docs/routing.md)
and [offline example](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/examples/routing_demo.py).

Lens owns model selection and recorded routing outcomes. Sidecar retains
pre-action authority and approvals; Chaos retains fault injection; Evals retains
scoring/gates; Tower retains fleet control and native evidence posture; AIOS
remains the shared contract authority. Routing schemas stay Lens-local.
Only MCP needs a patch release (0.3.12); existing Chaos, Evals and Sidecar ranges
already admit Lens 0.10.0, and Tower/AIOS need no runtime/schema change.

## Chaos 0.8.0 interoperability

Chaos 0.8.0 adds:

- multi-stage chaos workflows: steps, steady-state health checks, parallel
  branches, approval gates that can be resumed, and reusable templates
- declarative YAML/JSON/TOML experiments, with validation that never executes
  targets and cron schedule previews
- `Scope` explosion-radius control (steps, providers and exclusions) on every
  built-in fault and `cascade()`; custom faults get it by calling
  `BaseFault.__init__`, setting `scope` or overriding `in_scope()`
- a topology fuzzer that weights fault placement by fan-out

Native event IDs and fault types are unchanged. Workflow provenance
(`detail.workflow`) and an optional `ChaosReport.workflow` summary are
additive. A workflow's steps merge into one native report for contracts and
AIOS export.

See the [v0.8 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.8.0/docs/v0.8.md)
and the [offline examples](https://github.com/DeepAgentLabs/agentic-chaos/tree/v0.8.0/examples/workflows).
Workflow statuses, health checks and fuzz outcomes are resilience evidence.
They are not scores, release gates or proof of containment. No new shared
schema, automatic adapter or hosted execution capability is introduced.

Chaos 0.8.0 ships this milestone. Sidecar 0.8.5 admits it as an optional dependency, and MCP 0.3.13 updates the published image pins. Lens, Evals, Tower and AIOS need no runtime releases.

## Sidecar 0.9.0 — authority, privacy and evidence

Sidecar now enforces explicitly bound task authority with narrowed delegation,
ancestor revocation and dispatch-time expiry checks. Scoped context has explicit
reader access and redacted summaries; framework transport and process isolation
remain host responsibilities. Native Decision and sidecar.correlation/1 remain
compatible. Sidecar contract readiness continues in v0.10; the stable freeze belongs to the coordinated ecosystem v1.0 release.

The reproducible 24-run synthetic comparison records 0/6 unsafe dispatches with
Sidecar and 2/6 clean false interventions during gate/provider outages. Chaos 0.8
injects faults; Evals 0.9 scores supplied observations; Lens reads native evidence;
Tower keeps governance outcomes separate from deployment health; MCP discovers
installed capability without connecting to a task; AIOS retains schema ownership.

See the [v0.9 guide and migration notes](https://github.com/DeepAgentLabs/agentic-sidecar/blob/v0.9.0/website/docs/v0.9.md).
Only Sidecar needs the 0.9.0 feature release. MCP receives a 0.4.1 compatibility
patch; other siblings retain compatible dependency ranges and need no runtime release.

## AIOS v0.6 canonical examples and extension model

[AI Operations Specification v0.6.0](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.6.0/specification/v0.6)
adds exploratory canonical minimal/advanced artifacts, retry examples, schema
and semantic negative controls, and third-party extension guidance. Offline
validation uses the existing v0.4 schemas; artifact markers remain `0.4-draft`.
Independent review is still pending; this repository release does not freeze
any layer or establish stable conformance. Provenance objects and a portable
conformance suite remain v0.6.x work.

Lens and Chaos exports, MCP schema routing, Evals reports, Sidecar decisions and
Tower evidence retain their existing contracts and ownership. No sibling runtime
dependency floor changes or package patch releases are required. See the
[compatibility matrix and offline example workflow](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.0/docs/v0.6-ecosystem.md).

## Control Tower 0.8.0 live operations

See [operator compatibility and ownership](tower-0.8-live-operations.md) for
periodic detection, durable alerts, acknowledgements and joined incident console
views. Existing native contracts and optional dependency ranges remain compatible;
no runtime or patch release is required here.

## Chaos 0.9.0 interoperability

Chaos 0.9.0 adds:

- resilience probes: `HttpProbe`, `ResponseQualityProbe`, `LatencyProbe` and
  `FunctionProbe` check steady state before chaos, while faults are active and
  after recovery. By default no fault is injected when a pre-chaos probe
  fails; `require_steady_state=False` runs the chaos anyway and leaves the
  score inconclusive
- a 0-100 resilience score built from recovery, probe, latency,
  retry-efficiency and cost evidence, with per-fault verdicts. Components a
  run cannot show (for example latency without a baseline) are left out and
  the remaining weights renormalized. The score is inconclusive (`null`) after
  a failed pre-chaos probe, for dry runs, when no fault fired, or when no
  component can be computed
- a local run-history store for score trends, with `max_runs` and
  `max_age_days` retention, and a `--min-score` CI gate
- probes and scoring on chaos workflows, experiment files and the pytest marker

Native event IDs and fault types are unchanged. `ChaosReport.probes`,
`ChaosReport.resilience` and the matching `WorkflowReport` fields are optional
and additive. When a score was computed, AIOS exports add a derived
`resilience_score` measurement; inconclusive runs export none. Probe results
and the score breakdown stay in the `io.deepagentlabs.agentic-chaos`
producer extension.

See the [v0.9 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/docs/v0.9.md)
and the [offline demo](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/examples/chaos_resilience_demo.py).
The resilience score summarizes the evidence of one chaos run. It is not an
Evals score, a release-gate decision, a deployment health signal or proof of
containment. No new shared schema, automatic adapter or hosted execution
capability is introduced.

Chaos 0.9.0 ships this milestone. Sidecar 0.9.1 admits it as an optional dependency, and MCP 0.4.4 updates the published image pins. Lens, Evals, Tower and AIOS need no runtime releases.

## AIOS v0.6.1 provenance records and conformance suite

[AI Operations Specification v0.6.1](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.6.1/specification/v0.6)
is the first v0.6.x increment. Exploratory `0.6-draft` provenance records
describe where a finding came from (subjects with optional digests, source
references, derived findings and evidence lineage) without changing any
`0.4-draft` Run or Workflow. A portable conformance suite gives every case an
expected outcome and rule citations so implementations can check themselves
offline, and naming conventions are now documented and tested. Independent
review is still pending; no layer freezes and stable conformance is not
claimed. A verified, resolved source never shows that a finding is true.

Running the suite through DeepAgent MCP surfaced two `0.4-draft` divergences,
fixed in MCP 0.4.5. Lens, Chaos, Evals, Sidecar and Tower keep their existing
contracts and dependency ranges and need no release. See the
[sibling compatibility guide](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.1/docs/v0.6.1-ecosystem.md).

## MCP 0.5.0: hosted access control

[MCP 0.5.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.5.0) completes MCP Phase 5 with hosted access control. Each hosted key can carry allow and deny tool globs, an expiry and a task scope. The server enforces them at dispatch, outside the model: before each hosted handler runs, it re-authenticates the key and reloads its policy. Revocation, a narrower policy or expiry therefore stops queued calls, retries and calls on existing connections. Calls already running finish. Allowed calls log a `dispatch` and a `completion` record. Denied calls instead return and log a `denial` or `revocation_acknowledged` record and never reach the handler. Every record uses the MCP-local `mcp.access-decision.v1` shape, and the records of one call share a `correlation_id`. They are not AIOS artifacts. `core.access_status` reports a key's effective policy, and operators use `deep-agentic-core-mcp-admin` to narrow or revoke a key by user ID.

Tower's MCP revocation adapter is unchanged and now also stops queued calls.
Hosted chaos execution and `tower.*` stay disabled, and a policy cannot widen
the hosted surface. Lens, Chaos, Evals, Sidecar, Tower and the spec need
documentation only, with no dependency or pin changes. Next for MCP is Phase 6:
hosted Tower credentials, an authenticated Sidecar stop/revoke bridge and a
shared AIOS access-evidence format. See the
[hosted access control guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.5.0/docs/access-control.md).

## Control Tower 0.9.0 runbooks

See [operator compatibility and ownership](tower-0.9-runbooks.md) for versioned runbooks,
exact-digest approval, bounded steps, compensation, cancellation and verified
recovery. Existing native contracts and optional dependency ranges remain
compatible. MCP 0.5.1 adds local `tower.runbook*` tools; the other siblings need
documentation only.

### Lens 0.12 execution evidence

Lens 0.12 implements authenticated ordered-record snapshots, explicit coverage,
HMAC trust-store verification and offline record replay. This Lens-local format
is not a shared AIOS execution ledger. Lens now exports/imports AIOS 0.4-draft execution Runs through a lossless
namespaced mapping, and MCP 0.5.2 and Tower 0.9.1 delegate verification with host-owned trust
and redacted causal IDs. Shared canonical access-event semantics remain draft work. See the
[Lens verification guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.12.0/docs/evidence-verification.md).

## Next coordinated release: MCP Phase 6 and Chaos containment validation

MCP's authenticated Sidecar stop/revoke integration and Chaos containment tests
are one planned delivery, published as coordinated sibling releases. Target MCP
0.6.0 plus a Chaos 0.9.x validation patch (0.10.0 if public APIs change).
Validate candidate wheels together and publish the tested version matrix before
closing the milestone. Other siblings get patches only when compatibility needs
one.

The shared gate requires zero forbidden dispatches after effective stop/revoke
acknowledgement across queues, retries, existing sessions and delegated access.
Report in-flight effects separately. Use actual execution observations, require a
bypassed negative control to fail, and reject missing or failed/unknown/incomplete
verification as a passing result. Chaos runs on isolated synthetic targets; MCP's
hosted arbitrary-chaos restriction remains. Evals v0.11 scoring now ships in 0.11.0 after this
paired release.

See [MCP's release gate](https://github.com/DeepAgentLabs/mcp-server/blob/main/ROADMAP.md#coordinated-mcp-and-chaos-release-planned)
and [Chaos's acceptance criteria](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/ROADMAP.md#required-paired-release-acceptance).

## MCP Phase 6 coordinated containment delivery

MCP 0.6.0 adds hosted Tower user bindings, authenticated task-scoped Sidecar
stop/revoke, guided setup and saved-report recall. Chaos 0.10.0 authenticates
observed containment scenarios with Lens 0.12.0; Sidecar 0.9.2 widens its optional
Chaos ranges. Evals 0.10.0, Tower 0.9.0 and AIOS 0.6.1 remain compatible.
CI and paired publication close the release gate. Evals v0.11 scoring subsequently shipped in 0.11.0. Running side effects and uninstrumented boundaries remain explicit limits;
hosted arbitrary chaos execution stays disabled. See the
[operator guide and acceptance matrix](https://github.com/DeepAgentLabs/mcp-server/blob/c18f73decdc75aaac3e2e95004ae88589d587e75/docs/phase6-containment.md).

## Evals 0.11 containment scoring — 2026-11-03

Evals 0.11.0 adds required containment judgments over authenticated, bounded
dispatch/completion and denial observations, with six reusable stop/revoke,
denied-tool, authority, injected-instruction and fail-closed scenarios.
Lens 0.12.1 synchronizes embedded Evals schemas and failed live-target trials;
its 0.12 integrity API verifies snapshot integrity; coverage remains producer-declared.
Chaos 0.10 and Sidecar 0.9.2 own attacks and enforcement; MCP 0.6.1 pins
Evals 0.11 and checks real dispatch negative controls. Tower 0.9 reads the
unchanged report/gate schema 1.0. AIOS 0.6.1 and its exploratory access profile
gain no normative schema or universal containment claim.
See [the guide and executable passing/failing fixtures](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/containment.md).

## AIOS v0.7.0 interoperability guidance — 2026-11-03

AIOS repository v0.7.0 delivers a [migration guide](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/specification/v0.6/migration-guide.md),
a [non-normative OpenTelemetry companion](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/specification/v0.6/otel-binding.md)
pinned to upstream 1.37.0 with complete canonical-event coverage and a tested
retry projection, plus a strict MkDocs build and main-only Pages publishing.
Run/Workflow remain `0.4-draft`; provenance remains `0.6-draft`. Independent
review and producer/consumer acceptance gates remain open. Verification-signal,
audit-event and incident-summary shapes still require implementation evidence.
Lens, Chaos, Evals, Sidecar, MCP and Control Tower need documentation alignment
only: no dependency floors, runtime adapters or sibling patch releases change.
See the [compatibility matrix and offline commands](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/docs/v0.7.0-ecosystem.md).

## Evals 0.12 readiness — 2026-11-04

Evals 0.12.0 implements the final local API/report readiness phase: candidate
root API and current-schema compatibility baselines, every registered offline
Python example exercised in CI, CPython 3.10-3.14 support, and pinned
Lens 0.12.1 / Tower 0.9.1 / MCP 0.6.1 downstream candidate validation.
Native report/gate schema 1.0 and AIOS 0.4-draft exports are unchanged.

MCP and Tower validation pins advance in patch releases after Evals publication;
Lens, Chaos, Sidecar and AIOS need documentation alignment only. Stable APIs,
the >=1.0,<2 downstream matrix and coordinated release-candidate acceptance
remain open gates for the ecosystem v1.0 launch. See
[the implementation, support matrix and remaining gates](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.12.0/docs/support-policy.md).

## Sidecar 0.10 contract readiness — 2026-11-04

Sidecar publishes candidate intent, decision, audit, scope and transfer contracts
with migration tests and an offline cross-instance/cross-agent propagation
example. Receiving hosts preserve constraints, narrow authority and consult a live
parent registry; disconnected authorization remains out of scope. AIOS hosts
[non-normative schemas and mappings](https://github.com/DeepAgentLabs/ai-operations-spec/tree/main/drafts/sidecar-contracts-v1).
Native correlation, containment receipts, scoring and deployment health retain
their separate meanings. MCP 0.6.3 image recipes pin Sidecar 0.10.0; package
publication does not update hosted infrastructure. Coordinated v1.0 remains open.

## Lens 0.13 production readiness candidate — 2026-11-04

Lens 0.13.0 delivers the local enterprise readiness candidate: single-node
organization/project artifact storage, scoped bearer roles, atomic audit,
immutable model/prompt metadata registries, mandatory pattern redaction, trace
retention, reproducible Evals gate receipts and candidate container/Helm recipes.
Existing native schemas remain unchanged. MCP 0.6.4 pairs hosted Lens 0.13.0;
Chaos 0.10.0, Evals 0.12.0, Sidecar 0.10.0 and Tower 0.9.1 ranges remain compatible.
AIOS requires no runtime/schema change. Sibling docs/examples are aligned without
unnecessary package releases. See the [Lens guide and security boundaries](https://github.com/DeepAgentLabs/agenticlens/blob/v0.13.0/docs/production-readiness.md).

Local audit integrity is not verified, metadata export is not certification and
pattern redaction is not comprehensive PII discovery. Independent security review,
operator deployment acceptance and stable API freeze remain open for coordinated
ecosystem v1.0. Publishing these packages does not deploy a new hosted service.

## Control Tower 0.10 capability contract readiness

Tower 0.10 implements the Tower-local `tower.capabilities.v1` candidate:
authenticated discovery of registration, heartbeat and readback schemas with
explicit status semantics. CPython and Node.js clients are validated over live
HTTP, including durable SQLite readback. See the [contract, examples and migration policy](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.10.0/docs/capability-contract.md).
Existing native sibling schemas, optional dependency ranges and evidence/health
boundaries are unchanged. The initial Tower delivery used documentation-only sibling updates. The
MCP 0.6.5 follow-up below adds runtime discovery and its own patch publication. Production runtime connectors, independent
ecosystem acceptance and the coordinated v1.0 stable freeze remain open.

Operator discovery against a running Tower 0.10 server:

```bash
curl --fail -H "Authorization: Bearer $AGENTICOPS_READ_TOKEN" \
  "$AGENTICOPS_API_URL/contracts/capabilities"
```

Expect `contract_version: tower.capabilities.v1` and `maturity: candidate`.

## MCP 0.6.5 Tower discovery

MCP 0.6.5 exposes read-only `tower.capability_contract` over Tower 0.10's
candidate contract endpoint. Hosted access reuses per-user reader bindings and
MCP dispatch policy; local operators configure the Tower reader credential.
Native schemas and optional dependency boundaries are unchanged. The MCP runtime implementation needs the 0.6.5 patch release; this profile
update and Tower companion docs need no package release. Package publication
does not deploy the hosted service.
See the [operator guide and example](https://github.com/DeepAgentLabs/mcp-server/blob/main/docs/tower-0.10-compatibility.md).

## ChaosHub 0.11 delivery — 2026-11-04

Agentic Chaos 0.11.0 delivers six offline instrumented-call recipes, commit-pinned
opt-in GitHub list/search/pull, contribution staging through ordinary PRs and
explicitly loaded BaseFault entry-point plugins. The generic scenarios use
existing fault primitives; specialized provider/vector-store integrations are
not implied. Native reports and AIOS exports remain unchanged. Sidecar 0.10.1
widens optional ranges and MCP 0.6.6 updates image pins; Lens 0.13.0, Evals 0.12.0,
Tower 0.10.0 and AIOS repository 0.7.0 require documentation alignment only.

```bash
agentic-chaos hub search rag
agentic-chaos chaos run examples/chaoshub_app.py --experiment rag-context-poisoning --save hub-report.json
```

Use [the ChaosHub guide and offline example](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/v0.11.md)
from a Chaos checkout. Availability is not response quality or containment;
remote recipes require review and target binding. Shared v1.0 stability and
independent AIOS acceptance remain open.
