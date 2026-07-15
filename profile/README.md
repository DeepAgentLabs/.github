# DeepAgentLabs

## An Open AI Operations Ecosystem

DeepAgentLabs builds **open operational infrastructure for production AI
systems**.

## The Three Core Projects

### [agenticlens](https://github.com/DeepAgentLabs/agenticlens)

[![PyPI](https://img.shields.io/pypi/v/agenticlens.svg)](https://pypi.org/project/agenticlens/)
[![Python](https://img.shields.io/pypi/pyversions/agenticlens.svg)](https://pypi.org/project/agenticlens/)

The observability, evaluation, and operational intelligence layer. It tells you
what happened, how well the system performed, where cost, latency, and risk
came from, and whether things are getting better or worse.

```bash
pip install agenticlens
```

### [agentic-chaos](https://github.com/DeepAgentLabs/agentic-chaos)

[![PyPI](https://img.shields.io/pypi/v/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)
[![Python](https://img.shields.io/pypi/pyversions/agentic-chaos.svg)](https://pypi.org/project/agentic-chaos/)

The resilience and failure-validation layer. It deliberately breaks AI
workflows so teams can test reliability, recovery, fault tolerance, and
degraded behavior before production incidents do it for them.

```bash
pip install agentic-chaos
```

### [deep-agentic-core-mcp](https://github.com/DeepAgentLabs/mcp-server)

[![PyPI](https://img.shields.io/pypi/v/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/deep-agentic-core-mcp.svg)](https://pypi.org/project/deep-agentic-core-mcp/)

The unified MCP control surface. It exposes the shared operational model and
the capabilities of both tools through one interface for hosts, agents, and
external systems.

```bash
pip install deep-agentic-core-mcp
```

## The Center of Gravity

At the center of the ecosystem is the **AI Operations Workflow Specification**,
a versioned workflow contract for representing production AI runs,
observability data, evaluation evidence, resilience events, and future
operational metadata.

This turns `workflow.json` into a first-class artifact rather than an internal
implementation detail.

All three projects are centered on the **AI Operations Workflow Specification**
as the canonical operational model for production AI systems.

- Spec: [AI Operations Workflow Specification](https://github.com/DeepAgentLabs/agenticlens/blob/main/docs/workflow-schema-spec.md)

## Summary

The ecosystem serves as an open operational framework for production AI
systems, similar in spirit to OpenTelemetry but purpose-built for AI systems
and agentic workflows. It makes applications observable, testable, and
manageable through a structured, shared data model.

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
