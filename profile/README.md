# DeepAgentLabs

DeepAgentLabs builds **open operational infrastructure for production AI
systems**.

The ecosystem is organized around a simple architecture:

```text
Operational Model
        |
        v
AI Operations Workflow Specification
        |
        v
Reference Implementations
        |
        +-- AgenticLens
        +-- Agentic Chaos
        +-- deep-agentic-core-mcp
```

The core idea is simple:

- define an open operational model for production AI systems
- express it through a versioned workflow specification
- build practical PyPI packages that implement the model

All three projects are centered on the **AI Operations Workflow Specification**
as the canonical operational model for production AI systems.

## Workflow Specification

At the center of the ecosystem is the **AI Operations Workflow Specification**,
a versioned workflow contract for representing production AI runs,
observability data, evaluation evidence, resilience events, and future
operational metadata.

This turns `workflow.json` into a first-class artifact rather than an internal
implementation detail.

- Spec: [AI Operations Workflow Specification](https://github.com/DeepAgentLabs/agenticlens/blob/main/docs/workflow-schema-spec.md)

## Projects

### [agenticlens](https://github.com/DeepAgentLabs/agenticlens)

[![PyPI](https://img.shields.io/pypi/v/agenticlens.svg)](https://pypi.org/project/agenticlens/)
[![Python](https://img.shields.io/pypi/pyversions/agenticlens.svg)](https://pypi.org/project/agenticlens/)

The flagship reference implementation for observability, evaluation, and
operational intelligence for production AI systems.

AgenticLens observes, evaluates, explains, and recommends:

- workflow profiling
- latency, token, and cost analysis
- RAG and agent workflow inspection
- incident and change-impact analysis
- SLI/SLO-oriented operational reporting
- audit and standards-readiness evidence

```bash
pip install agenticlens
```

### [agentic-chaos](https://github.com/DeepAgentLabs/agentic-chaos)

[![PyPI](https://img.shields.io/pypi/v/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)
[![Python](https://img.shields.io/pypi/pyversions/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)

The resilience testing and failure-validation reference implementation for
production AI systems.

Agentic Chaos injects, validates, tests, and proves resilience:

- LLM fault injection
- agent failure injection
- recovery validation
- deployment and release validation
- conformance-style resilience testing
- drift and degradation evidence

```bash
pip install agentic-chaos
```

### [deep-agentic-core-mcp](https://github.com/DeepAgentLabs/mcp-server)

[![PyPI](https://img.shields.io/pypi/v/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)

The unified MCP-native control surface for the ecosystem.

DeepAgentLabs MCP exposes the shared operational model through one MCP server,
bridging hosts and tooling over the same workflow specification used by the
reference implementations.

```bash
pip install deep-agentic-core-mcp
```

## How They Fit Together

```text
┌──────────────────────────────────────────────────────────────┐
│                  AI Operations Workflow Specification        │
└──────────────────────────────┬───────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
┌────────▼────────┐   ┌────────▼─────────┐   ┌───────▼────────────────┐
│   AgenticLens   │   │  Agentic Chaos   │   │ deep-agentic-core-mcp  │
│ Observe         │   │ Break            │   │ Unified MCP interface  │
│ Evaluate        │   │ Validate         │   │ over the same model    │
│ Explain         │   │ Test             │   └────────────────────────┘
│ Recommend       │   │ Prove resilience │
└─────────────────┘   └──────────────────┘
```

Each package is independently installable and useful on its own. They compose
through the shared workflow specification rather than hard code dependencies.

## Philosophy

- **Architecture-first:** the ecosystem is organized around one shared
  operational model and workflow specification.
- **Package-first:** core capabilities ship as installable Python packages.
- **Local-first:** artifacts work in local development and CI without a hosted
  backend.
- **Framework-agnostic:** the operational model stays broader than any one SDK.
- **Composable by default:** one shared workflow specification, multiple
  reference implementations.
