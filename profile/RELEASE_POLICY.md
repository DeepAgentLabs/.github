# Coordinated ecosystem release policy

Updated 2026-11-05.

## The 1.0.0 milestone

The maintainer authorized a coordinated 1.0.0 release as an incremental ecosystem
milestone. Feature delivery, validation and roadmap work continue after it.
This decision supersedes the earlier policy that reserved the package major
version for completion of every independent acceptance and stable-schema gate.

All seven projects participate: AI Operations Specification, AgenticLens,
Agentic Evals, Agentic Chaos, Agentic Sidecar, Deep Agentic Core MCP and
AgenticOps Control Tower. AIOS is a repository/document release; the other six
publish Python distributions through their existing tag-triggered workflows.

Package/repository version 1.0.0 does not change artifact schema versions,
promote draft/candidate contracts, certify AIOS conformance or establish
production deployment readiness. Existing scope and limitations remain in each
project's guides. Alpha/experimental capabilities retain their stated maturity.
Breaking changes to supported package interfaces require a major version;
draft/candidate contracts continue under their documented evolution policies.

## Follow-up acceptance work

The following work remains open and is not represented as passed or waived
validation evidence:

- Independent AIOS review of prerequisite layers and operational mappings.
- Independent validator, producer and consumer implementations.
- Independent security review and operator deployment acceptance.
- Authenticated OpenAI and Anthropic provider acceptance.
- Final stable contract freeze, migration and compatibility acceptance.

These items remain on the roadmap and in the executable readiness report.
`release_readiness.py --require-ready` continues to enforce all of them for a
full stability claim. A milestone version does not make that report ready.
The 1.0.0 publication decision permits release while that report remains false.
Never fabricate external reviewers, provider observations or freeze approvals.

## Publication requirements

- Prepare matching package/runtime versions, dated changelogs, registry metadata,
  lockfiles and sibling dependency bounds that admit the coordinated 1.x matrix.
- Run each repository's required checks and package validation.
- Test the exact committed matrix with isolated installed wheels, native exports,
  portable schema cases, provenance resolution and negative controls. Record
  internal evidence with its real source attribution and source pins.
- Merge release changes through the existing repository process, then push an
  annotated v1.0.0 tag using the matching changelog section as its message.
- Verify PyPI/GitHub/MCP Registry publication. Publish in dependency order and
  announce completion only after the coordinated matrix is available.

This is not an atomic registry transaction. Publication does not deploy hosted
AWS/Render services. Keep project ownership and optional integration boundaries.
See [the readiness plan](V1_READINESS.md) for the remaining acceptance scope.
