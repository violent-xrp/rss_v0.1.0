# RSS v0.1.0 — Claim Discipline

## Core rule
**Describe only what the current code and proof surface actually support.**

Use this sequence before public outreach:
1. Check the Roadmap baseline.
2. Check the Truth Register.
3. Verify the claim against the current code snapshot and acceptance suite.
4. State limitations alongside strengths.
5. Keep code-license and Pact-license language separate.

## Approved framing
Use language like:
- honest alpha/MVP
- domain-agnostic, application-layer zero-trust governance kernel
- pre-model governance pipeline
- hash-chained audit with cold verification
- stronger in architectural discipline than deployment maturity
- governed offline fallback and seeded demo world

## Disallowed framing
Do not say RSS v0.1.0 is:
- enterprise-complete
- cryptographically immutable
- a full deployment-layer zero-trust stack
- fully async-safe across all wrappers
- a polished production application

## Metric discipline
Current project-snapshot baseline:
- **138 test functions / 1155 assertions / 0 failures**
- **92.2% statement coverage**
- **138 claims / 138 tests / 101 Pact sections**
- **22 source modules in `src/rss/` package tree** (R1 restructure complete)

When metrics change:
- update `ROADMAP.md` first
- update the remaining docs from ROADMAP
- do not let older numbers persist in public docs
- if counts fall, explain why in plain language

## Repo-layout discipline
Public-facing root docs stay at the root:
- `README.md`
- `ROADMAP.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`

Supporting narrative docs belong under `docs/`.
Runtime/support code belongs under `src/`.
Runnable walkthroughs belong under `examples/`.

## Final language rule
Build ambitiously. Describe conservatively. Prove aggressively.
