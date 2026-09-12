# RSS — Roadmap

_Licensed under AGPLv3; see `LICENSE/LICENSE_INDEX.md`._

ROADMAP is the rolling work queue for the RSS kernel and its build system.
It selects work and records disposition; linked owners hold technical detail.
The current line is treated as Genesis. The next version decision is deferred,
not inferred from an old phase label or a local tag.

## Active Work

### Current Build Thread

KERNEL-02 is locally checkpointed after independent review and human disposition.
Table order records the human-approved sequence, starting with DOCS-03 and then
the coordination tasks below. Queue rows schedule work only; no implementation
or Git operation is authorized by a queue row.
Each slice needs bounded proof, cross-family review relayed through the human
controller, and disposition before advancing. Remaining kernel work is retained
after that sequence; BUILD-02/03 stay deferred. Report new safety blockers first.

| Workstream | Task ID | Work | State | Evidence | Next action | Detail owner |
| --- | --- | --- | --- | --- | --- | --- |
| Build system | DOCS-03 | Remaining documentation-index routing | paused | unreviewed | Reconcile the missing index entries after the KERNEL-02 checkpoint; no further roadmap redesign. | [Index follow-up](docs/PROJECT_CONTROL_SURFACE.md#deferred-index-reconciliation) |
| Build system | BUILD-05 | Roots promotion readiness | paused | unreviewed | After DOCS-03, check Main ancestry and reconcile Main-only commits into Roots with approval if needed; reproduce complete applicable gates at the resulting checkpoint and obtain cross-family review of the Main-bound diff. | [Promotion loop](docs/BUILD_DISCIPLINE.md#promotion-and-reconciliation-loop), [owed proof](#release-boundary) |
| Build system | BUILD-06 | Main promotion and Roots reconciliation | paused | unreviewed | After BUILD-05 acceptance and exact Git approval, merge into Main, gate the result and push; reconcile Main back into Roots, gate and push Roots. No tag. | [Promotion loop](docs/BUILD_DISCIPLINE.md#promotion-and-reconciliation-loop) |
| Build system | BUILD-07 | Preservation-first Lab baseline refresh | paused | unreviewed | After BUILD-06, verify recoverable preservation of unique Lab history, dirty/untracked work and needed ignored context before any replacement; review dispositions, then refresh shared baseline/instructions with approval. Keep experiments and Lab rules distinct; no blind reset or wholesale Lab promotion. | [Lane boundaries](docs/BUILD_DISCIPLINE.md#three-trees-one-direction-of-trust) |
| Build system | BUILD-08 | Separate Taproot review handoff | paused | unreviewed | After BUILD-07, route pending method changes into a separate Taproot review/disposition. This row tracks handoff only; candidate detail and acceptance stay in Taproot, without inheriting the kernel roadmap. | [Method ownership](docs/PROJECT_CONTROL_SURFACE.md#supporting-evidence-and-session-state) |
| Kernel | KERNEL-03 | Atomic Safe-Stop entry | paused | unreviewed | Specify halt/receipt failure outcomes and restart proof before implementation. | [Entry finding](docs/KERNEL_FINDINGS.md#atomic-safe-stop-entry) |
| Kernel | KERNEL-04 | OATH duration enforcement and coercion semantics | paused | unreviewed | Decide expiry semantics and restoration obligations; keep coercion-warning semantics distinct. | [Consent finding](docs/KERNEL_FINDINGS.md#oath-consent-duration-and-coercion-semantics) |
| Kernel | KERNEL-05 | Seat load-bearing audit | paused | unreviewed | Map each seat's unique invariant to active callers and behavioral proof; decide unused-route disposition. | [Seat audit](docs/KERNEL_FINDINGS.md#seat-load-bearing-audit) |
| Kernel | KERNEL-06 | Identity and propagation cluster | paused | unreviewed | Scope caller authentication, actor/request binding, and wrapper/worker propagation separately; recovery design precedes keys. | [Ingress](docs/KERNEL_FINDINGS.md#caller-identity-and-ingress-boundary), [worker context](docs/KERNEL_FINDINGS.md#thread-and-worker-context-propagation), [recovery](docs/KERNEL_FINDINGS.md#t-0-recovery-and-lock-out-before-keys) |
| Build system | BUILD-02 | Owned temporary-file lifecycle | paused | unreviewed | Scope cleanup/failure-path proof; legacy removal requires separate preservation approval. | [Testing findings](docs/TESTING.md#build-system-findings) |
| Build system | BUILD-03 | Windows entrypoints and scan boundaries | paused | unreviewed | Preserve Python automation; scope shell, encoding, external-launcher and scratch-scan work. | [Testing findings](docs/TESTING.md#build-system-findings) |

State and Evidence are independent. State is `active` (work underway), `paused`
(deferred by decision, resumable when chosen), `blocked` (awaiting an external
condition or approval), or `closed` (scoped work complete with disposition).
Evidence describes this implementation slice: `unreviewed`, `reviewed`
(independently accepted), `checkpointed` (committed), or `landed` (integrated into
the approved destination). Finding/design review is not implementation review.
Checkpointed does not mean pushed, promoted, or released; landed is not a tag.
Closed/checkpointed work can still owe full-gate acceptance: see Release Boundary.

Queue upkeep:

- Record each verified finding once with Task ID, workstream, state, evidence,
  next action, and detail link. Keep one implementation slice active.
- Workstream is the primary goal, not the edited files: `Kernel` or `Build system`,
  never bare `Build`. The Build posture is unchanged. Task IDs are references,
  not filenames; `PACT-nn` is reserved within Kernel. No phase or existing ID is renumbered.
- Insert new rows above the resume point unless the human controller directs
  otherwise. Insertion records priority, not implementation authority.
- Reprioritize by moving existing rows, not renumbering IDs or making a new list.
  Add a row only for distinct work; update affected dependencies in Next action.
  A new finding does not automatically reorder unrelated work or reopen closed work.
- Link closure evidence before removing a completed row. Exact session/tree
  state belongs in the ignored handoff, not another backlog.
- The table is read-whole. If it exceeds one screen or needs filtering (~20 rows),
  first archive closed rows and route deferred rows to the inventory. Only if
  still necessary, generate a view from this queue; no authoritative spreadsheet.
- Merge documents answering the same question; keep different questions separate.
  Follow the [per-pass update ceiling](docs/PROJECT_CONTROL_SURFACE.md#per-pass-update-ceiling).

Runtime-data safety remains binding. Check the filesystem, not only Git:
default database/sidecar files are ignored. Launcher/baseline preflight refuses
existing entries. Priority never authorizes data deletion or unsafe commands.

## Current Snapshot

KERNEL-02 baseline reproduced during build and independent review, not re-measured
by the checkpoint. This does not discharge accumulated promotion-readiness obligations:

- Canonical acceptance: **181 test functions / 3013 assertions / 0 failures**
- Coverage: **92.7% statement coverage**
- Claim matrix: **181 claims / 181 tests / 125 Pact sections**
- Source package: **26 kernel modules**, plus the CLI entry point

The [Truth Register](TRUTH_REGISTER.md) owns capabilities and non-claims.
[Testing](docs/TESTING.md) owns commands and their mutation/cleanup limits;
[Coverage Tracker](docs/roadmap/COVERAGE_TRACKER.md) owns module measurements.
Deterministic adapter proof is not live-model usefulness or deployment proof.
Partial and historical observations do not replace the required release gates.

### Release Boundary

At the DOCS-02 base `0b4ca43`, local annotated tag `v0.1.0` points to
`3bde3c1`, an ancestor 62 commits before that base. Both `v0.1.0` and
`v0.1.0-rc.1` remain unchanged. This is local Git evidence only: no hosted-release
or remote-state assertion. Genesis is the current planning posture, with versioning
deferred under the [version-clock clarification](docs/VERSIONING.md).
It does not change Section 0's Genesis hash or bypass an amendment ceremony.

Completed rows have left the rolling queue, not the acceptance obligations.
They are checkpointed locally, not full-gate accepted, not merged to main, and
not released as this staging line:

- DOCS-01 — [queue/ownership receipt](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-09-docs-01-documentation-candidate).
- BUILD-04 — [authored-history protection receipt](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-10-build-04-archive-history-protection-candidate).
- KERNEL-01 — [bounded broker checkpoint](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-10-kernel-01-reviewed-local-checkpoint).
- BUILD-01 — [coverage-launcher checkpoint](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-10-build-01-reviewed-local-checkpoint).
- DOCS-02 — closed/checkpointed; [reviewed roadmap checkpoint](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-12-docs-02-reviewed-local-checkpoint).

Additional reviewed local checkpoint: KERNEL-02 is closed/checkpointed after
its bounded candidate gates and independent review; see the
[review disposition](docs/roadmap/ACCEPTANCE_HISTORY.md#2026-09-12-kernel-02-reviewed-local-checkpoint).
It is not integrated into main or released and does not discharge BUILD-05.

Keep these stages distinct: local checkpoint records the candidate; reproduced
proof records particular executed checks; full-gate acceptance requires the
complete applicable gate set; main integration is a separate approved Git action;
a tagged release is a further deliberate version/release disposition.
A past tag does not certify later staging commits. Individual green runs do not
close the full-gate obligation. No promotion, retag, push, or release is authorized here.

Before the current line is promoted or released, obtain safe current acceptance,
coverage, claim-matrix/baseline, reverse-map, Project-Status and public-hygiene
evidence, plus the declared demo/reviewer handoff and cold-verifier evidence.
Preserve explicit non-claims and inspect main/staging content before integration.
The [build discipline](docs/BUILD_DISCIPLINE.md) owns that workflow.
Historical rc.1 exit criteria and measurements are retained in the
[Phase Ledger](docs/roadmap/PHASE_LEDGER.md#docs-02-historical-carry-forward).

## Planned / Deferred Inventory

Ordered by subject, not priority. This is not a second queue or a release
commitment. Existing phase/version names identify proposals and history, not
current scheduling. Selection happens only in Current Build Thread.
Each named survivor below retains distinct requirements; a topic merge is not
permission to drop one. The kernel remains the main work, even where its owner
is a design or testing document.

### Authority, Consent, and Recovery

- Caller authentication and actor/request authority binding:
  [ingress finding](docs/KERNEL_FINDINGS.md#caller-identity-and-ingress-boundary).
  Wrapper identity propagation and ASGI/worker/job/tool context are separate
  [dispatch obligations](docs/KERNEL_FINDINGS.md#thread-and-worker-context-propagation).
- Mechanical T-0 authority, subordinate operational credentials, and recovery
  before key dependence: [recovery finding](docs/KERNEL_FINDINGS.md#t-0-recovery-and-lock-out-before-keys).
  Seat/container reserved powers remain in [Pact alignment](docs/PACT_ALIGNMENT.md#known-alignment-gaps).
- Consent expiry versus metadata-only policy, coercion-warning semantics, and
  [dual-failure audit evidence](docs/KERNEL_FINDINGS.md#oath-audit-dual-failure-gap)
  remain distinct from current keyword flags and durable-mutation refusal.
- Lossless consent/Hub restoration, tuple uniqueness and broader state/TRACE
  coupling: [persistence detail](docs/PACT_ALIGNMENT.md#retained-persistence-and-authority-detail).
  Conditional parent/child consent inheritance belongs to [tenant detail](docs/PACT_ALIGNMENT.md#retained-tenant-and-seat-detail);
  runtime/TRACE consent-source exposure remains in [alignment gaps](docs/PACT_ALIGNMENT.md#known-alignment-gaps).

### Execution, Streams, and Context

- Universal runtime/tool-call broker enforcement, actor-bound leases and contained
  workers: [Action Plane](docs/ACTION_PLANE.md#lifecycle-boundary). The current
  local broker does not itself execute external effects.
- [Observable stream gate](docs/KERNEL_FINDINGS.md#observable-stream-enforcement)
  and [Runtime Obligation Ledger](docs/KERNEL_FINDINGS.md#runtime-obligation-ledger)
  retain before-release buffering, metering, interruption and continuing duties.
- Connector-IPI matrix is consolidated under
  [import/PAV requirements](docs/PACT_ALIGNMENT.md#retained-import-and-pav-detail):
  hidden/metadata payloads, structured authority spoofing, and poisoned/malformed/
  oversized shadow connectors stay distinct acceptance requirements.
- Structured PAV trust metadata/filters and least-context ceilings, plus CYCLE
  retry/burst/denied-action and execution/token/cost budgets, use that same
  detail owner. Live usefulness evaluation remains distinct from safety fixtures.

### Meaning, Seats, and Tenant Policy

- [RUNE scale/lifecycle](docs/KERNEL_FINDINGS.md#rune-registry-scale),
  [namespace/confidence policy](docs/KERNEL_FINDINGS.md#rune-pack-namespaces-and-synonym-confidence),
  and [Unicode/confusable handling](docs/KERNEL_FINDINGS.md#rune-unicode-and-confusable-normalization)
  are three findings, not one generic vocabulary task.
- Governed pack/version selection and tighten-only tenant/domain overlays:
  [tenant detail](docs/PACT_ALIGNMENT.md#retained-tenant-and-seat-detail).
  Tenant worlds may differ; the global Pact cannot be forked or loosened.
- Seat load-bearing proof, enforced-versus-declared permission mapping and WARD
  hook coverage for future fields remain in that owner and the seat finding.
  Genesis-path clarity and the execution placeholder's wire-or-retire decision
  belong to [persistence/authority detail](docs/PACT_ALIGNMENT.md#retained-persistence-and-authority-detail).

### Audit, Pact, and External Proof

- Atomic Safe-Stop entry stays separate from proven atomic clearing.
  Full-Pact integrity and pre-seal checks, lossless persistence, and store-local
  purge limits remain [alignment work](docs/PACT_ALIGNMENT.md#retained-persistence-and-authority-detail).
- Signed exports, timestamps/off-box rollback detection, canonical privacy-safe
  payload material, independent recomputation, cross-machine cold proof,
  large-event characterization, and chain-version migration use the named survivor
  [external-proof detail](docs/PACT_ALIGNMENT.md#retained-external-proof-detail).
- Guarded Sections 1-7 canon export is built; Section 0 still requires re-anchoring
  and boot/tamper/recovery proof. Preserve the
  [canon-export proposal](docs/proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md) and
  [amendment plan](docs/proposals/V0_1_1_AMENDMENT_PLAN.md): Option B's first
  ceremony stays Sections 1, 3, and 6, not a broad Section 0 rewrite.
- Reviewer identity/quorum, richer amendment diff/evidence, stale-base handling,
  ratification preview and post-ratification proof:
  [ceremony gaps](docs/PACT_ALIGNMENT.md#known-alignment-gaps).
  Pact splitting is deferred to the Section 7 ceremony; no Pact text changes here.
- Retain the ledger's low-priority verifier-return consistency and Hub collision
  behavior observations through [persistence detail](docs/PACT_ALIGNMENT.md#retained-persistence-and-authority-detail).

### Operator, Advisor, and Deployment Surfaces

- The [three-window proposal](docs/proposals/THREE_WINDOW_GOVERNANCE_MODEL.md)
  owns before/during/after boundaries; during means observable output, not thought.
- Tier 2.5 advisors remain non-authoritative, with typed evidence packets before
  implementation. Agency never grants authority. Graduated false-halt reduction,
  amendment/code-review advice and TECTON operator views remain
  [operator/advisor detail](docs/PACT_ALIGNMENT.md#retained-operator-and-advisor-detail).
- Sigil universality has one survivor, the [Sigil proposal](docs/proposals/SIGIL_SET_PROPOSAL.md);
  acceptance would require coordinated Section 0 re-anchor, references, presentation
  and proof, not a cosmetic swap.
- Cross-OS proof has one survivor,
  [Testing's cross-OS contract](docs/TESTING.md#future-cross-os-proof):
  Windows-local evidence is not Linux/Android/macOS proof. Linux comes first;
  Android is an adapter/action-surface testbed, not a kernel port.
- Multi-process/distributed audit throughput, runner JSON verdict/CI hooks, and
  proof-surface inventory remain [deployment detail](docs/PACT_ALIGNMENT.md#retained-deployment-and-proof-detail).
  These do not authorize BUILD-02/03 or change the single-process claim.
- Public vocabulary/maps, operator truth, 30/60/90 demo routes and honest artifacts
  remain [operator detail](docs/PACT_ALIGNMENT.md#retained-operator-and-advisor-detail).
  Governance integrity precedes demo quality; cosmetic/package reshuffles are not priorities.

## History, Detail, and Limits

[Phase Ledger](docs/roadmap/PHASE_LEDGER.md) preserves Phase A-H and later evidence.
Its old “Still open” lists are historical observations routed through the owners
above, not another work order. CLOSED-prefixed duplicate retirement is proposed
only; records remain preserved pending human approval.

[Acceptance History](docs/roadmap/ACCEPTANCE_HISTORY.md) owns dated receipts;
[Threat Model](THREAT_MODEL.md#retained-boundaries-from-roadmap) owns retained risk
boundaries; [Truth Register](TRUTH_REGISTER.md#retained-non-claims-from-roadmap)
owns the corresponding non-claims. Neither risk visibility nor a moved item implies
closure. Kernel findings own evidence/consequence/closure criteria, not scheduling.

Generated claim/reverse maps and Project Status remain generated evidence, not
authored queues. [Document ownership](docs/PROJECT_CONTROL_SURFACE.md) controls
maintenance and routing; [Docs Index](docs/DOCS_INDEX.md) is the reading directory.
The temporary old-to-new map is review evidence in the ignored handoff's external
evidence location, not a new permanent migration registry.

RSS remains a runnable governance reference kernel, not a production deployment,
universal connector sandbox, distributed system, or claim of non-repudiation.
Build ambitiously; describe only what the evidence supports.
