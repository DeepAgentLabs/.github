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
| [**AgenticLens**](https://github.com/DeepAgentLabs/agenticlens) (`agenticlens`) | Observability, evaluation, and operational intelligence for production AI systems — what ran, why, at what cost, and how to improve it, with failure diagnosis and faulty-step attribution (0.7.0). |
| [**Agentic Evals**](https://github.com/DeepAgentLabs/agentic-evals) (`agentic-evals`) | A standalone, framework-agnostic scoring and evaluation engine for LLM and agent outputs. |
| [**Agentic Sidecar**](https://github.com/DeepAgentLabs/agentic-sidecar) (`agentic-sidecar`) | A real-time supervision layer that checks an agent's plans and actions against intent, policy, risk, and budget before they execute. |
| [**Agentic Chaos**](https://github.com/DeepAgentLabs/agentic-chaos) (`agentic-chaos`) | A fault-injection toolkit that deliberately breaks agent workflows to measure resilience and recovery, with circuit breakers and dry-run previews (0.5.2), AgenticLens diagnosis span markers (0.5.3), and a pytest plugin with fail-closed resilience contracts (0.6.0). |
| [**MCP Server**](https://github.com/DeepAgentLabs/mcp-server) (`deep-agentic-core-mcp`) | A single MCP interface that exposes workflow inspection, evaluation, and chaos/resilience tooling to AI clients. |
| [**AgenticOps Control Tower**](https://github.com/DeepAgentLabs/agenticops-control-tower) | An operations control plane for inventory, evidence posture, cited MCP investigation and approved verified staging recovery (0.6.0). |

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

## Evals 0.7.2: published native report contract

The Evals v0.7.x milestone is complete in 0.7.2: packaged Draft 2020-12
JSON Schemas, offline report/gate accessors, frozen 0.7.1 compatibility checks
and validated examples. Contract 1.x changes are additive only. Tower and Lens
retain their native reader shapes; no sibling dependency floor increases are
needed. Chaos resilience, Sidecar supervision and AIOS conformance remain
separate concerns. See the [contract and sibling matrix](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/report-contract.md).
Evals v0.8 (suite/pack/gate CLI) is next; AIOS evaluation export remains v0.10.

## Native Evals contract adoption

MCP 0.3.8 exposes offline `evals.validate_artifact` and validates native reports
in Lens analysis/audit/SLO tools. Tower 0.6.1 validates full Evals reports and
gates before evidence projection; malformed evidence is unavailable. Bundled
upstream 0.7.2 schemas keep both consumers independent of runtime sibling
installations. This is native structural validation, not AIOS conformance.
