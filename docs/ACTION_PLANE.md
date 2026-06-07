# RSS Action Plane

_Licensed under AGPLv3; see `../LICENSE/README.md`._

## Status

This document is a future-design boundary, not a current release claim.

RSS v0.1.0 does not include a universal action plane, side-effect broker, connector sandbox, or per-tool-call enforcement loop. The current kernel governs request input, prepared advisory view construction, consent/authority checks, model exposure, and TRACE evidence. It does not yet execute arbitrary external actions through a contained broker.

This document does not amend the Pact and does not change the v0.1.0 proof surface.

## Purpose

The future action plane is the execution boundary below the governance kernel.

The kernel decides what may be seen, proposed, authorized, and recorded. The action plane would contain the execution of an already-authorized typed action and return an independently checkable receipt. It is not a shortcut around SCOPE, RUNE, OATH, CYCLE, WARD, SEAL, or TRACE.

## Design Rule

The model proposes. The kernel authorizes. The action plane contains and reports.

A sandbox or worker is containment, not authority. A tool call is not permitted because it is technically possible; it is permitted only if a typed proposal re-enters governance and receives bounded authorization before execution.

## Minimum Future Lifecycle

1. An `ActionProposal` is created from model, operator, or subsystem output.
2. The proposal schema, payload hash, target resource, actor, container, TTL, and action class are validated.
3. The proposal re-enters SCOPE, RUNE, execution validation, OATH, and CYCLE.
4. A short-lived capability lease is issued only for the approved action class, target, container, TTL, budget, and payload hash.
5. A broker executes the action inside a contained worker with no ambient credentials.
6. An independent verifier checks the artifact or side effect from fresh context.
7. TRACE records proposal, rejection or authorization, execution receipt, verifier report, and final outcome.

## Required Objects

- `ActionProposal`: typed, hash-bound request for a side effect.
- Capability lease: short-lived, scoped authorization bound to actor/request, action class, target, container, TTL, budget, and payload hash.
- Execution receipt: broker output describing exactly what ran and what artifact changed.
- Verifier report: independent check of the artifact or side effect, not a continuation of model reasoning.

## Hard Rules

- Model output is data until governed.
- No proposal authorizes itself.
- No ambient credentials in the broker.
- No artifact mutation without a TRACE-visible proposal and receipt.
- No reasoning handoff as proof; use artifact-only handoff plus independent verification.
- No current v0.1.0 claim expands until tests prove the action plane path.

## Non-Claims

RSS v0.1.0 does not claim:

- universal per-action or per-tool-call enforcement
- sandboxed external action execution
- connector-safe browser, email, document, RAG, or API actions
- cryptographic T-0 identity
- external audit anchoring for action receipts

## Relationship To ROADMAP

`ROADMAP.md` tracks when this lane becomes active and how it relates to the v0.1.1+ hardening queue. This file defines the boundary and vocabulary for that lane so future work does not blur current proof with future architecture.
