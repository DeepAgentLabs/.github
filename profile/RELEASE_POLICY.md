# Coordinated ecosystem release policy

Updated 2026-11-04.

DeepAgentLabs will continue delivering each project's remaining roadmap phases
through **minor releases**. Reserve **v1.0 for one coordinated ecosystem
launch**, rather than allowing each final feature phase to trigger its own
major release. No launch date is committed by this policy.

| Project | Final local phase / next minor target | Scope |
| --- | --- | --- |
| AI Operations Specification | v0.8 | Operational artifact drafts delivered in repository v0.8.0, following v0.7.0 guidance; independent review and stabilization remain open |
| Agentic Chaos | v0.11 | ChaosHub delivered in 0.11.0; coordinated stability remains open |
| Agentic Evals | v0.12 | Public API and report-schema readiness |
| Agentic Sidecar | v0.10 | Interoperability contract readiness |
| AgenticLens | v0.13 | Local candidate delivered in 0.13.0; independent security/deployment acceptance and coordinated stability remain open |
| DeepAgent MCP | v0.7 | Local candidate delivered in 0.7.0; coordinated stability and independent security/deployment acceptance remain open |
| AgenticOps Control Tower | v0.10 | Control-plane and capability-contract readiness |

The targets above replace package-local final v1.0 milestones. Historical
roadmap labels and already published versions remain unchanged. In particular,
Lens's earlier roadmap labels differ from package versions; the upcoming
v0.13 target follows the current 0.12.x package line. Additional minor releases
may be used when scope or evidence requires them. This policy does not itself bump package metadata or dependency ranges;
delivered status rows refer to the corresponding implementation releases.

## Gate for the coordinated v1.0 launch

All participating projects must satisfy their own published acceptance criteria
before the shared major release. Coordinate a tested version matrix, migration
and compatibility policies, documentation, examples, security/operational
acceptance evidence, CI, release candidates and publication plans. AIOS must
still satisfy its independent-review and independent-implementation gates;
coordination alone cannot make the draft specification stable.

API/schema freezing and stable-conformance claims belong to that coordinated
release after their gates pass. Minor readiness milestones can develop and
test candidate contracts without making those guarantees early. Native schema
versions such as Evals report `1.0` and the diagnosis taxonomy `1.0` are
independent of package release numbers and do not change under this policy.

The launch is coordinated, not an atomic cross-registry transaction. Each
package retains its own repository and release pipeline; publish from reviewed
merge commits, verify artifacts, and announce the shared v1.0 release only
when the agreed matrix is available. Keep package ownership and optional
integration boundaries intact.
