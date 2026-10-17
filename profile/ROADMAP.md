# DeepAgentLabs Roadmap

> DeepAgentLabs should be built **specification-first** toward an **open operational standard for AI systems**.

The AI Operations Specification comes before SDK ergonomics, package features, dashboards, or integrations. The specification is the foundation; the packages are reference implementations of that foundation.

## 🧭 Direction

DeepAgentLabs should follow the pattern used by the strongest ecosystems:

| Ecosystem     | Defined first                            |
| ------------- | ---------------------------------------- |
| OpenTelemetry | Telemetry model and semantic conventions |
| Kubernetes    | API objects                              |
| OpenAPI       | Interface specification                  |

The specification should stay above any one package. Multiple tools should share the same operational contract, and third parties should be able to implement that contract without depending on the Python packages directly.

## 🏗️ Specification-First Architecture

```mermaid
flowchart TB
    Spec["AI Operations Specification"]
    Spec --> Concepts["Core Concepts"]
    Spec --> Conventions["Semantic Conventions"]
    Spec --> Schemas["JSON Schemas"]
    Spec --> Versioning["Versioning"]
    Spec --> Examples["Examples"]
    Spec --> Extensions["Extension Model"]
    Concepts --> Implementations["Reference Implementations"]
    Conventions --> Implementations
    Schemas --> Implementations
    Versioning --> Implementations
    Examples --> Implementations
    Extensions --> Implementations
    Implementations --> Lens["AgenticLens"]
    Implementations --> Chaos["Agentic Chaos"]
    Implementations --> Sidecar["Agentic Sidecar"]
    Implementations --> MCP["DeepAgent MCP"]
    Implementations --> Tower["AgenticOps Control Tower"]
```

The **AI Operations Specification is the foundation**. It defines the shared concepts, conventions, schemas, versioning, examples, and extension model before package-specific behavior.

The packages are **reference implementations** of that foundation. They should not invent a parallel operational model or independent package types; Python models should represent the specification directly.

This separation keeps the specification above any one package and makes it possible for third parties to implement the contract without taking a dependency on the Python packages.

## 🗺️ Ecosystem Build Journey

This overview groups the numbered phases to make the progression easier to scan; the detailed phase goals follow below.

```mermaid
flowchart TB
    subgraph Foundation["PHASES 1–5 · FOUNDATION"]
        P1["AI Operations Specification"] --> P2["Relationships"] --> P3["Semantic Conventions"] --> P4["JSON Schemas"] --> P5["Python Models"]
    end
    subgraph Operational["PHASES 6–9 · OPERATIONAL LAYERS"]
        P6["AgenticLens"] --> P7["Agentic Chaos"] --> P8["DeepAgent MCP"] --> P9["Agentic Sidecar"]
    end
    subgraph Control["PHASE 10 · CONTROL PLANE"]
        P10["AgenticOps Control Tower"]
    end
    P5 --> P6
    P9 --> P10
```

## 📐 AI Operations Specification

### Initial operational objects

Phase 1 defines the language of AI operations. Questions to answer:

- what is a workflow
- what is a request
- what is a step
- what is an agent
- what is an LLM call
- what is a prompt
- what is a context object
- what is a tool call
- what is a memory operation
- what is a RAG retrieval
- what is an evaluation
- what is a safety signal
- what is a reliability event
- what is an incident

The initial operational objects are:

| Runtime objects                           | Runtime activity and outcomes         |
| ----------------------------------------- | ------------------------------------- |
| `Workflow` · `Request` · `Step` · `Agent` | `LLM` · `Prompt` · `Context` · `Tool` |
| `Memory` · `RAG` · `Evaluation`           | `Safety` · `Reliability` · `Incident` |

At this stage, the focus is on **definitions, relationships, and terminology**, not Python APIs or exporters.

### Explicitly defined relationships

The diagram below shows only relationships stated in Phase 2. A `Step` may represent or contain the listed runtime activity or other runtime activity.

