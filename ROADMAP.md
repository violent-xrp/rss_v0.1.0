# RSS v0.1.0 — Roadmap

_Licensed under AGPLv3; see `LICENSE/README.md`._

Release target: **v0.1.0**

Current release candidate: **v0.1.0-rc.1** is tagged and pushed at `c694b83`.

Versioning posture:
- canonical model: `docs/VERSIONING.md`
- project/release versions use semver (`0.1.0`, `0.1.1`, `0.2.0`) for code and release boundaries
- `-rc.N` means release-candidate iteration toward the target version only; it does not track Pact edits or code significance
- Pact section versions increment internally through the Section 7 amendment ceremony and Section 0.10.4; a sealed Pact amendment surfaces as a project MINOR bump, never in the `-rc.N` suffix
- keep `main` moving through hardening commits between release boundaries without treating every commit as a version event

This is the current command document for RSS. It should answer four questions quickly:
- what is true now
- what is active now
- what must happen before the next release checkpoint
- what must stay visible without blocking the current work

Historical receipts live in supporting docs:
- acceptance history: `docs/roadmap/ACCEPTANCE_HISTORY.md`
- phase ledger and landed work: `docs/roadmap/PHASE_LEDGER.md`
- coverage tracker: `docs/roadmap/COVERAGE_TRACKER.md`
- testing layout and runner discipline: `docs/TESTING.md`
- versioning model: `docs/VERSIONING.md`
- demo handoff and artifact usage: `docs/demo/DEMO_HANDOFF.md`
- external vocabulary / reviewer map: `docs/EXTERNAL_MAP.md`
- documentation map: `docs/README.md`
- NIST AI RMF reviewer map: `docs/NIST_AI_RMF_MAPPING.md`
- future action-plane design boundary: `docs/ACTION_PLANE.md`
- active design proposals: `docs/proposals/`
- Pact-to-kernel alignment map: `docs/PACT_ALIGNMENT.md`
- claim traceability: `docs/claim_matrix.md`

---

## Current Snapshot

Current code state:
- **163 test functions / 1500 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **91.9% statement coverage** via `python run_coverage.py`
- **163 claims / 163 tests / 115 Pact sections** in `docs/claim_matrix.md`
- **24 kernel modules** in the `src/rss/` package tree plus `src/main.py`
- current phase: **Phase G — demo/operator experience and coverage polish**

Current posture:
- public-alpha hardening is materially beyond the earlier 111/850 baseline
- the acceptance harness is the single local truth command
- public docs are synced to the current 163/1500 baseline
- the Phase G coverage floor is closed; the project is now polishing the demo handoff and release boundary, not inflating claims

Canonical local truth-run:
```bash
python tests/test_all.py
```

