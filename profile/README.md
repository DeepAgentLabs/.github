# DeepAgentLabs

Open-source tooling for observing and stress-testing LLM-powered applications
and agentic workflows.

## Projects

### [agenticlens](https://github.com/DeepAgentLabs/agenticlens)

A lightweight, local profiler for LLM applications — like `cProfile` for
agentic workflows. Explicit `profile()`/`step()` instrumentation, no hosted
dashboard, no account, no data egress. Tracks tokens, cost, and latency per
step, and turns that into rule-based optimization recommendations (repeated
prompts, excessive RAG chunks, long conversation history, duplicate tool
calls, and more).

```bash
pip install agenticlens
```

### [agentic-chaos](https://github.com/DeepAgentLabs/agentic-chaos)

A standalone fault-injection toolkit for LLM calls and agentic workflows.
Deliberately breaks your app — hung completions, provider rate-limit storms,
silently corrupted output — so you can find out what actually happens when
it does. No required dependency on `agenticlens` or anything else; an
optional integration merges chaos events into an `agenticlens` report when
you want cost/latency and resilience findings together.

```bash
pip install agentic-chaos
```

## Philosophy

Both projects are local-first and explicitly instrumented rather than
relying on SDK monkey-patching or a hosted backend — and they're independent
of each other by default, composing through a shared, documented JSON format
rather than a hard code dependency.
