# RSS and the NIST AI RMF

_Licensed under AGPLv3; see `../LICENSE/README.md`._

This document maps Rose Sigil Systems (RSS) to the NIST AI Risk Management Framework (AI RMF) as a reviewer aid.

It is not a certification, compliance statement, audit opinion, or production deployment claim. RSS v0.1.0 is an alpha governance-kernel prototype. The purpose of this map is to show how the current RSS mechanisms express control thinking that aligns with the AI RMF's Govern, Map, Measure, and Manage functions.

Official framework sources:

- NIST AI RMF 1.0: <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST AI RMF Playbook: <https://airc.nist.gov/airmf-resources/playbook/>
- NIST AI RMF Generative AI Profile: <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence>

## How To Read This Map

The AI RMF is voluntary guidance for managing AI risks across design, development, deployment, and use. Its core functions are:

- **Govern:** establish policies, accountability, risk posture, and oversight.
- **Map:** understand context, actors, data, purpose, risks, and boundaries.
- **Measure:** evaluate, test, monitor, and document system behavior and risk.
- **Manage:** prioritize, respond to, and reduce identified risks.

Govern is cross-cutting; it informs the other functions rather than appearing only once in a pipeline.

RSS is narrower than the whole AI RMF. It is not an enterprise governance program. It is a working application-layer kernel that explores pre-model controls: scoped context, authority checks, audit evidence, fail-closed behavior, and recovery.

## Summary Mapping

| AI RMF function | RSS mechanism | Current proof surface | Known limit |
| --- | --- | --- | --- |
| Govern | Pact, Genesis binding, version model, T-0 seam, claim discipline | `pact/`, `src/rss/core/config.py`, `src/rss/core/runtime.py`, `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, `docs/PACT_ALIGNMENT.md` | T-0 is still a soft command seam, not cryptographic identity. |
| Map | SCOPE, PAV, REDLINE, TECTON, threat model | `src/rss/governance/seats/scope.py`, `src/rss/hubs/pav.py`, `src/rss/hubs/tecton.py`, `THREAT_MODEL.md`, `docs/EXTERNAL_MAP.md` | Future connectors need connector-specific threat tests before claims expand. |
| Measure | acceptance runner, coverage, claim matrix, reverse code map, TRACE cold verification | `tests/test_all.py`, `run_coverage.py`, `docs/claim_matrix.md`, `docs/pact_code_map.md`, `src/rss/audit/verify.py` | Local proof does not equal operational monitoring or external non-repudiation. |
| Manage | Safe-Stop, OATH, CYCLE, REDLINE redaction, guarded canon export, amendment workflow | `src/rss/core/runtime.py`, `src/rss/governance/seats/oath.py`, `src/rss/governance/seats/cycle.py`, `src/rss/audit/pact_canon_export.py`, `src/rss/governance/seats/seal.py` | Universal per-action/tool-call enforcement remains future action-plane work. |

## Govern

RSS uses a versioned policy source, called the Pact, as the governing text for the kernel. Section 0 is tied to startup through the Genesis hash, and runtime behavior is checked against the current constitutional artifact before ordinary requests proceed.

Current RSS evidence:

- The Pact defines the authority model and release/version boundaries.
- Section 0 / Genesis binds boot integrity to an expected source artifact.
- Safe-Stop clearing, RUNE mutations, and SEAL operations route through a shared soft T-0 authorization seam.
- `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, `docs/PACT_ALIGNMENT.md`, and generated proof docs constrain what the repo can claim publicly.
- `docs/VERSIONING.md` separates project semver, release-candidate iteration, and Pact section versions.

What this demonstrates:

- Policy and implementation are intentionally connected.
- Release claims are constrained by runner-truth evidence.
- Known limits are named rather than hidden.

Current limits:

- The T-0 authorization seam is not cryptographic identity.
- RSS does not implement a complete enterprise governance process.
- The public docs should describe alignment and evidence, not NIST compliance.

## Map

RSS maps each request before model exposure. It determines what data is in scope, what meaning has been classified, whether protected sources must be excluded, and which container or tenant boundary applies.

Current RSS evidence:

- SCOPE creates bounded access envelopes.
- PAV constructs a prepared advisory view instead of exposing the full data environment.
- REDLINE entries are excluded from model-facing context and redacted if detected after model output.
- TECTON isolates tenant/container data and container-scoped request behavior.
- `THREAT_MODEL.md` documents current risk boundaries and future connector risks.
- `docs/EXTERNAL_MAP.md` translates internal RSS names into familiar engineering control concepts.

What this demonstrates:

- Context is selected before the model sees it.
- Sensitive data handling is a structural boundary, not only an output filter.
- Tenant/container state is a first-class risk boundary.

Current limits:

- Deployment-layer caller identity is not cryptographic yet.
- Future browser, email, document, RAG, and tool-return connectors require their own indirect prompt-injection and data-boundary tests.
- Some declared envelope fields remain future or bounded controls rather than full deployment guarantees.

## Measure

RSS treats evidence as part of the system, not an afterthought. The project maintains a local proof baseline, claim-to-test traceability, reverse code-to-Pact traceability, and cold audit verification.

Current RSS evidence:

- `tests/test_all.py` is the canonical acceptance runner.
- `run_coverage.py` reproduces statement coverage.
- `docs/sync_baseline.py` keeps public proof numbers synchronized and fails closed when coverage proof is missing unless explicitly skipped.
- `docs/claim_matrix.md` maps Pact claims to tests.
- `docs/pact_code_map.md` maps code references back to Pact sections.
- TRACE events are hash-chained and can be verified cold from SQLite.
- Demo artifact generation records operator-readable and machine-readable evidence for guided review.

What this demonstrates:

- Public claims have mechanical evidence.
- Reviewers can reproduce the current proof surface.
- Audit evidence can be inspected outside the running kernel.

Current limits:

- The TRACE chain does not yet provide external timestamping or independent non-repudiation.
- Local tests and demo artifacts are not the same as production telemetry.
- Current proof is strongest for single-process kernel behavior, not distributed deployment.

## Manage

RSS manages AI workflow risk through fail-closed behavior and explicit recovery paths. It does not treat fluent model output as authority.

Current RSS evidence:

- Safe-Stop blocks requests when core integrity or audit assumptions fail.
- OATH checks consent/authority before governed actions proceed.
- CYCLE constrains request cadence and container rate limits.
- RUNE blocks disallowed terms and distinguishes sealed, soft, ambiguous, and disallowed meaning states.
- REDLINE content is excluded from PAV and redacted if detected in post-LLM output.
- SEAL and SCRIBE support governed amendment and ratification workflows.
- The guarded Pact canon exporter refuses Section 0 and requires explicit soft T-0 write authorization for Sections 1-7.

What this demonstrates:

- Uncertainty and missing authority become explicit states.
- Risk response can halt, narrow, refuse, or require recovery rather than improvising.
- Constitutional text and implementation can be reconciled through guarded tools.

Current limits:

- The action plane is not complete; universal per-action/tool-call enforcement remains future work.
- Section 0 export remains a separate Genesis-aware future ceremony.
- Cryptographic identity, external audit anchoring, and deployment-grade incident handling are not v0.1.0 claims.

## Generative AI Profile Relevance

The NIST Generative AI Profile is relevant because RSS focuses on the boundary where generative systems receive context and produce responses.

RSS currently emphasizes:

- pre-model data minimization through SCOPE and PAV
- authority and consent checks before model exposure
- REDLINE exclusion and output redaction
- audit evidence for later review
- human recovery through Safe-Stop and T-0 command paths
- explicit distinction between model advice and system authority

This is not a full generative AI governance program. It is a working prototype for one part of the problem: runtime controls around context, authority, evidence, and recovery.

## Naming Translation

RSS uses internal names, but the names are not decorative. Each points to a control responsibility:

| RSS name | Framework-friendly meaning |
| --- | --- |
| Pact | policy source / governance source of truth |
| Seat | fixed authority surface |
| SCOPE | data access boundary |
| RUNE | meaning and prohibited-term classifier |
| OATH | consent and authority gate |
| CYCLE | cadence / runaway-control gate |
| TRACE | audit evidence layer |
| SCRIBE | drafting workspace |
| SEAL | ratification and canonization workflow |
| TECTON | tenant/container isolation |
| PAV | prepared evidence/context package |
| REDLINE | never-expose data marker |
| Safe-Stop | persistent halt and recovery state |

For a fuller plain-English vocabulary bridge, see `docs/EXTERNAL_MAP.md`. For Tier 2 subsystem handles, see `docs/SUBSYSTEM_HANDLES.md`.

## Non-Claims

Do not use this document to claim:

- NIST certification
- NIST compliance
- production readiness
- enterprise deployment
- complete zero trust
- cryptographic identity proof
- external non-repudiation
- complete per-action/tool-call enforcement

The stronger and more honest claim is:

> RSS is a test-backed alpha prototype showing how pre-model AI workflow governance controls can be expressed as runtime mechanics and mapped to recognized AI risk-management functions.