```mermaid
flowchart TB
    Workflow -->|contains| Request
    Workflow -->|contains| Step
    Workflow -->|contains| Evaluation
    Workflow -->|contains| Incident
    Step -->|may represent or contain| LLM
    Step -->|may represent or contain| Tool
    Step -->|may represent or contain| RAG
    Step -->|may represent or contain| Memory
    Step -->|may represent or contain| Other["Other runtime activity"]
```

### Phase 3 semantic conventions

Canonical AI-native event names and meanings give the ecosystem consistent language for AI runtimes. The roadmap's examples are grouped by subject here for scanning; no additional event names are implied.

| Subject    | Event names                               |
| ---------- | ----------------------------------------- |
| Workflow   | `workflow.started` · `workflow.completed` |
| Request    | `request.started` · `request.completed`   |
| Agent      | `agent.started` · `agent.step`            |
| LLM        | `llm.call`                                |
| Prompt     | `prompt.rendered`                         |
| Context    | `context.injected`                        |
| Tool       | `tool.called`                             |
| Memory     | `memory.read` · `memory.write`            |
| RAG        | `rag.retrieved`                           |
| Evaluation | `evaluation.run` · `judge.scored`         |
| Incident   | `incident.created`                        |

This is where the ecosystem starts to feel analogous to OpenTelemetry semantic conventions, but for AI runtimes.

## 🔭 10-Phase Roadmap

```text
01 ── AI Operations Specification
 │
02 ── Relationships and Execution Structure
 │
03 ── Semantic Conventions
 │
04 ── JSON Schemas
 │
05 ── Python Models
 │
06 ── AgenticLens
 │
07 ── Agentic Chaos
 │
08 ── DeepAgent MCP
 │
09 ── Agentic Sidecar
 │
10 ── AgenticOps Control Tower
```

### Phase 1 — AI Operations Specification

**Goal:** Define the language of AI operations before implementing package-specific behavior.

**Questions:** What is a workflow, request, step, agent, LLM call, prompt, context object, tool call, memory operation, RAG retrieval, evaluation, safety signal, reliability event, or incident?

**Initial operational objects:** `Workflow`, `Request`, `Step`, `Agent`, `LLM`, `Prompt`, `Context`, `Tool`, `Memory`, `RAG`, `Evaluation`, `Safety`, `Reliability`, `Incident`.

**Focus:** Definitions → relationships → terminology. Not Python APIs or exporters.

### Phase 2 — Relationships and Execution Structure

**Goal:** Define how the runtime objects connect.

- `Workflow` contains `Request`, `Step`, `Evaluation`, and `Incident`.
- `Step` may represent or contain `LLM`, `Tool`, `RAG`, `Memory`, or other runtime activity.
- Workflows may have parent-child relationships.
- Execution may be sequential, parallel, or graph-shaped.
- Agent handoffs and delegation should have a portable representation.

Define the execution graph model clearly enough that multiple tools can represent the same run consistently.

### Phase 3 — Semantic Conventions

**Goal:** Define canonical AI-native event names and meanings.

See the grouped event table above for every example in the roadmap. This is the point where the ecosystem starts to feel analogous to OpenTelemetry semantic conventions, but for AI runtimes.

### Phase 4 — JSON Schemas

**Goal:** Make artifacts validatable and portable.

Examples: `workflow.schema.json`, `agent.schema.json`, `evaluation.schema.json`, and future object-specific schemas. The output is a schema-backed artifact model that tools can produce and consume consistently.

### Phase 5 — Python Models

**Goal:** Represent the specification directly in Python.

Examples: `Workflow`, `Step`, `Agent`, `Prompt`, `ToolCall`, and `Evaluation`. These should be implementation models of the specification, not ad hoc package types invented independently in each repo.

### Phase 6 — AgenticLens

**Goal:** Make the specification observable in Python applications.

AgenticLens should populate the AI Operations Specification from real runtime activity, then export it as:

- `workflow.json`
- JSON, CSV, and Markdown
- OpenTelemetry traces, logs, and metrics
- OTLP and future transports

AgenticLens should answer:

- What ran?
- Why did it behave that way?
- What did it cost?
- Did it perform well?

### Phase 7 — Agentic Chaos

**Goal:** Extend the same operational model with resilience and failure evidence.