Optional local checks:
```bash
python run_coverage.py
python docs/build_claim_matrix.py
python docs/sync_baseline.py --check --require-clean
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Note: on the current Windows environment, `pytest` is not installed / not on PATH. `pytest` parity is optional tooling, not the source of truth.

---

## Active Focus

### Now
- **Release-boundary polish:** keep the v0.1.0 claim surface aligned with the closed Phase G coverage floor and remaining known limits.
- **Connector-proof planning:** keep future browser/email/document/RAG/tool-return import tests mapped before adding real external adapters.
- **Framework-facing reviewer map:** keep `docs/NIST_AI_RMF_MAPPING.md` aligned with the current proof surface so RSS can be explained in recognized AI risk-management language without claiming certification or production compliance.
- **Pre-tag RUNE/OATH hardening map:** closed. OATH requester fallback, RUNE constraint-prompt proof, and RUNE longest bounded-match precedence are now proven.
- **RUNE embedded disallowed scan:** closed as a code helper. RUNE can now audit longer payload strings for bounded disallowed terms via `scan_disallowed()` while preserving `classify()` exact-match semantics. The side-effect broker that will consume this helper remains future action-plane work.
- **Pact cleanup checkpoint:** the section-by-section Pact cleanup (Sections 0-7) is landed and pushed. Future Pact text changes move through the v0.1.1 amendment ceremony unless a release-gate review proves v0.1.0 would otherwise be false.
- **Code-first Pact posture:** let kernel hardening move where it makes RSS more true; keep Pact edits section-bounded, reviewed, and version-sensitive so cleanup does not bundle unrelated lanes.

### Next
- CLOSED: Sections 1-7 cleanup landed after Section 0; implementation-reference drift, CYCLE load wording, S5/S6 concurrency and persistence boundaries, and S7 amendment-persistence wording now match the current kernel truth.
- CLOSED FOR `v0.1.0-rc.1`: final acceptance, sync, claim-matrix, and offline demo gates passed before the tag. The ignored local demo bundle reports `PASS`, 22/22 successful task IDs bound to TRACE, 14/14 expected evidence markers found, and cold verification over 192 events. Rerun the gates before final `v0.1.0`.
- Demo proof artifacts now need to stay evidence-bound: PASS requires expected seeded evidence markers and successful task IDs bound to TRACE, not just fluent non-error answers.
- `v0.1.0-rc.1` is the current reviewable release candidate; the next release decision is whether this candidate can converge to final `v0.1.0` or needs another candidate iteration.
- Keep final v0.1.0 gates explicit: final acceptance proof, synced public docs, fresh demo artifacts, and no release claim beyond the current proof surface.
- Keep tightening the 30/60/90-minute reviewer path around governed useful retrieval, refusal, isolation, recovery, cold verification, and artifact inspection.
- Keep the zero-trust trajectory explicit without overclaiming v0.1.0: RSS is moving toward deployment-grade zero-trust through caller identity, per-action gates, least-privilege context, and external audit anchoring, but the current release remains a single-process governance kernel.
- Pact cleanup is complete for the current pass; keep public proof docs synced as code hardening and release-boundary polish continue.

### Post-rc.1 / Toward v0.1.1
- **Amendment mechanics:** Section 7 ceremony persists sealed canon in SQLite. A guarded Sections 1-7 canon-to-file exporter now lives in `rss.audit.pact_canon_export`; Section 0 export remains a separate Genesis-aware future path captured in `docs/proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md`.
- **Pact/canon drift detection:** a read-only diagnostic compares each Pact file hash to any sealed DB canon hash and reports no-canon-yet, in-sync, file-ahead, or canon-ahead states. The Sections 1-7 exporter can now close canon-ahead states when the file base is verified; Section 0 remains outside the common exporter.
- **Section 0 lock-out path:** Section 1-7 file export is the safe common path. Section 0 export is special because it is Genesis-anchored; any Section 0 file write must pair with Genesis re-anchor plus boot, tamper, and recovery verification or the runtime will Safe-Stop.
- **T-0 identity seam:** the `authorize_t0(action, context)` chokepoint now centralizes current soft sovereign-command gates for Safe-Stop clearing, SEAL authority checks, and runtime RUNE vocabulary mutations. Cryptographic/mechanical identity enforcement remains future work.
- **Recovery before keys:** cryptographic identity must be designed recovery-first. Keys may strengthen attestation, but they must not become the only way T-0 can recover lawful authority under Section 0.1.4.
- **Operational identity:** future TECTON deployment users should carry operational credentials and role scopes separate from, subordinate to, and unable to amend constitutional T-0 authority. Key rotation, revocation, and recovery are governed/audited events; keys do not belong in repo, Pact text, or TRACE payloads.
- **Action-proposal loop:** v0.1.0 is a single forward pass: model output is sanitized and logged, but it does not re-enter the gates. The v0.1.1+ frontier is a typed action proposal and side-effect broker where every proposed side effect re-enters SCOPE, RUNE, execution validation, OATH, and CYCLE before execution. The future design boundary is captured in `docs/ACTION_PLANE.md`.
- **Three-window governance model:** future architecture is organized as before model exposure, during observable output generation, and after output when proposed actions re-enter governance. This is a planning model in `docs/proposals/THREE_WINDOW_GOVERNANCE_MODEL.md`, not a claim that RSS observes hidden model thinking.
- **Cross-OS proof harness:** Windows is the current primary proof environment. Linux should be the first cross-OS CI target for the canonical runner, public hygiene, reverse map, cold verification, and file-write/export paths. Android remains an adapter/action-surface testbed, not a kernel port; macOS follows later.
- **Tier 2.5 advisor layer:** future internal advisors may assess, narrow, and recommend through structured packets, including amendment/code consistency review. They remain non-authoritative: automate assessment, never authorization.
- **Sigil universality:** `docs/proposals/SIGIL_SET_PROPOSAL.md` remains the public design surface for encoding-stable sigils and authority-marker caveats. No glyph change is built or claimed in v0.1.0.

### Keep Warm
- API/wrapper ingress boundary and caller identity propagation.
- Per-action/tool-call enforcement before real side effects execute.
- Observable stream enforcement before release of generated output: buffer streamed chunks, meter token/byte/cost estimates, halt on governed violations, and emit completion/halt receipts without claiming hidden-reasoning visibility.
- Structured Action Proposals: LLM output becomes a typed proposed task that must re-enter SCOPE, RUNE, Execution, OATH, and CYCLE before any side-effect broker acts. See `docs/ACTION_PLANE.md` for the planning-only boundary.
- Minimum proposal shape to evaluate later: `proposal_id`, `source_task_id`, `action_class`, `target_resource`, `payload`, `container_id`, `proposed_at`, and a payload hash/TTL binding. The broker boundary must emit proposal, rejection, authorization, and execution receipts before any external file, API, network, or tool side effect.
- Runtime Obligation Ledger: future live record of active leases, container bindings, consent source, budget, result-import requirement, verification requirement, and TRACE obligations after authorization.
- Cryptographic/mechanical T-0 identity gate for Safe-Stop clearing beyond the current soft `t0_command=True` fence.
- Zero-trust hardening sequence: authenticated ingress, actor-bound request context, capability-scoped side-effect broker, per-action/tool-call authorization, signed TRACE exports, external timestamp anchoring, and auditable recovery/bypass paths.
- Cross-OS proof: treat OS differences as proof surfaces, not assumptions. Windows is proven locally; Linux CI is the first portability target; Android belongs to adapter proof; macOS is a later completeness target.
- OATH duration policy and stronger coercion-warning semantics; the current urgency-word helper is now honestly named as keyword-limited, not coercion detection.
- RUNE scale path: current classification and embedded disallowed scanning are linear in active registry size and scan the global registry. Large-vocabulary support needs namespaced active registry partitions, a compiled multi-pattern matcher, and archived terms kept out of the hot path before RSS claims large-pack performance.
- RUNE per-pack/domain term and synonym namespaces plus v0.1.1 synonym confidence semantics. MED and LOW currently collapse to AMBIGUOUS, so distinct confirmation-state behavior must be designed and tested before RSS claims it.
- TECTON policy overlays: per-tenant overlays may tighten scope, terms, permissions, consent, and domain packs, but may not loosen or fork the global constitutional floor.
- Sigil universality proposal: current seat sigils are encoding-unstable and mostly latent. `docs/proposals/SIGIL_SET_PROPOSAL.md` tracks candidate replacement sets, ASCII fallback, authority-marker caveats, and the v0.1.1 amendment/re-anchor migration map.
- Tier 2.5 internal advisor design: future advisors should reduce false-positive halts through graduated response (`SERVE` / `NARROW` / `ESCALATE` / `HALT`) while staying below the authority line. Principle: automate assessment, never authorization.
- Agent terminology amendment candidate: an agentic system remains Tier 3 even when it has a loop and tool access. Agency is not authorization; any proposed side effect must re-enter governance before execution.
- CLOSED: Seat interface decision for SCOPE/RUNE resolved by adding WARD-compatible adapters while preserving direct runtime request-path calls.
- WARD hook protected-field audit as governance-relevant task/result fields grow.
- CLOSED: CYCLE fail-closed proof now covers internal runtime-stage exceptions as `UNEXPECTED_ERROR` at Stage 6, in addition to strict-mode unknown-domain rejection.
- CLOSED: SEAL external attribution scanner now blocks generic external-advisor/model authorship and authority-attribution phrases, including common verb/preposition/actor evasions, while still allowing bare non-authority mentions.
- Governed pack selection/versioning once multiple demo worlds or tenant-specific packs exist.
- Runner JSON verdict export for independent tooling / CI cross-checks.
- External vocabulary map maintenance as reviewer-facing language evolves.
- Pact alignment map maintenance before Pact wording, v0.1.1, or v0.2.0 changes.
- Section-ordered Pact amendment plan before the v0.1.1 ceremony: `docs/proposals/V0_1_1_AMENDMENT_PLAN.md`. Canon-to-file export sequencing is captured in `docs/proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md`. `docs/PACT_ALIGNMENT.md` remains the inventory, not the execution order.
- Seat load-bearing audit after v0.1.0.
- T-0 recovery/lock-out design before cryptographic identity becomes load-bearing.
- CLOSED: reverse Pact-code map now lives at `docs/pact_code_map.md`, generated by `docs/build_pact_code_map.py` and checked by public hygiene. Full-Pact hash/integrity enforcement remains future hardening.

### Future Watch
- indirect prompt-injection probes against imported web, email, document, RAG, and tool-return content
- structured PAV trust metadata beyond content-string markers
- structured authority spoof tests for imported JSON/YAML/tool-return text
- connector-specific IPI acceptance matrix for PDF, HTML, email, RAG chunks, tool returns, and Unicode invisibles/confusables
- external signing and timestamp anchoring
- cross-machine audit portability
- confusables/homoglyph hardening beyond current normalization
- larger-event-count TRACE verification characterization
- payload-inclusive TRACE export / recomputable envelope verification so third-party cold verifiers can validate event hashes from canonical exported material, not only parent-link continuity; design must preserve REDLINE/privacy boundaries, version the proof envelope, define whether payload material lives in a sovereign-only sidecar/receipt bundle, and stay future-work until the verifier can recompute hashes from exported material
- product/operator console structure that does not outrun kernel truth
- internal advisor layer design: structured, auditable, non-authoritative advisors between external models and the kernel/operator, primarily to reduce false-positive halts through graduated response rather than to grant authority
- advisory packet contract before advisor execution: typed evidence, concern kind, severity, proposed response class (`SERVE` / `NARROW` / `ESCALATE` / `HALT`), source-advisor attribution, packet hash, authority set to none, and TRACE-recorded invocation/output
- advise-to-act boundary: internal or personal advisor modules may read and advise, but may not mutate state, approve, call tools, or execute side effects until Structured Action Proposals, broker gates, and capability leases exist
- agent vocabulary binding: future Pact wording should state that agentic loops and tool access do not create authority; agency is not authorization
- sigil authority-marker design: future model-facing sigils are only meaningful if backed by kernel-only envelopes, nonce/hash binding, or equivalent structural proof; a bare glyph in a prompt is not security

Do not diffuse effort equally across all future phases. Keep the current checkpoint sharp.

---

## v0.1.0 Final Scope Split

The release standard is **safe to evolve**, not complete forever. A v0.1.0 item
belongs on this side of the tag only if it must exist before RSS can trust its
own release or amendment path. Default destination for everything else is the
v0.1.1 ceremony queue.

Completed for `v0.1.0-rc.1`:
- CLOSED: S0-S2 mechanical OATH/RUNE hardening is proven: OATH requester
  fallback closed, RUNE constraint-prompt exclusion proven, and longest
  bounded-match precedence implemented.
- CLOSED: Section 3 verification audits are resolved in code. HIGH_RISK
  classification wins over CONSTITUTIONAL when both appear, payload hashes are
  re-verified during intent validation, and externally constructed far-future
  TTLs are rejected.
- CLOSED: cold verifier full-chain head truncation detection is implemented and
  tested; filtered container views still allow a non-null first parent hash.
- CLOSED: stale top-level `src/pav.py` and `src/reference_pack.py` shims are
  removed, with no bare-module imports remaining.
- CLOSED: README architectural thesis language is in project voice rather than
  first-person reviewer commentary.
- CLOSED: Section 7 proposal attribution and ceremony write-ahead hardening are
  code-proven. Proposal-time external attribution creates no actionable state,
  and proposal/review/ratification mutation fails closed if TRACE emission
  fails.
- CLOSED: Section 7 amendment persistence is implemented and code-proven.
  Proposal objects, review state, ratified amendment records, reconstructed
  canon state, and queryable amendment history survive restart. Persistence
  failure leaves proposal/canon/history state unchanged after the failed step.
- CLOSED: Section 0 §0.8.4 governed-state bootstrap round-trip is proven in
  acceptance. Terms, synonyms, disallowed terms, hub entries, consent records,
  TRACE events, container state, container hub entries, Safe-Stop/system state,
  and schema version restore after restart. Container state proof uses the
  current explicit TECTON `save_to(...)` persistence path.
- CLOSED: Section 0 voice cleanup landed and was pushed in `0c9539a`. The
  pass includes the constitutional T-0 vs product operational ownership
  distinction, Pact-level recovery authority clause, internal advisor fence,
  Section Scope cleanup, and Genesis re-anchor. Council vocabulary is preserved
  verbatim in this pass; Section 0 vocabulary is deferred to a dedicated
  Genesis-aware ceremony, not the first Option B v0.1.1 amendment.
- CLOSED: `docs/PACT_VOICE.md` served as the non-authoritative rail for the
  section-by-section Pact cleanup.
- CLOSED: Section 0-7 cleanup landed with the Section 4 and Section 5
  "rule / current proof / boundary" style. Substantive additions such as T-0
  recovery authority remained T-0-owned rather than implementation cleanup.
- CLOSED: final rc.1 acceptance/sync pass was clean at 145 tests, 1312
  assertions, 0 failures, and 92.2% coverage. Rerun the same gates before
  final `v0.1.0`.
- CLOSED: demo artifact decision is made for `v0.1.0-rc.1`: do not rely on a
  stale artifact bundle. Fresh offline artifacts were generated before the
  checkpoint with summary `PASS`, 22/22 TRACE-bound successful task IDs, 14/14
  expected evidence markers, refusal/isolation/recovery flags, live TRACE
  validity, cold TRACE verification, and 192 cold events. Regenerate before
  final `v0.1.0`.

Mandatory before final `v0.1.0`:
- CLOSED: T-0 recovery authority is now carried in Section 0. Later sections
  may add cross-references during v0.1.1 cleanup, but v0.1.0 no longer depends
  on a separate recovery-authority drafting item.
- Final acceptance/sync/claim-matrix pass before final tag.
- Fresh offline demo artifact bundle before final tag.

Held for v0.1.1 ceremony unless a release-gate review proves otherwise:
- broad Pact wording cleanup and Council/vocabulary sweep
- Option B Council/register cleanup as the first v0.1.1 amendment ceremony test
  case: Sections 1, 3, and 6 only. This replaces or narrows "Council" language
  where current code already supports the clearer wording, while leaving Section
  0 untouched for a later Genesis-aware ceremony with re-anchor proof. It
  exercises amendment persistence and ceremony machinery with bounded, low-risk
  scope before larger v0.1.1 candidates run through ceremony.
- full-Pact integrity extension beyond the current Section 0 Genesis anchor
- RUNE large-vocabulary hardening: namespace the active registry by pack/domain/container, replace global linear scans with a compiled multi-pattern matcher, and add active/archive lifecycle so retired terms leave the hot classifier path
- tighten-only TECTON policy overlays for tenant/domain customization without tenant constitutional deltas
- CLOSED: generated `docs/pact_code_map.md` reverse map from code references back to Pact sections, kept separate from generated `docs/claim_matrix.md` and hand-authored `docs/PACT_ALIGNMENT.md`
- internal advisor layer / multi-voice amendment design
- TECTON product UI and operator-surface design
- accumulated section-level Pact refinements. `docs/PACT_ALIGNMENT.md` is the
  canonical candidate inventory; ROADMAP tracks sequencing, not the full text
  queue.

---

## v0.1.0 Exit Criteria

Before tagging final v0.1.0, RSS should have:
- one clean acceptance run at the current or higher assertion count
- current coverage and claim matrix regenerated
- `python docs/sync_baseline.py --check --require-clean` exits 0, proving current-facing baseline docs are synced, the runner is clean, and coverage proof reproduced
- demo artifact flow documented and runnable
- remaining known limitations disclosed clearly
- no public claim that exceeds the current proof surface

Phase G should close when:
- every package module is at or above 85% coverage, or a documented exception is accepted (**met: current floor is >=85%**)
- the demo handoff artifacts are documented well enough for an outside engineer to inspect
- the current release/non-goal boundary is clear

v0.1.0 does **not** require:
- deployment-layer cryptographic caller identity
- universal per-action/tool-call enforcement
- full wrapper/API maturity
- external signing or timestamp anchoring
- distributed multi-node TECTON
- polished end-user product UX
- broad Pact rewrite, vocabulary sweep, internal advisor layer, or product UI work

---

## Current Release Truth

### Safe Claims Now
RSS v0.1.0 can be presented as:
- a domain-agnostic, application-layer governance kernel with a zero-trust trajectory
- a constitutional middleware architecture with typed seat authority separation
- a pre-model governance pipeline
- a system with scoped data access, bounded advisory exposure, and governed consent
- a system with hash-chained TRACE and stand-alone cold verification
- a system with persistent Safe-Stop
- a system whose acceptance harness produces a truthful single summary verdict
- a system with a governed offline fallback that summarizes only scoped data
- a system with a kernel-level untrusted-content import boundary that marks external evidence as data-only before advisory use
- a system with a deterministic governed demo walkthrough proving useful retrieval, refusal, isolation, recovery, and cold verification
- an honest alpha/MVP

### Unsafe Claims Now
RSS v0.1.0 should not yet be described as:
- fully async-safe in all wrappers
- per-action/tool-call enforced for every future side effect
- distributed
- cryptographically immutable
- enterprise-complete
- a full deployment-layer zero-trust stack
- a complete zero-trust implementation
- a production-ready end-user application
- a polished natural-feeling offline assistant experience
- cryptographically authenticated at ingress
- proven safe for every future browser, email, document, RAG, or tool-return connector without connector-specific tests
- able to let imported content grant authority, expand scope, or authorize side effects

---

## Current Phase Plan

### Phase G — Demo / Operator Experience

Landed:
- live demo-suite default with deterministic `--offline` proof mode
- normal advisor lane with SYSTEM-only scope so ordinary conversation does not open project/private data
- interactive `src/main.py demo` routing for normal chat vs seeded-data questions
- cross-domain demo packs for construction, legal, medical, and finance
- explicit entry metadata with non-REDLINE PERSONAL and explicit PERSONAL/REDLINE rows
- demo/reference-pack validation that fails loud before runtime seeding mutates state
- PAV now honors `forbidden_sources` during advisory-view construction
- indirect prompt-injection proof for poisoned retrieved content as scoped data, not authority
- `save_untrusted_content()` import boundary for future browser/email/document/RAG/tool connectors
- untrusted import receipt hardening: source content SHA-256, wrapped content SHA-256, byte lengths, provenance persistence, TRACE payload binding, and mutation detection
- OATH routed `authorize` now fails closed when `requester` is missing or blank instead of defaulting to T-0; proof verifies no consent record is created and explicit requester flow still works
- RUNE contextual reinjection now has capture-adapter proof that sealed-term constraints remain kernel metadata and are excluded from advisor prompt text
- RUNE primary substring classification now prefers the longest bounded sealed-term match so registration order cannot make a shorter term outrank a more specific phrase
- stale top-level duplicate modules `src/pav.py` and `src/reference_pack.py` removed; canonical code now lives under `src/rss/`
- cold TRACE verifier now fails full-chain verification when the first surviving row still has a parent hash, detecting head truncation while preserving filtered container-view semantics
- `_validate_llm_response()` now documents that response scanning is downstream sanitation, while SCOPE/PAV/OATH remain the authoritative upstream boundary
- Section 3 execution validation now re-hashes `ExecutionIntent.raw_text` before execution and rejects far-future TTLs on externally constructed intents
- SEAL amendment proposals now reject external advisor attribution before review or ratification, so forbidden authorship claims cannot sit in actionable proposal state
- SEAL ceremony TRACE emission now fails closed when a trace callback is wired: proposal, review, and ratification do not mutate ceremony state if amendment audit emission fails
- WARD registration now fails fast when a seat lacks the standard `status()` / `handle(task)` interface, so malformed routable seats cannot enter the registry.
- Phase G coverage floor closed: `cycle.py` and `trace_verify.py` are both above 94% and every package module is at or above 85%
- demo handoff now names the 30/60/90-minute reviewer path, artifact review order, proof signals, and release boundary
- demo artifact proof now records per-question proof rows, expected governed-evidence markers, and successful task IDs bound to TRACE artifacts so useful retrieval cannot pass on fluent but ungrounded answers
- external vocabulary map added for engineers/reviewers who do not know RSS terms yet
- artifact export bundle from a single governed run:
  - `demo_report.json`
  - `demo_summary.md`
  - `demo_trace.json`

Threat-hardening note:
- **Improved now:** PAV closes the allowed/forbidden-source overlap; `save_untrusted_content()` gives future external adapters a single import path that wraps external content with `UNTRUSTED_EXTERNAL_CONTENT` and `DATA_ONLY_NOT_AUTHORITY`; import receipts now carry source/wrapped SHA-256 digests and byte lengths; TRACE records `UNTRUSTED_CONTENT_IMPORTED` with digest-bearing payload; adversarial coverage proves poisoned imported content stays data, does not mutate OATH consent, and does not expose forbidden PERSONAL/REDLINE material through the advisory path.
- **Still not proven:** RSS has not implemented real browser, email, document, RAG, or tool-return connectors. Each future connector needs hidden-text, metadata, comment, retrieved-snippet, and tool-output tests before public claims expand.

Open in Phase G:
- generate and inspect a fresh offline demo artifact bundle before the v0.1.0 tag
- live-advisor quality evaluation remains separate from proof: a governed live model can be constrained correctly and still under-answer PAV-backed questions, so future demo/product work needs a live-eval harness before claiming production-level answer quality
- keep connector-specific indirect prompt-injection probes parked as required acceptance criteria for future external adapters

### v0.1.1 Candidate Hardening Queue

These are not v0.1.0 blockers unless a release-gate review says otherwise:
- structured trust metadata in PAV entries, so `instruction_status` survives as data, not only as rendered text
- entry-level PAV trust filters by provenance/source_type/instruction_status, not only hub name
- structured authority-spoof probes: imported JSON/YAML/tool-return text cannot become consent, scope, or side-effect authorization
- connector IPI acceptance matrix for PDF metadata/hidden text, HTML hidden spans/alt text, email MIME parts, RAG neighbor chunks, tool returns, and Unicode invisible/confusable text
- shadow connector harness: fake browser/email/API/RAG/tool-return adapters that return poisoned, malformed, oversized, metadata-hidden, and authority-spoofing payloads before any live connector claims expand
- capability leases for future side-effect work: short-lived, scoped, revocable authorization objects bound to actor/request, action class, target resource, container, TTL, budget, and payload hash
- CYCLE budget/anomaly extension: prove bounded behavior for retry loops, repeated denied actions, abnormal bursts, execution-budget exhaustion, and token/cost budget exhaustion in addition to simple request cadence
- PAV token-economy constraints: define entry-count, character/token-estimate, source, and total-context ceilings so governed PAV construction remains least-context evidence rather than a trusted context dump; audit/history material should stay outside model-facing prompts unless explicitly scoped back in
- three-window governance proposal: use `docs/proposals/THREE_WINDOW_GOVERNANCE_MODEL.md` to keep before/during/after language precise; "during" means observable output stream enforcement, not hidden model-thought visibility
- runner JSON verdict export for independent verification and future CI
- Linux CI gate for `tests/test_all.py`, `docs/check_public_hygiene.py`, reverse Pact-code map freshness, cold verification, and guarded canon export behavior before claiming cross-OS proof
- live LLM evaluation harness for governed usefulness under PAV constraints: score whether live adapters answer from expected evidence markers while preserving refusal/isolation boundaries
- external-map refinement for public reviewers
- post-v0.1.0 seat load-bearing audit: verify each seat owns a unique invariant as connectors and per-action gates arrive
- RUNE registry namespace: partition active terms, synonyms, and disallowed phrases by pack/domain/container context so construction, legal, medical, finance, and tenant packs can reuse common phrases without global collisions
- RUNE classification index: replace full-registry word-boundary scans with a compiled multi-pattern matcher that is rebuilt only on registry changes and searched per relevant namespace
- RUNE term lifecycle: distinguish active and archived/retired terms so historical meaning remains auditable without keeping every retired term in the hot classification path
- RUNE synonym confidence cleanup: decide in v0.1.1 whether to collapse HIGH/MED/LOW Pact wording to the states RSS actually uses, or build distinct MED/LOW confirmation semantics with explicit returned metadata and tests
- CLOSED: OATH structured `check(detailed=True)` preserves the current string return while exposing consent source (`CONTAINER`, `GLOBAL`, `GLOBAL_FALLBACK`, `ABSENT`, `ERROR`) for audit/reviewer context.
- OATH duration decision: either enforce expiry through deterministic time semantics or document `ConsentRecord.duration` as metadata-only
- CLOSED: OATH explicit `DENIED` consent status and `deny()` operation now let a container-specific denial override GLOBAL authorization, and DENIED records survive restore/restart without being upgraded.
- CLOSED: OATH coercion wording cleanup renamed the current urgency-word check as `detect_coercion_keyword_limited()` / `keyword_flagged` while preserving a legacy wrapper; real governed coercion-warning semantics remain future work.
- OATH nested consent inheritance only if TECTON grows parent/child container hierarchy
- last-resort consent failure receipt if durable consent persistence and TRACE failure notification fail at the same time
- mechanical T-0 gate ordering for Pact-reserved powers: `authorize_t0(action, context)` now centralizes the current soft command check for Safe-Stop clearing, SEAL seal/ratification, and runtime RUNE term/synonym/disallowed mutations; seat changes, broader container lifecycle authority, and cryptographic/mechanical identity remain future hardening
- TECTON permission-enforcement map: keep `can_draft`, `can_request_seal`, `can_call_advisors`, `can_access_system_hub`, `max_requests_per_minute`, and `risk_tier` visibly split between enforced behavior and declared metadata
- CLOSED: TECTON rate-limit input validation now rejects non-positive or malformed `max_requests_per_minute` values at profile construction and mutation boundaries, while invalid legacy persisted values sanitize visibly to the default on restore.
- CLOSED at OATH API boundary: structured consent checks expose whether authorization came from container-specific consent, GLOBAL, GLOBAL fallback, absent consent, or validation error. Runtime response/TRACE surfacing remains future product work.
- Section 6 export/audit precision: keep cold verification, cold export, and future payload-inclusive external recomputability as separate claims; do not let Pact wording claim external recomputation until exported canonical proof material, privacy policy, and verifier tests exist
- Section 6 production posture evidence: keep the one-switch `production_mode` behavior visible if more settings join that profile
- Section 6 provenance proof: decide whether `UNTRUSTED_IMPORT` needs a dedicated full restore test beyond current SQLite row round-trip proof
- CLOSED: Section 6 live export sanitizer hardening now aborts JSON/text exports if REDLINE ID collection from live hubs fails, rather than producing a silently trusted export
- CLOSED: Restore visibility hardening now counts skipped persisted records in `restore_skips`, stores structured `runtime.restore_warnings`, and prints restore warnings for malformed or duplicate terms, synonyms, consents, and hub entries instead of silently swallowing them.
- CLOSED: PAV/runtime skipped-source visibility now records skipped-source metadata for forbidden sources, standard LEDGER exclusion, and hub-read failures, and runtime responses expose only the skipped-source count without leaking skipped content or exception messages.
- CLOSED: Section 7 amendment persistence now persists proposals, review state, ratified amendment records, reconstructed canon state, and queryable history across restart
- CLOSED: canonical versioning model now lives in `docs/VERSIONING.md`: project/release versions use semver, `-rc.N` is release-candidate iteration only, and Pact section versions are internal amendment records that surface through a project MINOR bump when sealed.
- Section 7 operator ceremony API: future richer diff report, stale-base UX, and post-ratification verification report for TECTON UI readiness; the guarded Sections 1-7 canon-to-file CLI exists, while Section 0 export remains future Genesis-aware work
- T-0 recovery authority: design auditable manual recovery so future cryptographic identity strengthens attestation without creating permanent lock-out risk
- Full-Pact integrity: extend hash verification and pre-seal integrity beyond Section 0
- CLOSED: reverse Pact-code map generation now reports code references by Pact section, source references without matching Pact headings, Pact sections without source refs, and governance modules without Pact refs
- CLOSED: guarded Sections 1-7 canon-to-file export now lives in `rss.audit.pact_canon_export` with dry-run default, stale-base refusal, explicit T-0 write gate, atomic writes, first-canon `--expected-file-hash`, and Section 0 refusal
- Local enforcement hooks: add pre-commit/CI checks for baseline sync, claim matrix drift, and Pact-reference extraction once the commands are stable beyond the local public-hygiene gate
- Genesis path cleanup: document or consolidate the two Genesis verification surfaces (`verify_genesis` runtime path and `load_constitution` loader path) so the canonical production path stays obvious
- Execution law placeholder cleanup: remove dead `ExecutionStateMachine.execute()` code if it is truly obsolete, or mark it explicitly as a non-wired future-broker placeholder
- Vocabulary/register pass: keep "seat" as the authority-surface term, prefer operational/constitutional seat classes over broad Council language, and translate Pact vocabulary in reviewer/product docs
- Sigil amendment ceremony: choose a universal non-emoji glyph set or revise `docs/proposals/SIGIL_SET_PROPOSAL.md`; if accepted, amend the genesis-anchored Section 0 seat registry, re-anchor Genesis, update Section 1/2/5 references, TECTON `SEAT_SIGILS`, tests, and public presentation in one coordinated v0.1.1 change
- CLOSED for planning: `docs/proposals/V0_1_1_AMENDMENT_PLAN.md` groups the accumulated `docs/PACT_ALIGNMENT.md` Pact text candidates by section and dependency before the v0.1.1 ceremony begins
- Pact wording candidates after code proof: use `docs/PACT_ALIGNMENT.md` as the canonical inventory; ROADMAP should only summarize release sequencing and amendment-plan timing.

Pre-v0.1.0 scope rule:
- Code can continue to harden before the tag where the work improves enforcement, proof, or release honesty.
- Pact text should not be broadly rewritten before the tag. If code proof naturally requires a pre-tag Pact edit, keep it narrow: Section 7 ceremony viability, T-0 recovery authority, and immediately adjacent wording only.
- Everything else in this queue waits for v0.1.1 ceremony unless a release-gate review shows the current v0.1.0 claim would otherwise be false.

### v0.2.0 / TECTON Candidate Queue

These are product/substrate directions, not v0.1.0 blockers:
- internal advisor layer: domain-bounded modules that translate external model analysis into structured, auditable advisory packets without becoming seats or authority holders; primary purpose is false-halt reduction through graduated response, not authorization
- internal advisor packet schema: define the typed packet contract before any advisor/agent implementation, including evidence binding, concern kind, severity, proposed response class, source attribution, packet hash, and authority set to none
- one law, many worlds: TECTON may support tighten-only tenant/domain policy overlays for terms, scope, consent, permissions, hubs, and packs, while the global Pact remains unforked and non-tenant-editable
- multi-voice amendment review: advisor packets can inform T-0 during amendment review, while T-0 and SEAL remain the authority path
- agent terminology: define agentic systems as Tier 3 model/tool loops whose agency grants no authority; proposed actions must re-enter RSS governance before side effects execute
- runtime obligation ledger: track active constraints after authorization so confirmed actions remain bound to container, lease, budget, result-import, verification, and TRACE requirements
- TECTON operator surfaces for amendment queues, ratification previews, drift indicators, cold-verifier reports, consent-source views, and recovery/bypass receipts
- public vocabulary translation table for product copy: Pact terms remain precise internally, while UI language uses operator, authority module, amendment workflow, and system owner where those are clearer

### Phase H — External Trust Anchoring

Preview, not current blocker:
- signed TRACE exports
- timestamp anchoring
- stronger off-box audit posture
- chain-version migration ceremony when `CHAIN_HASH_VERSION` changes
- genuine ingress authentication beyond architectural single-process discipline
- recovery-key and bypass ceremony that cannot strand T-0 outside the system

---

## Open Risks To Keep Visible

Grouped for scanning; the grouping does not reduce severity or remove any disclosed gap.

Identity and authority:
- **Ingress identity:** architectural in v0.1.0, not cryptographic.
- **Safe-Stop clearing:** explicit `t0_command=True` soft sovereign gate today; cryptographic/mechanical identity gate remains future hardening.
- **Cryptographic lock-out:** future identity hardening must include auditable recovery/bypass paths before keys become operationally load-bearing.

Execution and side effects:
- **Side effects:** only governable when they pass through the runtime boundary.
- **Per-action enforcement:** current runtime is request/task-level with action-class gates; per-tool-call gating is active future hardening.
- **Wrapper/API boundary:** context propagation across ASGI, worker threads, background jobs, and external tools remains unresolved.
- **Cross-OS proof:** current proof is Windows-local. Linux, Android-adapter, and macOS claims require their own gates before public wording expands.

Imported content and meaning:
- **Indirect prompt injection:** future external-content importers must preserve the data/instruction boundary across hidden text, metadata, comments, retrieved snippets, and tool returns.
- **RUNE registry scale:** classification is currently linear in active registry size and global unless a caller narrows context. Large vocabulary packs need namespacing, indexing, and lifecycle before RSS claims large-pack performance.
- **RUNE matching edge cases:** current normalization is useful but not full Unicode/confusable defense; punctuation-heavy labels and apostrophe-like terms need tests or validation as the registry grows.
- **RUNE synonym namespace:** synonyms are global today; multi-pack/domain collisions must be namespaced before domain packs can be composed freely.
- **OATH consent duration:** duration is recorded today but not enforced as expiry unless/until v0.1.1 hardening changes that contract.
- **OATH audit dual-failure gap:** if consent persistence fails and the failure callback/audit path also fails, the caller still receives refusal but TRACE may not record the failed consent attempt.
- **OATH coercion check:** current support is a narrow urgency-keyword flag, not a full coercion-defense system.

Persistence, audit, and Pact drift:
- **External audit anchoring:** cold verification exists, but signing/timestamp anchoring is Phase H.
- **Pact drift:** Section 0 integrity is protected today; full-Pact hash verification remains future hardening.
- **Reverse traceability:** `docs/claim_matrix.md` maps Pact-to-tests today, while `docs/pact_code_map.md` maps code-to-Pact references through generated tooling. Neither should be hand-maintained.

Public surface:
- **Terminology drift:** formal Pact vocabulary is useful internally, but reviewer/product surfaces should translate it instead of making "Council" language carry more architecture than exists in code.
- **Demo maturity:** demo quality must not outrun governance integrity.
- **Tenant customization:** product overlays must customize worlds, not fork the law. Tenant policy can tighten the global floor, never loosen it.

---

## Working Rules

- Build ambitiously. Describe conservatively. Prove aggressively.
- Trust is earned by mechanism, not by language.
- What is not proven is not promised.
- If a claim is stronger than the code, either the code rises to meet it or the text steps down to current truth; no middle fog.
- One law, many domains.
- Customize the world; do not fork the law.
- One verdict, not two.
- ROADMAP is the return point after every meaningful pass.
- Generated maps are regenerated, not hand-edited.
- Usefulness matters. Do not optimize only for refusal or rigidity.
- Preserve the distinction between **current truth**, **future phase work**, **aspiration**, and **non-goals**.
- Cold TRACE verification, cold export, and future payload-inclusive external recomputation are separate claims until canonical payload/export proof exists.
- Product design may move forward as structure/spec before every kernel feature is fully complete. The kernel still holds final authority over what is lawful, bounded, auditable, and provable.

---

## Non-Goals For This Release

Do not bend v0.1.0 into claims it cannot honestly support. The point of the release is not to sound complete. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

Explicit non-goals:
- cryptographic non-repudiation
- distributed multi-node TECTON
- REST ingestion layer
- full async-streaming safety in all wrappers
- universal per-action/tool-call enforcement for external side effects
- polished end-user AI product experience
- repo structural refactor into a different package architecture

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
