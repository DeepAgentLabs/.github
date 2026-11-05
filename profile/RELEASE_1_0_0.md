# DeepAgentLabs 1.0.0 milestone

2026-11-05 marks the coordinated 1.0.0 milestone across the seven ecosystem
projects. This is a checkpoint in ongoing development; feature delivery and
roadmap validation continue.

| Project | Distribution / release |
| --- | --- |
| AI Operations Specification | [Repository 1.0.0](https://github.com/DeepAgentLabs/ai-operations-spec/releases/tag/v1.0.0) |
| AgenticLens | [PyPI 1.0.0](https://pypi.org/project/agenticlens/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/agenticlens/releases/tag/v1.0.0-ecosystem) |
| Agentic Evals | [PyPI 1.0.0](https://pypi.org/project/agentic-evals/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v1.0.0) |
| Agentic Chaos | [PyPI 1.0.0](https://pypi.org/project/agentic-chaos/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/agentic-chaos/releases/tag/v1.0.0) |
| Agentic Sidecar | [PyPI 1.0.0](https://pypi.org/project/agentic-sidecar/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/agentic-sidecar/releases/tag/v1.0.0) |
| AgenticOps Control Tower | [PyPI 1.0.0](https://pypi.org/project/agenticops-control-tower/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/agenticops-control-tower/releases/tag/v1.0.0) |
| Deep Agentic Core MCP | [PyPI 1.0.0](https://pypi.org/project/deep-agentic-core-mcp/1.0.0/) · [GitHub](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v1.0.0) |

Lens uses `v1.0.0-ecosystem` because its historical July `v1.0.0` GitHub tag
points to package 0.1.2. That historical tag/release remains unchanged; the
coordinated Python distribution version is 1.0.0 like the other packages.
AIOS is a repository/document release and is not published as a Python package.

## Compatibility and validation

Sibling dependency bounds admit the coordinated 1.x packages while retaining
existing compatible 0.x floors. Runtime behavior and existing native artifact
versions are preserved. AIOS 0.4/0.6/0.8 draft markers and Lens candidate
enterprise markers retain their maturity. The AIOS portable-suite snapshot
advances to repository v1.0.0; schema bytes and expected outcomes are unchanged.

The [exact source matrix](../release/candidate.json) and
[isolated installed-wheel evidence](../release/evidence/wheel-acceptance.json)
record internal engineering acceptance: six standalone wheels, the combined
matrix, 66 portable cases, five held-byte provenance-resolution cases, native
exports, negative controls and installed-source checks. Repository CI also
covers supported Python versions, native SDK adapters, downstream readers,
packaging and the MCP PostgreSQL/stdio paths.

The [publication receipt](../release/evidence/published-1.0.0.json) records the
all twelve published wheel/source artifacts with verified hashes and name/version
metadata. A fresh installation of the published matrix passed dependency checks,
portable/provenance cases, native exports, five CLI help commands and installed
source-origin checks. The published MCP wheel also passed standalone stdio
protocol acceptance, and MCP Registry publication succeeded. Package publication
does not deploy hosted services.
The optional Evals PRAgent review workflow could not check out its review
repository because its existing token is invalid; its Python, packaging,
containment and downstream compatibility checks passed.

## Continuing roadmap

Independent AIOS review, independent implementations, security/deployment
acceptance, authenticated live-provider validation and the stable contract
freeze remain open. No missing acceptance is recorded as passed. The strict
readiness report remains false until those inputs are supplied.

The maintainer authorized this milestone under the updated
[release policy](RELEASE_POLICY.md). See [the readiness plan](V1_READINESS.md)
for the remaining scope and evidence requirements.