Agentic Chaos should not invent a parallel model. It should extend the same workflow artifact with chaos and degradation evidence.

Agentic Chaos should answer:

- What breaks under stress?
- How badly does it break?
- Did recovery work?

### Phase 8 — DeepAgent MCP

**Goal:** Expose the same artifact and model through one MCP-native interface.

The MCP server should read and operate on the shared operational contract:

```text
workflow.json
    ↓
analyze()
recommend()
compare()
report()
```

This keeps the MCP layer thin, portable, and aligned with the rest of the ecosystem.

### Phase 9 — Agentic Sidecar

Sidecar **0.8.0** builds on implemented 0.7 live status,
immutable audit records and local Control Room controls. v0.8 adds native
LangGraph/AutoGen/CrewAI/OpenAI Agents/Google ADK tool boundaries, real MCP
transport/gateway validation and versioned native decision correlation.
Lens 0.7.1 reads correlated decisions and verifies native journal chains;
Chaos 0.5.3 recovery proposals retain fault IDs. Tower 0.5.2 keeps governance
outcomes separate from deployment health; MCP server 0.3.5 retains discovery
and transport ownership. Live-provider smoke remains pending credentials.

Shared & Exclusive context/intent and guardrails are implemented at the v0.8
configuration/delivery/composition level: context only, guardrails only, or both,
scoped across a system/task or designated agents. Shared restrictions cannot be
weakened by agent-specific rules. Context transport is explicit and host-owned;
in-process wrappers are not isolation. v0.9 validates privacy, authority and
lifecycle behavior; v1.0 stabilizes schemas. Semantica export remains conditional
on upstream API validation. AIOS records the native correlation convention as a
non-normative draft, not stable conformance.
See the [canonical roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/ROADMAP.md).

**Goal:** Add pre-action supervision and decision governance against the same operational model.

Agentic Sidecar should answer:

- Is the next action aligned with user intent?
- Is the action policy-compliant?
- Does the action require escalation, replanning, or blocking?

### Phase 10 — AgenticOps Control Tower

v0.1–v0.5 are released: optional SQLite registry persistence, reader/writer
authorization, HTTP and offline CLI inventory, shared health and capability
coverage summaries, agent filters, the read-only console, controlled desired
configuration with independent approval and audit, and pushed Lens, Evals,
Sidecar and Chaos evidence shown as fresh/stale/missing posture.

**Goal:** Build an AI-native operations command center and unified control plane
for autonomous agents: live evidence, investigation through MCP and an operations
copilot, human approvals, automated runbooks and verified recovery.

The first approved incident-to-recovery staging scenario ships with the local MCP
investigation connector in Tower 0.6.0 (Phase 6 and 6A combined). The supported
runtime is a deterministic dependency fixture; live incident views follow in
v0.8 and reusable production runbooks in v0.9. Tower coordinates them while Lens,
Evals, Sidecar and Chaos retain their engines.

AgenticOps Control Tower should not replace Lens, Chaos, Sidecar, or MCP. It should centralize:

- Agent inventory
- Capability discovery
- Health and status rollups
- Centralized configuration
- Multi-agent operational workflows

It should answer:

- What is deployed?
- Where is it running?
- Which capabilities and versions are present?
- What is unhealthy?
- What should operators manage from one place?

## 📦 Package Roles

| Package                    | Role                                            |
| -------------------------- | ----------------------------------------------- |
| `ai-operations-spec`       | Defines the standard.                           |
| `agenticlens`              | Observes and evaluates the standard.            |
| `agentic-chaos`            | Tests and stress-validates the standard.        |
| `agentic-sidecar`          | Governs decisions against the standard.         |
| `deep-agentic-core-mcp`    | Connects the standard through MCP.              |
| `agenticops-control-tower` | Operates the ecosystem through a control plane. |

The ecosystem should stay cleanly separated:

- `ai-operations-spec` defines the standard.
- `agenticlens` instruments and exports the standard.
- `agentic-chaos` extends the standard with resilience evidence.
- `deep-agentic-core-mcp` exposes the standard through MCP.

