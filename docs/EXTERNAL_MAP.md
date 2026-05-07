# RSS External Map

_License: AGPLv3 documentation terms; see `../LICENSE/README.md`._

This is a plain-English bridge for engineers and reviewers who are new to the RSS vocabulary.

It does not rename the internal system. It maps the RSS terms to more familiar engineering concepts so reviewers can evaluate the mechanics without first learning the full project dialect.

## Register Rule

The Pact can use constitutional language because it is the constitutional document. Reviewer-facing and product-facing surfaces should translate that language into engineering terms when the formal register adds friction.

In particular:
- **Seat** should stay. It means a fixed authority surface whose responsibility survives code changes.
- **Council** should not be used as a general external label. There is no separate Council runtime actor, class, or vote path today. Any future Pact exception should be explicit and rare; the default should be replacement with more precise seat-class language.
- Prefer **the eight seats**, **operational seats**, **constitutional seats**, **authority surfaces**, or **governance modules** depending on audience.
- Product copy should say **operator**, **system owner**, **amendment workflow**, and **authority module** where those are clearer than sovereign/ceremony/seat language.

## Core Translation

| RSS term | Engineering translation | Current role |
| --- | --- | --- |
| The Pact | versioned constitutional policy source | Defines the law the runtime is built to honor. |
| Section 0 / Genesis | boot integrity anchor | Binds startup to an expected constitutional artifact. |
| WARD | routing and protected dispatch boundary | Routes tasks to seats while protecting governance fields. |
| SCOPE | data-access envelope | Declares allowed and forbidden sources before retrieval. |
| RUNE | meaning classifier | Classifies terms as sealed, soft, ambiguous, or disallowed. |
| OATH | consent and authority gate | Checks whether an action class is authorized. |
| CYCLE | cadence and rate-limit gate | Prevents runaway request loops and enforces container limits. |
| PAV | prepared advisory view | Sanitized evidence package exposed to an advisor or LLM. |
| TRACE | append-only audit chain | Records events and supports cold verification. |
| TECTON | tenant/container boundary | Isolates domain data, lifecycle state, and container-scoped requests. |
| REDLINE | never-expose data marker | Forces exclusion from advisory and normal response surfaces. |
| Safe-Stop | persistent halt state | Blocks requests at Stage 0 until cleared by T-0. |
| SEAL | amendment / artifact ratification | Handles review, approval, and ratification of governed artifacts. |
| SCRIBE | draft and proposal workspace | Builds candidate text and UAP bundles before sealing. |

## Seat Load-Bearing View

RSS has two seat rhythms. They differ by operating cadence, not by rank.

Operational seats participate in governed request flow:
- **WARD:** protects routing and dispatch surfaces.
- **SCOPE:** without it, data exposure is not bounded.
- **RUNE:** without it, meaning and disallowed terms drift.
- **OATH:** without it, authority becomes implicit.
- **CYCLE:** enforces cadence and rate limits.
- **TRACE:** without it, the system cannot prove what happened.

Constitutional seats participate in drafting, review, canonization, and amendment surfaces:
- **SCRIBE:** keeps drafting separate from ratification.
- **SEAL:** governs amendment and ratification ceremony.

The post-v0.1.0 audit question is not "can these names be merged?" It is "does each seat continue to own a unique invariant as connectors, per-action gates, and external trust anchoring arrive?"

Avoid implying that all seats act as one collective body. In ordinary governed requests, operational seats carry runtime work. In Pact/amendment work, constitutional seats carry drafting and sealing while TRACE records. The precision matters because it keeps the public architecture closer to the code.

## Public Positioning

Use conservative external language:
- "application-layer governance kernel"
- "pre-model data and authority boundary"
- "typed runtime gates"
- "hash-chained audit with cold verification"
- "alpha/MVP with explicit non-goals"

Avoid absolute claims:
- "solves prompt injection"
- "cryptographically immutable"
- "enterprise-complete"
- "safe for all future connectors"
- "full deployment-layer zero trust"

## Reviewer Shortcut

If a reviewer asks where the proof lives, point them to:
- `ROADMAP.md` for current truth and active work
- `TRUTH_REGISTER.md` for what can and cannot be claimed
- `docs/PACT_ALIGNMENT.md` for Pact-to-kernel alignment and known gaps
- `docs/claim_matrix.md` for claim-to-test traceability
- `docs/demo/DEMO_HANDOFF.md` for the demo artifact path
- `tests/test_all.py` for the canonical acceptance runner
