# RSS Action Plane

_Licensed under AGPLv3; see `../LICENSE/README.md`._

## Status

This document is a boundary document. It separates the current proposal/broker
decision surface from future execution wrappers and universal tool-call
enforcement.

RSS now includes a structured action proposal and in-process side-effect broker
decision surface in `rss.action`. It can review a proposed side effect, emit
TRACE receipts, issue a short-lived single-use authorization receipt, re-check
Safe-Stop at claim time, support revocation, and import a claimed result as
untrusted data-only evidence.

RSS does not yet include a universal action plane, connector sandbox,
per-tool-call enforcement loop, external execution wrapper, durable
restart-surviving leases, or runtime auto-wiring from model output to broker.
The current kernel governs request input, prepared advisory view construction,
consent/authority checks, model exposure, TRACE evidence, and the local
pre-execution broker decision surface. It does not execute arbitrary external
actions through a contained worker.

This document does not amend the Pact and does not change the v0.1.0 proof surface.

## Relationship To Three-Window Governance

The action plane is the future **after-output** window in the broader three-window model:

1. **Before model exposure:** RSS decides what governed context may reach the model.
2. **During observable output generation:** a future stream gate may inspect buffered output chunks, meter token/cost budgets, and halt before unsafe text is released.
3. **After output:** model output remains data; any proposed side effect must become a typed action proposal and re-enter governance before execution.

RSS should not describe this as observing model "thinking" unless it has access to model internals. The application-layer claim is narrower: observable output generation and proposed side effects can be governed.

See `proposals/THREE_WINDOW_GOVERNANCE_MODEL.md` for the planning model.

## Purpose

The action plane is the execution boundary below the governance kernel. The
first code-backed slice is the proposal/broker decision surface; contained
execution remains future work.

The kernel decides what may be seen, proposed, authorized, and recorded. The
current broker can authorize or refuse an in-process receipt, but it does not
perform the side effect. A future action plane would contain the execution of an
already-authorized typed action and return an independently checkable receipt.
It is not a shortcut around SCOPE, RUNE, OATH, CYCLE, WARD, SEAL, or TRACE.

## Design Rule

The model proposes. The kernel authorizes. The action plane contains and reports.

A sandbox or worker is containment, not authority. A tool call is not permitted because it is technically possible; it is permitted only if a typed proposal re-enters governance and receives bounded authorization before execution.

## Lifecycle Boundary

Built today:

1. An `ActionProposal` is created from a structured payload.
2. The proposal schema, payload hash, target resource, container, TTL, and action class are validated.
3. The broker re-enters local governance gates: Safe-Stop, payload hash, TTL, tool policy, RUNE, OATH, and CYCLE.
4. A short-lived in-process receipt is issued only after the gates pass.
5. A caller must claim the receipt before acting; Safe-Stop and revocation are checked again at claim time.
6. A claimed result may be imported as untrusted data-only evidence.
7. TRACE records proposal, rejection, authorization, claim refusal, claim, revocation, and result import.

Future work:

1. Bind model/operator output into the broker path instead of free-text execution.
2. Add actor/request identity and durable or explicitly non-durable lease policy.
3. Execute authorized actions inside contained workers with no ambient credentials.
4. Add independent verifier reports for artifacts and side effects.
5. Track active obligations after authorization.

## Required Objects

- `ActionProposal`: typed, hash-bound request for a side effect. Built.
- Broker decision: gate-reviewed authorization or refusal with TRACE receipts. Built.
- In-process receipt: short-lived, single-use, revocable pre-execution receipt. Built, but not durable across restart.
- Execution receipt: future broker/wrapper output describing exactly what ran and what artifact changed.
- Verifier report: future independent check of the artifact or side effect, not a continuation of model reasoning.
- Runtime obligation ledger: future live record of active leases, budgets, container bindings, result-import requirements, and TRACE obligations after authorization.

## Hard Rules

- Model output is data until governed.
- No proposal authorizes itself.
- No ambient credentials in the broker.
- No artifact mutation without a TRACE-visible proposal and receipt.
- No reasoning handoff as proof; use artifact-only handoff plus independent verification.
- No public claim expands from local broker decision to external execution until tests prove the execution wrapper path.

## Non-Claims

RSS does not claim:

- universal per-action or per-tool-call enforcement
- sandboxed external action execution
- connector-safe browser, email, document, RAG, or API actions
- durable or restart-surviving capability leases
- runtime auto-wiring from model output into broker execution
- cryptographic T-0 identity
- external audit anchoring for action receipts

## Relationship To ROADMAP

`ROADMAP.md` tracks when this lane becomes active and how it relates to the v0.1.1+ hardening queue. This file defines the boundary and vocabulary for that lane so future work does not blur current proof with future architecture.