The specification stays above any one package, making ecosystem adoption easier for third parties that want to implement the contract without depending on the Python packages directly.

## 📋 Specification Milestones

The AI Operations Specification itself should evolve in these milestones. The sequence below describes milestone scope; it does not imply completion status.

```mermaid
flowchart TB
    V01["v0.1<br/>Core concepts"] --> V02["v0.2<br/>Relationships"]
    V02 --> V03["v0.3<br/>Semantic conventions"]
    V03 --> V04["v0.4<br/>JSON Schema support"]
    V04 --> V05["v0.5<br/>Versioning and compatibility rules"]
    V05 --> V10["v1.0<br/>Stable public specification"]
```

<details>
<summary>Milestone scope</summary>

| Milestone | Exact scope                                                                                                                                                    |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **v0.1**  | Core concepts: `Workflow`, `Request`, `Step`, `Agent`, `LLM`, `Prompt`, `Tool`, `Context`, `RAG`, `Memory`, `Evaluation`, `Safety`, `Reliability`, `Incident`. |
| **v0.2**  | Relationships: workflow-to-step structure, parent-child relationships, execution graph representation.                                                         |
| **v0.3**  | Semantic conventions: `workflow.started`, `llm.call`, `tool.call`, related canonical event names and lifecycle meanings.                                       |
| **v0.4**  | JSON Schema support.                                                                                                                                           |
| **v0.5**  | Versioning and compatibility rules.                                                                                                                            |
| **v1.0**  | Stable public specification.                                                                                                                                   |

</details>

## 🚧 Current Implementation Priorities

The following items are the current implementation priorities, grouped by the roadmap's urgency labels. Items remain in their source categories.

### 🔴 Implement Now

**`deep-agentic-core-mcp`** — _(sessions, rich diagnostics, tool annotations,
prompt registry, and `core.verify` in `0.2.0`; optional authenticated HTTP,
DynamoDB signup/key lifecycle, Redis user-scoped state, and Sidecar discovery
in `0.3.0`; Phase 3 completed in `0.3.3`)_

Local stdio remains supported. Hosted access is available at
`https://mcp.deepagentlabs.io/mcp`, with signup at `https://mcp.deepagentlabs.io`.
Version-tag releases publish to PyPI before deploying the same source to AWS;
ordinary main-branch pushes run checks without deploying.

- ~~Provenance verification on `lens.analyze_workflow`'s response shape~~ ✅ `0.3.3`.
- ~~Multi-version AIOS schema support + conformance-style reporting~~ ✅ `0.3.3` (`spec_version` routing and rule-cited reports over the `ai-operations-spec` `0.5.1` catalogs).
- Unified workflows: joined observability + chaos, incident/readiness reporting (Phase 4).

**`agenticlens`** — _(evidence/provenance objects, next-best-analysis guidance, OpenTelemetry export, import-layer enforcement, and AIOS conformance CLI shipped in `0.4.0`; v0.3 evaluation evidence and v0.4 experiments and statistical comparison shipped in `0.6.0`; step provenance on every default recommendation in `0.6.1`; v0.5 advanced evaluation and diagnosis shipped in `0.7.0`)_

- Built-in provider clients for LLM-judge calls.
- ~~v0.5 advanced evaluation and diagnosis: failure taxonomy, faulty-step attribution, judge cost recording~~ ✅ `0.7.0`. Next: v0.6 test-suite and dataset management.
- ~~Judge calibration reports and statistical confidence intervals~~ ✅ `0.5.0` (agreement intervals); threshold tuning ✅ `0.6.0`.
- ~~Versioned evaluation datasets (summary, split, sample export)~~ ✅ (`agenticlens dataset`); dataset lifecycle management (immutable snapshots, approvals) remains planned under v0.6.
- ~~Experiment/variant manifests and statistical comparison~~ ✅ `0.6.0` (pass@k/pass^k, intervals, significance tests, heatmaps, HTML/CSV).

**`agentic-chaos`**

