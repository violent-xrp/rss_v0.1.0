# Three-Window Governance Model

_License: CC BY-ND 4.0 discipline material; see `../../LICENSE/CC BY-ND 4.0.md`._

## Status

Proposal. This document is a future architecture note, not a current release claim and not Pact text.

RSS currently has its strongest proof at the pre-model boundary: scope, meaning, consent, cadence, container isolation, PAV construction, REDLINE exclusion, and TRACE evidence before governed context reaches a model. The next architecture target is a three-window governance model that keeps the same discipline before, during, and after model output.

## Canonical Statement

RSS should evolve toward three enforcement windows: before model exposure, during observable output generation, and after output when proposed actions must re-enter governance before execution.

## Waiting Posture

The phrase **"An AI that waits"** captures the intended posture of the governed system.

RSS should wait for scope, consent, authority, cadence, verification, and user sovereignty before acting. Waiting is not a delay artifact; it is the control boundary. A system that cannot wait cannot be trusted with agency.

This phrase is positioning language, not proof by itself. Public use should stay tied to specific enforced waits: before model exposure, before streamed output release, and before side effects execute.

## Window 1: Before Model Exposure

This is the current core of RSS.

The kernel decides what the model may see before model exposure:

- SCOPE declares allowed and forbidden sources.
- RUNE classifies meaning and sealed terms.
- OATH checks consent and authorization.
- CYCLE bounds cadence and request load.
- TECTON binds tenant/container context.
- PAV construction creates a least-context advisory view rather than exposing the full data environment.
- REDLINE/protected material is excluded from model-facing context.
- TRACE records the governed path.

Public claims may describe this window as current behavior only where the acceptance runner, claim matrix, and current docs support it.

## Window 2: During Observable Generation

RSS should not claim to observe model "thinking" unless it has access to model internals such as hidden reasoning traces, activations, attention, or provider-side telemetry. The application-layer boundary RSS can govern is the observable output stream.

Future during-generation enforcement should govern:

- streamed chunks before release to the user or downstream system
- buffered partial output
- byte counts, chunk counts, and token estimates
- mid-stream REDLINE/governance-pattern detection
- CYCLE token and cost budgets
- stream-completion receipts
- stream-halt receipts that name the violated class without leaking suppressed text

The public phrase should be "during observable output generation" or "at the token-stream/output boundary," not "during thinking."

## Window 3: After Output

Model output remains data after generation. It does not become authority by being fluent, useful, or confirmed by a user.

Future after-output enforcement should require proposed side effects to become typed, hash-bound action proposals before execution:

- the output is parsed into an `ActionProposal`
- proposal schema, payload hash, TTL, actor, container, target, and action class are validated
- the proposal re-enters SCOPE, RUNE, execution validation, OATH, and CYCLE
- authorization produces a bounded capability lease, not open-ended permission
- execution occurs through a contained broker with no ambient credentials
- tool or connector results return through the untrusted-content import path
- TRACE records proposal, rejection or authorization, execution receipt, verifier report, and final outcome

Human confirmation is not enough by itself. Confirmation may approve a bounded lease, but RSS must continue enforcing the active constraints after confirmation.

## Runtime Obligation Ledger

The after-output layer needs a live record of active constraints. This proposal uses the term **Runtime Obligation Ledger** for that future surface.

The ledger would track active duties created by authorization:

- actor/request binding
- container binding
- consent source
- action class
- target resource
- payload hash
- lease TTL
- rate/token/cost budget
- result-import requirement
- verification requirement
- TRACE receipt obligations

This is not a new source of authority. It is the runtime record of what the kernel already authorized and what remains required before, during, and after execution.

## Build Sequence

1. Recut the stream-gate prototype into staging only after review proves it is deterministic, receipt-backed, and safe against leaking suppressed output.
2. Add CYCLE/PAV budget accounting for token estimates, context ceilings, and cost envelopes before making token-economy claims.
3. Recut the typed action-proposal and broker path in small slices: proposal object, validation, RUNE/OATH/CYCLE re-entry, lease issuance, execution receipt, and result import.
4. Add the Runtime Obligation Ledger only after the action proposal and lease semantics are stable enough to track.
5. Update README or public-facing site language only after the relevant window has code proof and current docs can state exactly what is built.

## Non-Claims

This proposal does not claim that RSS currently:

- observes hidden model reasoning or internal model activations
- performs full token-stream enforcement in the released kernel
- executes arbitrary tools through a side-effect broker
- maintains a runtime obligation ledger
- enforces token/cost budgets across all adapters
- provides production zero-trust deployment guarantees

## Relationship To Existing Docs

- `../ACTION_PLANE.md` defines the future side-effect broker boundary.
- `../PACT_ALIGNMENT.md` tracks claim-vs-code gaps and wording cautions.
- `../../ROADMAP.md` owns sequencing and release boundaries.
- `../TESTING.md` tracks the future cross-OS proof posture for Windows, Linux, Android-adapter, and macOS gates.
- `../PROJECT_CONTROL_SURFACE.md` explains which documents own which claims.
