# DeepAgentLabs Roadmap

## Direction

DeepAgentLabs should be built **specification-first**.

The AI Operations Specification should come before SDK ergonomics, package
features, dashboards, or integrations. That is the pattern used by the
strongest ecosystems:

- OpenTelemetry defined the telemetry model and semantic conventions first
- Kubernetes defined the API objects first
- OpenAPI defined the interface specification first

DeepAgentLabs should follow the same shape:

```text
AI Operations Specification
        │
        ├── Core Concepts
        ├── Semantic Conventions
        ├── JSON Schemas
        ├── Versioning
        ├── Examples
        └── Extension Model
                 │
                 ▼
     Reference Implementations
        ├── AgenticLens
        ├── Agentic Chaos
        └── DeepAgent MCP
```

The specification is the foundation. The packages are reference
implementations of that foundation.

## Ecosystem Build Order

The ecosystem should be developed in this order:

### Phase 1 — AI Operations Specification

Goal: define the language of AI operations before implementing package-specific
behavior.

Questions to answer:

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

Initial operational objects:

- `Workflow`
- `Request`
- `Step`
- `Agent`
- `LLM`
- `Prompt`
- `Context`
- `Tool`
- `Memory`
- `RAG`
- `Evaluation`
- `Safety`
- `Reliability`
- `Incident`

At this stage, the focus is on definitions, relationships, and terminology,
not on Python APIs or exporters.

### Phase 2 — Relationships and Execution Structure

Goal: define how the runtime objects connect.

Examples:

- `Workflow` contains `Request`, `Step`, `Evaluation`, and `Incident`
- `Step` may represent or contain `LLM`, `Tool`, `RAG`, `Memory`, or other
  runtime activity
- workflows may have parent-child relationships
- execution may be sequential, parallel, or graph-shaped
- agent handoffs and delegation should have a portable representation

This phase should define the execution graph model clearly enough that multiple
tools can represent the same run consistently.

### Phase 3 — Semantic Conventions

Goal: define canonical AI-native event names and meanings.

Examples:

- `workflow.started`
- `workflow.completed`
- `request.started`
- `request.completed`
- `agent.started`
- `agent.step`
- `llm.call`
- `prompt.rendered`
- `context.injected`
- `tool.called`
- `memory.read`
- `memory.write`
- `rag.retrieved`
- `evaluation.run`
- `judge.scored`
- `incident.created`

This is the point where the ecosystem starts to feel analogous to
OpenTelemetry semantic conventions, but for AI runtimes.

### Phase 4 — JSON Schemas

Goal: make artifacts validatable and portable.

Examples:

- `workflow.schema.json`
- `agent.schema.json`
- `evaluation.schema.json`
- future object-specific schemas

The output of this phase is a schema-backed artifact model that tools can
produce and consume consistently.

### Phase 5 — Python Models

Goal: represent the specification directly in Python.

Examples:

- `Workflow`
- `Step`
- `Agent`
- `Prompt`
- `ToolCall`
- `Evaluation`

These should be implementation models of the specification, not ad hoc package
types invented independently in each repo.

### Phase 6 — AgenticLens

Goal: make the specification observable in Python applications.

AgenticLens should populate the AI Operations Specification from real runtime
activity, then export it as:

- `workflow.json`
- JSON
- CSV
- Markdown
- OpenTelemetry traces, logs, and metrics
- OTLP and future transports

AgenticLens should answer:

- what ran
- why it behaved that way
- what it cost
- whether it performed well

### Phase 7 — Agentic Chaos

Goal: extend the same operational model with resilience and failure evidence.

Agentic Chaos should not invent a parallel model. It should extend the same
workflow artifact with chaos and degradation evidence.

Agentic Chaos should answer:

- what breaks under stress
- how badly it breaks
- whether recovery worked

### Phase 8 — DeepAgent MCP

Goal: expose the same artifact and model through one MCP-native interface.

The MCP server should read and operate on the shared operational contract:

```text
workflow.json
    ↓
analyze()
recommend()
compare()
report()
```

This keeps the MCP layer thin, portable, and aligned with the rest of the
ecosystem.

## Specification Milestones

The AI Operations Specification itself should evolve in clear milestones.

### v0.1

Core concepts:

- `Workflow`
- `Request`
- `Step`
- `Agent`
- `LLM`
- `Prompt`
- `Tool`
- `Context`
- `RAG`
- `Memory`
- `Evaluation`
- `Safety`
- `Reliability`
- `Incident`

### v0.2

Relationships:

- workflow-to-step structure
- parent-child relationships
- execution graph representation

### v0.3

Semantic conventions:

- `workflow.started`
- `llm.call`
- `tool.call`
- related canonical event names and lifecycle meanings

### v0.4

JSON Schema support.

### v0.5

Versioning and compatibility rules.

### v1.0

Stable public specification.

## Package Roles

The ecosystem should stay cleanly separated:

- `ai-operations-spec` defines the standard
- `agenticlens` instruments and exports the standard
- `agentic-chaos` extends the standard with resilience evidence
- `deep-agentic-core-mcp` exposes the standard through MCP

That keeps the specification above any one package and makes ecosystem adoption
easier for third parties who want to implement the contract without depending
on the Python packages directly.

## North Star

The long-term goal is not just a Python toolkit.

It is an **open operational standard for AI systems** with:

- a shared object model
- shared semantic conventions
- shared schemas
- shared examples
- additive extensions
- multiple interoperable implementations
