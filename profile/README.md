# DeepAgentLabs

Open-source observability, evaluation, and resilience tooling for agentic AI
applications — from profiling and quality scoring to fault injection and chaos
testing.

## Projects

### [agenticlens](https://github.com/DeepAgentLabs/agenticlens)

[![PyPI](https://img.shields.io/pypi/v/agenticlens.svg)](https://pypi.org/project/agenticlens/)
[![Python](https://img.shields.io/pypi/pyversions/agenticlens.svg)](https://pypi.org/project/agenticlens/)

Full-stack observability, evaluation, and regression toolkit for agentic AI
applications. Workflow profiling, cost/latency/token analysis, RAG
chunk-utility scoring, and multi-format export — all local-first, no hosted
backend required.

**Current:** workflow profiling, cost analysis, RAG chunk-utility scoring,
multi-format export, and agentic-chaos interop.

**Roadmap:** graph-aware tracing, evaluator API with LLM-as-judge scoring,
datasets and trace-to-dataset curation, experiment runner for prompt/model
variant comparison, prompt registry, and CI policy guardrails.

```bash
pip install agenticlens
```

### [agentic-chaos](https://github.com/DeepAgentLabs/agentic-chaos)

[![PyPI](https://img.shields.io/pypi/v/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)
[![Python](https://img.shields.io/pypi/pyversions/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)

A comprehensive fault-injection and resilience testing toolkit for LLM calls
and agentic workflows. Deliberately breaks your app — token timeouts,
rate-limit storms, silent degradation, tool-call failures, memory corruption,
infinite loops — so you find out what actually happens before your users do.
Includes a LangGraph adapter and agent topology tracking out of the box.

**Current (v0.2):** LLM-level faults (token timeout, rate-limit storm, silent
degradation) + agent-level faults (tool-call failure, memory corruption,
infinite loop) + LangGraph adapter + topology tracking + CLI.

**Roadmap:** fidelity judges, prompt/model drift detection, streaming faults,
pytest plugin, fault cascades, resilience scoring, and a shared ChaosHub
experiment registry.

```bash
pip install agentic-chaos
```

### [deep-agentic-core-mcp](https://github.com/DeepAgentLabs/mcp-server)

[![PyPI](https://img.shields.io/pypi/v/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)

A unified MCP (Model Context Protocol) server that exposes the full
DeepAgentLabs ecosystem — workflow observability from AgenticLens and
resilience testing from agentic-chaos — through a single MCP interface. One
server, one registry identity, one connection for MCP-compatible hosts.

**Status:** Foundation phase — project structure, registry metadata, and
initial tool surface design.

```bash
pip install deep-agentic-core-mcp
```

## How They Fit Together

```
┌─────────────────────────────────────────────────┐
│            deep-agentic-core-mcp                │
│         (unified MCP server layer)              │
└────────────────┬────────────────┬───────────────┘
                 │                │
     ┌───────────▼───┐    ┌───────▼─────────┐
     │  agenticlens  │    │  agentic-chaos  │
     │ observability │    │   resilience    │
     │  & evaluation │    │   & testing     │
     └───────────────┘    └─────────────────┘
```

Each package is fully standalone — `pip install` any one of them and it works
independently. They compose through a shared, documented `workflow.json` format
rather than hard code dependencies. The MCP server is a thin orchestration layer
that delegates to both.

## Philosophy

- **Local-first:** runs on your machine or in CI — no hosted backend, no
  account, no data egress.
- **Package-first:** every feature is usable through Python and the CLI.
- **Explicitly instrumented:** no SDK monkey-patching or hidden side-effects.
- **Framework-agnostic:** integrations matter, but the core data model stays
  independent.
- **Composable by default:** independent packages, shared JSON contracts.
