<h1 align="center">DeepAgentLabs</h1>

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
| [**ai-operations-spec**](https://github.com/DeepAgentLabs/ai-operations-spec) | The AIOS specification: a vendor-neutral contract and shared vocabulary for runs, steps, model/tool calls, retrieval, memory, evaluations, and incidents. |
| [**AgenticLens**](https://github.com/DeepAgentLabs/agenticlens) (`agenticlens`) | Observability, evaluation, and operational intelligence for production AI systems — what ran, why, at what cost, and how to improve it, with failure diagnosis and faulty-step attribution (0.7.0), reviewed, immutable regression suites built from traces and feedback (0.8.0), and evidence-backed model recommendations per task category (0.9.0), and advisory runtime routing from that evidence (0.10.0). |
| [**Agentic Evals**](https://github.com/DeepAgentLabs/agentic-evals) (`agentic-evals`) | A standalone, framework-agnostic scoring engine for LLM and agent outputs, with declarative suite/live evaluation, release gates, and JSON/JUnit/Markdown CI output (0.8.0). |
| [**Agentic Sidecar**](https://github.com/DeepAgentLabs/agentic-sidecar) (`agentic-sidecar`) | A real-time supervision layer that checks an agent's plans and actions against intent, policy, risk, and budget before they execute. |
| [**Agentic Chaos**](https://github.com/DeepAgentLabs/agentic-chaos) (`agentic-chaos`) | A fault-injection toolkit that deliberately breaks agent workflows to measure resilience and recovery, with circuit breakers and dry-run previews (0.5.2), AgenticLens diagnosis span markers (0.5.3), a pytest plugin with fail-closed resilience contracts (0.6.0), cascades, threshold search, synthetic response poisoning and cost estimates (0.7.0), and gated multi-stage chaos workflows, linted declarative experiments, explosion-radius scopes and topology fuzzing (0.8.0). |
| [**MCP Server**](https://github.com/DeepAgentLabs/mcp-server) (`deep-agentic-core-mcp`) | A single MCP interface that exposes workflow inspection, evaluation, and chaos/resilience tooling to AI clients. |
| [**AgenticOps Control Tower**](https://github.com/DeepAgentLabs/agenticops-control-tower) | An operations control plane for inventory, evidence posture, cited MCP investigation and approved verified staging recovery (0.6.0), plus approved fleet desired settings and bounded stop/MCP-revocation coordination (0.7.0). |

See the [roadmap](ROADMAP.md) for how these pieces fit together and what's being built next.

**Sidecar v0.8: Shared & Exclusive context/intent and guardrails.** Users may choose
context only, guardrails only, or both, independently Shared across a system/task
or Exclusive to designated agent(s). Each agent receives shared plus assigned
exclusive context; shared guardrails remain mandatory alongside exclusive rules.
v0.8 provides scoped configuration, delivery and composition; v0.9 validates
privacy, authority and lifecycle behavior; v1.0 stabilizes contracts. Explicit host context delivery is implemented; automatic prompt rewriting and
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

## Tower 0.6.0: investigation to verified recovery

Phase 6 and Phase 6A ship as one release, paired with MCP 0.3.6. The supported
first runtime is a deterministic staging dependency fixture: detect, investigate
with cited Lens evidence, preview, obtain separate human approval, execute once
and verify fresh Lens/Evals evidence plus a probe. Failed recovery escalates.
Thin Sidecar stop/restart and native MCP revocation adapters preserve runtime
ownership. Production orchestration and hosted tenant credential binding remain
planned. [Walkthrough and scope](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/incident-recovery.md).

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
supported. Next is v0.9 judge reliability, cost and live-target resilience;
AIOS evaluation evidence export remains planned for v0.10.

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
