# Kernel Findings

_Licensed under AGPLv3; see `../LICENSE/LICENSE_INDEX.md`._

[ROADMAP's Current Build Thread](../ROADMAP.md#current-build-thread) owns
scheduling, priority, state, and disposition. This document owns kernel finding
detail, evidence, consequences, and proposed closure criteria. It is not another
queue, a release claim, or authorization to implement a remedy.

The initial entries consolidate unresolved requirements from the former
ROADMAP inventories and the [Phase Ledger](roadmap/PHASE_LEDGER.md). Source
observations below were checked at `0b4ca43` on 2026-09-11 without executing
runtime proofs. A documented design gap is not a reproduced exploit; proposed
closure criteria remain subject to the authorized design and review process.
Numbered Task IDs, when assigned, stay in ROADMAP rather than being duplicated
as a second status system here. [Action-plane detail](ACTION_PLANE.md) retains
ownership of broker lifecycle and universal side-effect enforcement.

## Caller Identity and Ingress Boundary

- **Finding:** the current ingress fence is trusted-process delegation, not
  authenticated caller identity. Three distinct requirements must survive
  consolidation: authenticate the external caller; bind that actor and request
  to container/scope authority; preserve the binding through wrappers and
  dispatch rather than accepting caller-supplied identity as authority.
- **Evidence:** [runtime.py](../src/rss/core/runtime.py),
  `_TECTON_INGRESS_TOKEN` and `Runtime.process_request`, reject non-GLOBAL
  container IDs without the sentinel. The source explicitly says an importer
  can obtain/spoof that token. [tecton.py](../src/rss/hubs/tecton.py),
  `Tecton.process_request`, supplies it during container delegation. The Phase
  Ledger's D/E/H entries retain authentication and wrapper guarantees as open.
- **Consequence:** an in-process origin check cannot substantiate deployment
  authentication, actor-bound leases, or an untrusted API-client boundary.
- **Proposed closure criteria:** specify the authenticating ingress and its
  trust assumptions; reject absent, forged, expired, or mismatched actor/request
  bindings; prove container and scope cannot widen through wrappers or tool
  dispatch. Preserve denial provenance without treating credentials as TRACE
  payloads. Coordinate with [worker context](#thread-and-worker-context-propagation),
  [recovery](#t-0-recovery-and-lock-out-before-keys), and the action-plane owner.

## Observable Stream Enforcement

- **Finding:** before-release chunk buffering, metering, mid-stream halt, and
  completion/halt receipts are future output-boundary work, not present stream
  enforcement or observation of hidden model reasoning.
- **Evidence:** [adapter.py](../src/rss/llm/adapter.py), `LLMAdapter.call`, sends
  `stream: False` and reads one complete response. `Runtime.process_request`
  calls `_validate_llm_response` after that return. The
  [three-window proposal](proposals/THREE_WINDOW_GOVERNANCE_MODEL.md) specifies
  the future observable-stream boundary and its non-claims.
- **Consequence:** post-response validation and a configured generation limit
  do not prove chunk-level containment, token/cost accounting, or mid-stream
  interruption across adapters.
- **Proposed closure criteria:** deterministic chunk fixtures must prove
  buffering before release, byte/chunk/token-estimate and cost-budget accounting,
  interruption on governed violations or cancellation, and completion versus
  halt receipts that do not expose suppressed output. Test chunk-boundary
  evasions and adapter failure; keep hidden-reasoning visibility a non-claim.

## Runtime Obligation Ledger

- **Finding:** a live record of duties continuing after authorization remains
  proposed; it must not create authority distinct from the governing decision.
- **Evidence:** the [three-window proposal's ledger](proposals/THREE_WINDOW_GOVERNANCE_MODEL.md#runtime-obligation-ledger)
  lists actor/request binding, container, consent source, action, target, payload
  hash, lease TTL, budgets, result import, verification, and TRACE obligations.
  [broker.py](../src/rss/action/broker.py), `_Authorization` and
  `SideEffectBroker._authorizations`, hold a narrower in-memory lifecycle.
- **Consequence:** an issued lease alone does not prove continuing budget,
  verification, result-import, or audit duties are tracked to completion.
- **Proposed closure criteria:** first settle lease/lifecycle semantics with
  the action-plane owner; define the complete obligation record and persistence
  or explicit non-persistence policy. Prove completion, expiry, revocation,
  failed execution/import, restart, and receipt-failure transitions cannot lose
  duties or mint authority. Bind every record to the original actor/request,
  container, action/target, payload, consent source, limits, and required evidence.

## OATH Consent Duration and Coercion Semantics

- **Finding:** consent duration is recorded but not enforced as expiry; the
  coercion helper is an urgency-keyword flag, not general coercion detection.
- **Evidence:** [oath.py](../src/rss/governance/seats/oath.py), `ConsentRecord`,
  `Oath.authorize`, and `Oath.deny` carry `duration` and `granted_at`, while
  `Oath.check` selects status without a clock or duration calculation.
  `detect_coercion_keyword_limited` checks five fixed substrings;
  `detect_coercion` is a compatibility wrapper. [Pact alignment](PACT_ALIGNMENT.md)
  explicitly limits the current coercion wording.
- **Consequence:** a duration field cannot support a claim of expiring consent,
  and an urgency hit cannot establish coercion, intent, or authority to override.
- **Proposed closure criteria:** decide the duration policy explicitly: enforce
  expiry with deterministic time and restart semantics, or retain metadata-only
  behavior with approved claim/Pact alignment. Prove exact expiry boundaries,
  restrictive precedence, and grant-time/duration restoration. Separately define
  governed warning, confirmation, and refusal semantics for coercion concerns;
  measure false positives/negatives and preserve the keyword-limited contract
  until stronger behavior is implemented and proved. Neither path may grant
  authority merely because a warning is absent.

## OATH Audit Dual-Failure Gap

- **Finding:** consent persistence failure can be followed by failure of its
  failure-notification/audit path without a durable receipt of that attempt.
- **Evidence:** `Oath.authorize`, `deny`, and `revoke` catch persistence failure,
  preserve prior in-memory state, and return structured refusal. Their nested
  `_failure_callback` exception is swallowed. In [runtime.py](../src/rss/core/runtime.py),
  `Runtime.__init__` installs `_oath_failure_handler`, which also catches an
  exception from `_log("OATH_PERSISTENCE_FAILURE", ...)`. These are source-level
  failure paths, not a new live fault-injection result from this documentation pass.
- **Consequence:** refusing a new consent mutation does not establish complete
  audit evidence. For failed revocation, the prior grant can remain in effect;
  the refusal must not be described as a completed revocation.
- **Proposed closure criteria:** choose a bounded last-resort failure signal or
  recovery fence that cannot recurse indefinitely through the broken audit
  path. Inject persistence-only, notification-only, and dual failures across
  grant/deny/revoke; prove prior state, explicit caller outcome, durable evidence
  when possible, and honest uncertainty when not. Never manufacture a successful
  consent or audit receipt, and do not disclose sensitive payloads in diagnostics.

## RUNE Registry Scale

- **Finding:** classification and embedded-disallowed scans iterate the active
  in-memory collections. A large-pack performance guarantee is not established.
- **Evidence:** [rune.py](../src/rss/governance/seats/rune.py),
  `MeaningLaw.classify`, `classify_all`, `_detect_compounds`, and
  `scan_disallowed`, loop through `_registry` or `_disallowed`.
  `Term` has version metadata but no active/archived lifecycle field.
- **Consequence:** expanding global vocabulary increases scan work; retaining
  every historical term in the active path conflates historical meaning with
  current classification cost. No benchmark bound is inferred here.
- **Proposed closure criteria:** define relevant active registry partitions,
  compiled multi-pattern indexing rebuilt on registry changes, and an
  active/archive/retirement lifecycle preserving auditable historical meaning.
  Compare indexed results against the existing classification order and
  restrictive behavior; measure scale and update costs on declared workloads
  before making large-pack claims. Namespace policy belongs to the next entry.

## RUNE Pack Namespaces and Synonym Confidence

- **Finding:** terms, synonyms, and disallowed phrases lack a pack/domain/container
  selector in the classification API. MED and LOW synonyms have the same
  returned confirmation state, despite being distinct stored labels.
- **Evidence:** `MeaningLaw` owns single `_registry`, `_synonyms`, and
  `_disallowed` dictionaries; `add_synonym` keys by normalized phrase.
  `classify` maps HIGH to SOFT and both MED/LOW to AMBIGUOUS with identical
  wording. `TermStatus` does not return a separate confidence field.
- **Consequence:** freely composing packs can collide on shared phrases, and
  three stored confidence labels do not prove three distinct user-visible
  confirmation policies.
- **Proposed closure criteria:** partition vocabulary by approved pack/domain/
  container context while keeping tenant policy unable to loosen the global
  floor. Prove phrase reuse, cross-pack isolation, version selection, retirement,
  and persistence/restore behavior. Decide through the normal approval process
  whether to align confidence wording to current states or implement distinct
  MED/LOW confirmation semantics with returned metadata and tests. Preserve both
  requirements; namespacing alone does not close confidence semantics.

## RUNE Unicode and Confusable Normalization

- **Finding:** current normalization is useful but not complete visual-confusable
  resistance or a guarantee for all boundary-sensitive labels.
- **Evidence:** `rune._normalize_phrase` applies NFKC, strips a bounded control
  set and surrounding punctuation, and collapses whitespace. Its docstring
  explicitly excludes full homoglyph folding. `_word_boundary_match` uses
  escaped labels with regular-expression word boundaries.
- **Consequence:** visually similar characters, punctuation-heavy/apostrophe-like
  labels, combining marks, and boundary interactions need explicit policy and
  regression evidence rather than a general Unicode-safety claim.
- **Proposed closure criteria:** define confusable handling and allowed label
  forms without silently merging distinct legitimate terms. Build a corpus of
  compatibility forms, invisible/confusable characters, punctuation, apostrophes,
  internal hyphens, and combining marks; prove restrictive precedence, lookup/
  registration symmetry where intended, and bounded false positives. Keep
  connector-specific import cases routed to their own acceptance matrix.

## Seat Load-Bearing Audit

- **Finding:** interface conformance does not establish that every seat carries
  a unique enforced invariant on every relevant ingress and action path. The
  requested audit remains open; this is not a finding that a seat is redundant.
- **Evidence:** [ward.py](../src/rss/governance/seats/ward.py),
  `Ward.register_seat`, checks `status` and `handle`; `Ward.route` enforces its
  hook contract. `Runtime.__init__` registers the seats, while
  `Runtime.process_request` invokes seats directly. RUNE's `handle` docstring
  explicitly distinguishes its adapter from direct runtime request-path calls.
- **Consequence:** registration and isolated seat tests cannot, alone, establish
  end-to-end enforcement or that a routing/hook guarantee is on the active path.
- **Proposed closure criteria:** map each seat to its unique invariant, actual
  caller paths, authority boundary, and registered behavioral proof as connectors
  and per-action gates arrive. Demonstrate which invariant fails when a seam is
  bypassed; decide explicitly whether an unused route should be wired or retired.
  Do not add architectural layers or rename seats merely to improve the diagram.

## Thread and Worker Context Propagation

- **Finding:** current context-bound hub isolation does not establish every
  future ASGI, worker, background-job, or external-tool propagation contract.
- **Evidence:** `ACTIVE_HUBS` and `Runtime.hubs` select context-local hubs with
  global fallback. `Tecton.process_request` sets the context and resets its token
  in `finally`. [Pact alignment](PACT_ALIGNMENT.md) distinguishes existing
  isolation/reset proof from the child-worker binding edge; the Phase Ledger's
  D/E open lists retain wrapper guarantees.
- **Consequence:** a wrapper that loses or wrongly reuses context can select the
  wrong data topology; a clean parent request does not prove child dispatch safe.
  Propagation must be checked per dispatch API, not inferred for all threads.
- **Proposed closure criteria:** inventory each supported async/thread/process
  dispatch and its actual propagation behavior; require explicit actor,
  container, scope, and hub bindings where needed. Prove nested calls, concurrent
  tenants, cancellation, exceptions, worker reuse, missing context, and cleanup.
  Define safe refusal versus permitted global fallback before wrappers ship.

## T-0 Recovery and Lock-Out Before Keys

- **Finding:** the current sovereign-command seam is a soft gate; future
  mechanical/cryptographic identity must not make possession of one key the
  only means of lawful recovery.
- **Evidence:** [t0.py](../src/rss/governance/t0.py), `authorize_t0`, checks
  `t0_command` and explicitly denies being identity proof. Runtime Safe-Stop
  clearing and protected RUNE mutations use that seam. `SafeStopRecovery`
  restricts halted-bootstrap access but does not supply recovery credentials.
  The prior recovery-first requirement is also retained in
  [Pact alignment](PACT_ALIGNMENT.md).
- **Consequence:** calling the current flag authentication overstates the
  boundary; adding keys without recovery design can instead strand legitimate
  sovereign authority. Operational tenant credentials must remain subordinate
  to, and unable to amend, that authority.
- **Proposed closure criteria:** design and approve auditable manual recovery,
  bypass, credential rotation, and revocation before keys become load-bearing.
  Prove lost/compromised credentials, denied recovery, replay, interrupted
  ceremony, and Safe-Stop restart paths. Keep keys out of source, Pact text, and
  TRACE payloads; separate operational roles from constitutional authority.
  Retain the rule that Section 0 file export requires a Genesis re-anchor plus
  boot/tamper/recovery proof rather than treating it as ordinary file export.

## Atomic Safe-Stop Entry

This adjacent finding supplies the explicitly requested near-term queue item;
it is separate from the eleven legacy kernel findings above.

- **Finding:** Safe-Stop entry does not share the already-bounded atomic-clear
  mechanism; persisting the halt and recording its entry event are separate calls.
- **Evidence:** `Runtime.enter_safe_stop` checks for an existing halt, then calls
  `Persistence.enter_safe_stop(reason)` followed by `_log("SAFE_STOP_ENTERED",
  ...)`. [sqlite.py](../src/rss/persistence/sqlite.py),
  `Persistence.enter_safe_stop`, commits the `system_state` write in its own
  connection context. The clear path instead uses
  `clear_safe_stop_with_trace_event`; that difference is not entry atomicity.
- **Consequence:** a durable halt can exist without the corresponding entry
  receipt if the subsequent audit append fails. A successful clear proof cannot
  establish symmetric entry behavior, and audit failure must not release a halt.
- **Proposed closure criteria:** specify one bounded halt/receipt outcome model,
  including pre-existing halt idempotence and preservation of its first reason.
  Prove success, state-write failure, receipt failure, rollback failure,
  post-commit error, and restart reconciliation. Preserve an existing halt;
  report unconfirmed durability explicitly, keep hot/cold evidence consistent,
  and choose a fail-closed recovery outcome without falsely claiming a receipt
  or durable halt that was not established. No implementation is authorized here.