- ~~v0.6 pytest plugin and assertions~~ ✅ `0.6.0` (`pytest --chaos`, seven contracts, CLI contract gating).
- Structured experiment traces/reports (hypothesis, injection point, fault, observed behavior, recovery outcome, verdict, provenance).
- Synthetic test scenarios (prebuilt known-bad agent behaviors).
- v0.7 fault cascades, adaptive intensity and response poisoning.

**`ai-operations-spec`**

- Provenance/evidence concepts in the spec.
- Conformance test suite for producers.
- Naming conventions document.

**Cross-cutting (done)**

- `AGENTS.md` in each repo ✅
- `CI.md` pre-push quality guide in each repo ✅

### 🟡 Implement Next

**`agenticlens`**

- ~~Investigation-style narratives on recommendations~~ ✅ `0.7.0` (`agenticlens explain`).
- ~~Remaining CLI subcommands (`trace show`, `report explain`)~~ ✅ `0.7.0` (`trace show`, `trace timeline`, `explain`, `diagnose`).
- v0.6 test-suite and dataset management: trace-to-test-case conversion, immutable approved suites, PII masking.
- ~~Analysis guardrails (budget limits, stagnation detection)~~ ✅ `0.7.0` (`AnalysisBudget`, `AnalysisGuard`).
- ~~Structured judge verdict fields (agree/partially-agree/disagree, confidence score, factual-grounding breakdown)~~ ✅ `0.6.0`.

**`agentic-chaos`**

- Resilience benchmark fixtures/datasets.
- Parallel/sharded test execution.

**`ai-operations-spec`**

- Migration guides between spec versions.
- Hosted docs site.
- Report/investigation artifact schemas.

**`deep-agentic-core-mcp`**

- Guided onboarding wizard.
- Saved artifact browsing through MCP resources.
- Explainable report recall and session history.

### ⚪ Defer

- `agenticlens` full interactive REPL/shell.
- `agentic-chaos` local chaos-lab stack (Docker Compose/kind).
- `deep-agentic-core-mcp` fleet/process registry.
- `deep-agentic-core-mcp` full gateway/multi-surface architecture.
- Conversational long-term memory in `agenticlens` or `agentic-chaos`.

## 🧩 Recommended Build Order

This is the roadmap's recommended order; shipped annotations and the named frontier are retained as stated.

| Order | Work                                                                                                             | Roadmap status                            |
| ----: | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
|     1 | `deep-agentic-core-mcp` — sessions, diagnostics, tool metadata, prompts, verification                            | ~~✅ shipped in `0.2.0`~~                 |
|     2 | `agenticlens` — provenance/evidence, next-step recommendations, OTel, layer enforcement, conformance CLI         | ~~✅ shipped in `0.4.0`~~                 |
|     3 | `agentic-chaos` — structured reports/traces, synthetic scenarios                                                 | **current frontier**                      |
|     4 | `ai-operations-spec` — provenance/evidence/report semantics, naming rules, conformance requirements and fixtures | No status stated in this build-order list |

### Current frontier

> **Agentic Chaos** — structured experiment traces/reports (hypothesis, injection point, fault, observed behavior, recovery outcome, verdict, provenance) and synthetic test scenarios (prebuilt known-bad agent behaviors).

## 🌐 North Star

The long-term goal is not just a Python toolkit. It is an **open operational standard for AI systems** with a shared object model, shared semantic conventions, shared schemas, shared examples, additive extensions, and multiple interoperable implementations.

```mermaid
flowchart TB
    Standard["Open operational standard for AI systems"]
    Standard --> ObjectModel["Shared object model"]
    Standard --> Semantics["Shared semantic conventions"]
    Standard --> Schemas["Shared schemas"]
    Standard --> Examples["Shared examples"]
    Standard --> Extensions["Additive extensions"]
    Standard --> Implementations["Multiple interoperable implementations"]
```

### Control Tower evidence alignment

Control Tower owns fleet operations; Lens owns observability; Evals owns scoring
and release gates; Sidecar supervises decisions; Chaos runs resilience
experiments; AIOS defines draft shared semantics. Tower provides local native
artifact readers and explicit deployment/evidence attribution. Since v0.5 it
stores pushed evidence and shows posture in the API, CLI and console. Pull
collection from producer services remains planned; fleet health remains
separate from producer outcomes. No stable AIOS conformance is claimed.

