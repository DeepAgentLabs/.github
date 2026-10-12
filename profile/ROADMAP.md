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

Latest Sidecar release: **[0.7.0](https://github.com/DeepAgentLabs/agentic-sidecar/releases/tag/v0.7.0) — 2026-10-12**, available on PyPI. Deterministic policy/risk and
bound intent constraints are joined by governed suspension for all outcomes,
local ID-correlated approvals, full-plan context, optional live OpenAI/Anthropic
providers and validated shared budget accounting. Four deterministic fixtures
cover refund/environment/export/delegation with guardian off/on and clean controls.
Authenticated live-provider smoke evidence remains pending by request. Runtime-connected
status, immutable durable audit lifecycle and authenticated local Control Room are
included in v0.7.0, with task-scoped stop, async cancellation requests, explicit restart
and harness-supplied access-revocation acknowledgements.

The [v0.7.0 Sidecar roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/v0.7.0/ROADMAP.md)
prioritizes **0.8 adapters/integrations → 0.9 evaluation/authority → 1.0 stable schemas**.
Tower retains fleet/operator aggregation. Published
[Tower `0.3.1`](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.3.1)
adds native decision IDs, trigger details and causal links. Published
[MCP `0.3.1`](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.3.1)
detects installed v0.7 APIs separately from a live task connection; runtime
operator bridging remains planned. Both patches released on 2026-10-12.
Sidecar owns action supervision and its approval boundary.

**Goal:** Add pre-action supervision and decision governance against the same operational model.

Agentic Sidecar should answer:

- Is the next action aligned with user intent?
- Is the action policy-compliant?
- Does the action require escalation, replanning, or blocking?

### Phase 10 — AgenticOps Control Tower

v0.1/v0.2 are implemented: optional SQLite registry persistence, reader/writer
authorization, HTTP and offline CLI inventory, shared health and capability
coverage summaries, and agent filters. The read-only console is published in [v0.3.1](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v0.3.1), with fleet health, inventory, capability coverage, minimum-version checks and evidence readiness.

**Goal:** Build an AI-native operations command center and unified control plane
for autonomous agents: live evidence, investigation through MCP and an operations
copilot, human approvals, automated runbooks and verified recovery.

The first approved incident-to-recovery staging scenario is planned for v0.6.x;
live detection/incident views follow in v0.8 and reusable runbooks in v0.9.
These workflows are not implemented yet. Tower coordinates them while Lens,
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
in `0.3.0`; Sidecar v0.7 compatibility in `0.3.1`)_

Local stdio remains supported. Hosted access is available at
`https://mcp.deepagentlabs.io/mcp`, with signup at `https://mcp.deepagentlabs.io`.
Version-tag releases publish to PyPI before deploying the same source to AWS;
ordinary main-branch pushes run checks without deploying.

- Provenance verification on `lens.analyze_workflow`'s response shape.
- Multi-version AIOS schema support + conformance-style reporting, blocked on `ai-operations-spec` publishing `v0.4` schema artifacts and follow-on compatibility/versioning rules.
- Unified workflows: joined observability + chaos, incident/readiness reporting (Phase 4).

**`agenticlens`** — _(evidence/provenance objects, next-best-analysis guidance, OpenTelemetry export, import-layer enforcement, and AIOS conformance CLI shipped in `0.4.0`)_

- Judge calibration reports and statistical confidence intervals.
- Evaluation dataset management.
- Built-in provider clients for LLM-judge calls.
- Next release: experiment/variant manifests and statistical comparison.

**`agentic-chaos`**

- Structured experiment traces/reports (hypothesis, injection point, fault, observed behavior, recovery outcome, verdict, provenance).
- Synthetic test scenarios (prebuilt known-bad agent behaviors).

**`ai-operations-spec`**

- Provenance/evidence concepts in the spec.
- Conformance test suite for producers.
- Naming conventions document.

**Cross-cutting (done)**

- `AGENTS.md` in each repo ✅
- `CI.md` pre-push quality guide in each repo ✅

### 🟡 Implement Next

**`agenticlens`**

- Investigation-style narratives on recommendations.
- Remaining CLI subcommands (`trace show`, `report explain` — `inspect` and `compare` already shipped).
- Analysis guardrails (budget limits, stagnation detection).
- Structured judge verdict fields on `LLMJudgeEvaluator` (agree/partially-agree/disagree, confidence score, factual-grounding breakdown).

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
artifact readers and explicit deployment/evidence attribution. Remote collection
and console posture views remain planned (v0.5 partial); fleet health remains
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
