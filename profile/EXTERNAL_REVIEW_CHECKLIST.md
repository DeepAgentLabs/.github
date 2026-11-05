# Review DeepAgentLabs: start here

**Choose one area, try the steps, send one report.** You do not need to read
all our repositories or review the entire ecosystem. Findings, failures and
confusing instructions are all useful feedback.

## 1. Choose one area

| What would you like to review? | Start here |
| --- | --- |
| Do the agent concepts make sense? | [A. Review the specification](#a-review-the-specification) |
| Can other tools exchange the data? | [B. Test data compatibility](#b-test-data-compatibility) |
| Are access controls and private data handled properly? | [C. Review security](#c-review-security) |
| Can I install and operate the software? | [D. Try a deployment or provider](#d-try-a-deployment-or-provider) |
| Can a newcomer follow the instructions? | [E. Try a quickstart](#e-try-a-quickstart) |

**Unsure? Start with A.** It needs no installation. The letters below map to
our detailed task IDs; you can simply write the letter in your report.

## 2. Follow your area's steps

### A. Review the specification

1. Read the [customer-support story](https://github.com/DeepAgentLabs/ai-operations-spec/blob/main/reviews/scenarios/scenario-01-customer-support.md).
2. Compare it with the [AIOS core concepts](https://github.com/DeepAgentLabs/ai-operations-spec/blob/main/specification/v0.1/core-concepts.md).
3. Tell us which parts you would call a Run, Step, model call, tool call,
   evaluation or incident. List anything missing or ambiguous.
4. Send your interpretation and questions using the report below.

For a complete framework mapping or telemetry review, continue to the
[detailed AIOS worksheet](https://github.com/DeepAgentLabs/ai-operations-spec/blob/main/reviews/EXTERNAL_REVIEW_TASKS.md).
Detailed task IDs: R1, R2, R6.

### B. Test data compatibility

1. Open the [portable test-suite instructions](https://github.com/DeepAgentLabs/ai-operations-spec/blob/main/specification/v0.6/conformance-suite/README.md).
2. Use your own validator, producer or consumer for the cases you cover.
3. Record expected vs actual results, commands, input/output files and the
   implementation/version used. Mark rules you did not implement as not tested.
4. Send the results. Running only our tools is useful reproduction, but does
   not count as an independent implementation.

[Full compatibility tasks](EXTERNAL_REVIEW_DETAILS.md#r3--can-an-outside-validator-reach-the-expected-results): R3–R5.

### C. Review security

1. Pick [Lens](https://github.com/DeepAgentLabs/agenticlens/blob/main/SECURITY.md),
   [MCP](https://github.com/DeepAgentLabs/mcp-server/blob/main/SECURITY.md) or
   [Tower](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/SECURITY.md).
2. Read that project's linked security policy and test an environment you are
   authorized to use. Check permitted access first, then denied access and
   private-data handling within the documented scope.
3. Record the steps, expected/actual behavior and impact.
4. Report suspected vulnerabilities **privately through that project's security
   reporting path**. Do not use the public report route for exploitable details.

[Full security tasks](EXTERNAL_REVIEW_DETAILS.md#r7--do-the-security-boundaries-hold): R7.

### D. Try a deployment or provider

1. Choose the [Lens setup](https://github.com/DeepAgentLabs/agenticlens/blob/main/docs/production-readiness.md),
   [MCP setup/rollback](https://github.com/DeepAgentLabs/mcp-server/blob/main/docs/release-readiness.md),
   [Tower setup](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/getting-started.md)
   or [Sidecar provider setup](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md).
2. Follow that guide in a fresh test environment. For services, try a restart
   and the documented recovery/rollback path. Record your environment and results.
3. For live providers, select actual models, supply credentials privately and
   run `uv run python scripts/smoke_judge_providers.py --require-all` from Sidecar.
   Calls may incur charges; skipped or mocked calls are not live evidence.
4. Send sanitized logs and what you did not test. Never include credentials.

[Full operator tasks](EXTERNAL_REVIEW_DETAILS.md#r8--can-an-operator-install-and-recover-the-supported-system): R8–R9.

### E. Try a quickstart

1. Choose one project from the [project list](README.md#projects).
2. Follow its quickstart and first example without extra maintainer instructions.
3. Send the steps that failed or confused you, your environment and the output.

[Full newcomer task](EXTERNAL_REVIEW_DETAILS.md#r10--can-a-newcomer-follow-the-documentation-helpful-feedback): R10.

## 3. Send one report

Copy the [report template](EXTERNAL_REVIEW_REPORT_TEMPLATE.md), fill only what
you tested, and paste it into a [new review issue](https://github.com/DeepAgentLabs/.github/issues/new).
An issue or PR in the affected project is also welcome. For **security findings**,
use the private route in C instead. Remove credentials and customer data.

Include your chosen area, exact versions/revisions, steps, expected vs actual
results and untested areas. Disclose any authorship, funding or editorial
relationship with DeepAgentLabs. A partial review is welcome; we will help
identify any additional evidence needed for formal acceptance.

**What happens next?** A maintainer clarifies scope, records your findings,
links fixes or explains disagreements, and updates only the acceptance tasks
actually covered. You do not need to write release-receipt JSON or decide
whether the ecosystem can launch.

For specialists and maintainers: [all detailed tasks and acceptance requirements](EXTERNAL_REVIEW_DETAILS.md).