## Operational safety guarantees (planned)

Added 2026-10-11. Local blocking/stopping, hosted MCP key revocation, tracing,
fault injection and evaluation checks exist in parts. The following integrated
guarantees remain planned; package roadmaps contain their acceptance criteria.

| Guarantee | Implementation owner and dependencies |
| --- | --- |
| Emergency brake | Sidecar owns stop, dispatch blocking and task-access revocation; MCP/credential issuers execute revocation; Tower coordinates operators |
| Independent policy enforcement | Sidecar owns independent policy enforcement; MCP enforces its access boundary; protected tools reachable only through an enforcing boundary |
| Verifiable execution evidence | Lens AIOS-format capture, offline evidence replay and integrity verification; Sidecar/MCP policy/action correlation; Tower presentation |
| Adversarial containment validation | Chaos attacks/failures; Evals containment scoring/gates; Sidecar/MCP enforcing targets |

Shared command, authority and evidence semantics must be coordinated in AI
Operations Specification before claiming interoperable contracts. Stop must block
further dispatch independently of the LLM; in-flight effects and unsupported
credential revocation must remain visible. Evidence must distinguish verdicts
from actual execution and verification from ordinary schema validation.
Containment requires reproducible zero-violation tests and negative controls,
not only successful recovery or safe-sounding answers.

