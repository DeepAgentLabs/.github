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
| [**Agentic Chaos**](https://github.com/DeepAgentLabs/agentic-chaos) (`agentic-chaos`) | A fault-injection toolkit that deliberately breaks agent workflows to measure resilience and recovery, with circuit breakers and dry-run previews (0.5.2) and AgenticLens diagnosis span markers (0.5.3). |
| [**MCP Server**](https://github.com/DeepAgentLabs/mcp-server) (`deep-agentic-core-mcp`) | A single MCP interface that exposes workflow inspection, evaluation, and chaos/resilience tooling to AI clients. |
| [**AgenticOps Control Tower**](https://github.com/DeepAgentLabs/agenticops-control-tower) | A unified control plane for agent inventory, health, capability discovery, fleet-wide configuration, and ecosystem evidence posture. |

See the [roadmap](ROADMAP.md) for how these pieces fit together and what's being built next.

## Principles

- **Specification-first** — the contract comes before SDK ergonomics, dashboards, or integrations.
- **Modular** — each project is independently installable and useful on its own.
- **Runtime and framework agnostic** — works alongside LangGraph, CrewAI, the OpenAI Agents SDK, AutoGen, LlamaIndex, and custom agent stacks.
- **Open source** — released under permissive licenses; see each repository for its license.

## Get involved

Found a bug or have an idea? Open an issue or discussion on the relevant repository above. Most projects also publish to PyPI — search for the package name shown next to each project.