See the [Sidecar](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/ROADMAP.md),
[MCP](https://github.com/DeepAgentLabs/mcp-server/blob/main/ROADMAP.md),
[Tower](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/ROADMAP.md),
[Lens](https://github.com/DeepAgentLabs/agenticlens/blob/main/agenticlens-roadmap.md),
[Chaos](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/ROADMAP.md) and
[Evals](https://github.com/DeepAgentLabs/agentic-evals/blob/main/ROADMAP.md) roadmaps.


## Tower v0.4 controlled configuration

[Control Tower v0.4.0](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.4.0)
adds Tower-owned desired configuration, bounded action previews, independent
approval/denial, expiry, revocation, revision checks and atomic one-use execution.
HTTP/CLI expose the same durable configuration and audit model. Runtime-owned
settings remain mirrored or unsupported; desired-state changes do not claim a
remote runtime update. The console remains read-only. Lens 0.5, Evals 0.7,
Sidecar 0.7, Chaos 0.4 and MCP 0.3.1 remain optional integrations; no writable
sibling adapter or task stop/revoke transport is shipped.

## Agentic Chaos v0.5

[Agentic Chaos v0.5.0](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v0.5.0)
adds sync/async streaming cuts, bounded hangs and delivery delays, reversible
patches for explicit OpenAI/Anthropic/Google Gen AI client instances, seeded fault
probability, TOML profiles, and authentication/context-length simulations.
Provider SDKs and ecosystem packages remain optional. Native report fields are
unchanged: Lens consumes the events, MCP discovers new fault names dynamically,
and Tower reads native chaos evidence separately from fleet health.

The [v0.5 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/v0.5.md)
documents API coverage and compatibility tests. Structured experiment reports
remain unfinished v0.2.x work (the AIOS run export shipped in `0.5.1`, below).
Safety rails subsequently ship in `0.5.2` (see below); `0.5.0` itself does not
claim those capabilities.

## MCP 0.3.2 and Chaos 0.5 compatibility

[MCP v0.3.2](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.2)
adds real integration tests and an offline streaming experiment target for
Chaos v0.5's dynamic fault catalog and native experiment events. Local stdio
runs trusted workspace scripts; hosted HTTP rejects chaos execution. The
release keeps Chaos optional and does not expose profile/provider configuration
through a new MCP request schema. See the
[MCP user guide](https://github.com/DeepAgentLabs/mcp-server/blob/main/docs/user-guide.md#chaos-v05-streaming-with-mcp-032).

## Phase 3 completion: MCP 0.3.3 with Lens 0.6.1, Chaos 0.5.1 and AIOS 0.5.1

[MCP v0.3.3](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.3)
completes MCP Phase 3. Three patch releases supply what it composes:

- [AgenticLens 0.6.1](https://github.com/DeepAgentLabs/agenticlens/releases/tag/v0.6.1):
  every default recommendation, including model swaps and chaos impact, names
  its step and cites evidence for it. In MCP, `lens.analyze_workflow` adds a
  provenance block (artifact digest, step, spans) to each finding, with an
  explicit `resolved` status that is false whenever the step or a span is absent
  from the caller's artifact.
- [Agentic Chaos 0.5.1](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v0.5.1):
  `to_aios_run()` and `--save-aios` export a chaos report as an AIOS
  v0.4-draft Run. In MCP, `chaos.run_experiment` attaches that export and
  reports its validation result separately (`aios_export.aligned`),
  `chaos.export_aios_run` converts saved reports, and a script allow/deny glob
  policy narrows which local scripts can run.
- [AI Operations Specification 0.5.1](https://github.com/DeepAgentLabs/ai-operations-spec/releases/tag/v0.5.1):
  machine-readable conformance rule IDs and the v0.5 compatibility catalog. In
  MCP, `spec.validate_artifact` routes by `spec_version` and reports which
  `AIOS-0.4-*` and `AIOS-0.5-*` rules pass or fail, separately from server
  presentation.

Each sibling remains optional for MCP. An older sibling degrades rather than
failing. With an older Lens, findings without a step report `resolved: false`.
With Chaos 0.5.0, the export reports `available: false`. With an older spec
checkout, the conformance report has no rule catalog. These are
draft-alignment claims, not stable AIOS conformance; Lens integrity
verification remains planned. Tower 0.6.0 now supplies thin Sidecar stop and
native MCP issuer revocation adapters with explicit containment limits.

## Tower v0.5 ecosystem evidence posture

[Control Tower v0.5.0](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.5.0)
completes its ecosystem surface phase. Producers or pipelines push native Lens
runs, Evals reports and gates, Sidecar decisions and Chaos reports with explicit
deployment attribution. Tower stores the validated projection idempotently and
reports, per deployment and producer, whether evidence is fresh, stale or
missing, with counts of native outcomes, through Python, HTTP, CLI, offline
snapshots and the read-only console.

Lens runs now expose trace, timing, tool and failed-span correlation for later
incident investigation. Tower never recomputes an evaluation, decision or
resilience verdict, and producer outcomes never change reported health. Optional
floors are Lens 0.6, Evals 0.7, Sidecar 0.7, Chaos 0.5 and MCP 0.3.4; none is
required. The Lens, Evals, Sidecar and Chaos readers are checked against their
published packages; MCP is a declared floor only. Pull collection,
AIOS mapping and journal integrity verification remain planned. The MCP
connector and investigation prompt now ship with approved staging recovery
in Tower 0.6.0; see the combined milestone below.

## AgenticLens 0.7.0: advanced evaluation and diagnosis

[AgenticLens 0.7.0](https://github.com/DeepAgentLabs/agenticlens/releases/tag/v0.7.0)
delivers Lens roadmap milestone v0.5. `agenticlens diagnose` explains a failed
run from its trace. It applies a versioned failure taxonomy and deterministic
rules whose diagnoses carry confidence and supporting spans. It attributes the
failure to a step and an agent (discounting recovered failures and downstream
consequences), rebuilds the incident timeline, flags anomalies against healthy
baseline runs, and writes an investigation narrative. Attribution accuracy is
measured on controlled failures. On the bundled 40-case synthetic corpus,
attribution finds the faulty step 40/40 times; that corpus is not independent
evidence. Evaluation gains trace-aware evaluators (trajectory, handoff, loop,
retrieval groundedness and citations, safety in tool arguments), judge cost
and prompt-version recording, and reports that keep deterministic and
model-based scores apart and show where evaluators disagree. AIOS conformance
now cites rule IDs from the spec's catalog.

Sibling releases in the same window:

- [Agentic Chaos 0.5.3](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v0.5.3):
  `mark_span()` tags a Lens trace span with the injected fault, so chaos runs
  become ground truth for Lens attribution accuracy.
- [MCP 0.3.5](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.5):
  `lens.diagnose_run` and `lens.score_analysis`; hosted images pin Lens 0.7.0.
- [Control Tower 0.5.1](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.5.1):
  reads Lens diagnosis reports as native evidence and tallies attribution
  outcomes and faulty agents in posture, without re-diagnosing.

## Agentic Chaos 0.5.2 safety rails

The v0.5.x safety milestone ships in
[Agentic Chaos 0.5.2](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v0.5.2).
Circuit breakers bound explicitly recorded cost, rolling exception rate,
cooperative duration, and admitted injection count. Dry-run records selected
faults while target calls and streams execute normally. Abort prevents later
instrumented dispatches and reports already-running work separately; direct
uninstrumented calls remain outside that boundary.

The [safety guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/safety.md)
defines accounting and containment limits. Native safety fields are additive;
AIOS exports retain them in the producer extension and mark aborted runs
`cancelled`, without treating previews as observed failure evidence. Current
Lens, Tower, MCP saved-report export, and AIOS readers are compatibility-tested;
no sibling patch release is required. MCP's run tool does not yet expose the new
safety execution flags. Pytest integration/assertions (v0.6) are next, alongside
the remaining structured ExperimentReport and synthetic-scenario backlog.

## Tower 0.6.0 combined Phase 6/6A release

Tower 0.6.0 and MCP 0.3.6 deliver local authenticated investigation tools and
cited evidence assembly, exact-preview human approval, durable at-most-one
execution claims, and verified staging recovery with failure escalation.
The native-producer walkthrough uses Lens 0.7.1 and Evals 0.7.1. Sidecar 0.8.0
retains dispatch stop/restart and revoker enforcement; Chaos 0.5.3 retains fault
injection and native reports. `ai-operations-spec` catalog release 0.5.1 retains AIOS v0.4-draft schemas;
Tower-local incident and approval contracts do not become normative schemas. Producer dependencies stay
optional and unchanged. Documentation-only alignment needs no sibling releases.

Supported scope: deterministic local SQLite staging dependency fixture, explicit
detection, independent approval, fresh same-run Lens/Evals plus probe checks,
manual reconciliation of interrupted/partial execution, and thin emergency
braking adapters. Hosted MCP Tower credentials, production runtime remediation,
bulk operations and incident console views remain later work.

[Operator walkthrough](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/incident-recovery.md) ·
[MCP setup](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/mcp-connector.md).

## Agentic Chaos 0.6.0 pytest plugin and contracts

[Agentic Chaos 0.6.0](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v0.6.0)
makes chaos part of an ordinary test run. A `@pytest.mark.chaos` test runs under
faults when pytest is started with `--chaos`; without the flag it runs normally.
Seven contracts are pass/fail checks over the run's native report:
`CompletesWithin`, `NoUnhandledError`, `MaxRetries`, `RecoveredAfterFailure`,
`MaxCostImpact`, `NoRetryStorm` (retries across the whole topology) and
`FullTopologyTraversal` (every baseline node still ran). Contracts fail closed:
a check the report cannot support, including one on a report written before 0.6,
is `inconclusive`, and inconclusive never passes. The same contracts gate
`agentic-chaos chaos run --contract ...` and `contracts check` on saved reports.

Reports gain an additive call log and the escaped `unhandled_error`. Lens and
Tower readers ignore them, and the AIOS export carries only call counts and the
error in the producer extension, so no core AIOS object changes. Contract
verdicts are Chaos-native per-run checks; Evals still owns scoring and release
gates. The [v0.6 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/v0.6.md)
covers the marker, the fixture, async tests and the exact retry and visit definitions.

Sibling releases in the same window:

- [Agentic Sidecar 0.8.1](https://github.com/DeepAgentLabs/agentic-sidecar/releases/tag/v0.8.1):
  the optional `agentic-chaos` extra admits 0.6; no runtime change.
- [MCP 0.3.7](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.7):
  hosted images pin Chaos 0.6.0; MCP tools are unchanged.

Lens, Evals, Tower and AIOS spec changes are documentation-only.

