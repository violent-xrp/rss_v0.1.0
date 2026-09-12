# RSS Phase Ledger

_Licensed under AGPLv3; see `../../LICENSE/LICENSE_INDEX.md`._

This file preserves the landed-work ledger that used to live in `ROADMAP.md`.

`ROADMAP.md` should stay current/future-facing. This ledger records how the system got here.

## Phase A — Persistence, Restart Truth, And Baseline Runtime Integrity

Landed:
- persistence round-trip for TRACE, hubs, sealed terms, synonyms, disallowed terms, and consent state
- historical TRACE chain loaded back into memory on restart
- boot-time verification catches persisted chain tamper
- default EXECUTE consent now respects persisted state rather than overwriting revocations
- entry IDs remain stable across restore paths

## Phase B — Vocabulary And Pipeline Law Hardening

Landed:
- word-boundary matching for sealed terms
- input normalization before classification: NFKC, whitespace, punctuation, and control characters
- anti-trojan definition scanning with explicit force override
- synonym removal returns phrases to null-state without ghost mappings
- compound-term detection through `classify_all()` and attached compound context
- REDLINE count suppressed from normal response surfaces while still auditable through TRACE
- stage/stage_name reporting on pipeline halts

## Phase C — Audit Rigor, Export Discipline, And Failure Semantics

Landed:
- event code registry with optional strict validation
- persistent audit-failure threshold tied to Safe-Stop
- export summary generation and event categorization
- REDLINE artifact-ID sanitization in export paths
- exact-boundary container filtering across TRACE views
- cold/export parity tests for container/global REDLINE handling
- visible `chain_hash_migrate.py` scaffold so version bumps cannot happen silently
- full-envelope event hashing: timestamp, event code, authority, artifact ID, content, parent hash, and `CHAIN_HASH_VERSION`

## Phase D — Container Governance And Ingress Discipline

Landed:
- unified TRACE for TECTON lifecycle and request events
- ingress rejection for non-GLOBAL caller identities without sanctioned delegation
- least-privilege SYSTEM access in container scope
- lifecycle provenance and auditable transitions
- container profile immutability in ACTIVE state
- container-specific rate limiting through CYCLE

Still open under Phase D / adjacent wrapper work:
- real caller authentication beyond single-process ingress discipline
- stronger wrapper/API identity propagation guarantees

## Phase E — Production Posture, Write-Ahead Consent Truth, And Context Isolation

Landed:
- production-mode lockdown flags in config
- OATH write-ahead semantics: no ghost authorization when persistence fails
- OATH failure surfacing into unified TRACE
- context-bound hub isolation via `ContextVar`
- operator-visible ingress posture note

Still open under Phase E:
- thread / worker context propagation beyond current single-process assumptions
- wrapper-layer guarantees for future FastAPI / ASGI surfaces

## Phase F — Pre-Demo Hardening And Governed Usefulness

Landed:
- `trace_verify.py` proof expansion around CLI, schema, Safe-Stop, registry, and filter branches
- `trace_export.py` hardening for exact-boundary redaction and container/global REDLINE handling
- `seal.py` ceremony tightening: input normalization, explicit rejection/ratification paths, clearer idempotence, `ALREADY_RATIFIED` guard
- `oath.py` namespace hardening: uppercase action classes, trimmed requesters/container IDs, delimiter-bearing namespaces fail closed, structured handle errors
- governed offline fallback summarizes scoped data instead of echoing user input
- shared `reference_pack.py` foundation for demo/runtime/examples/tests
- deterministic demo entrypoints built on shared reference data
- runtime/bootstrap moved to config-driven Section 0 path/hash and config-driven default terminology

Phase F proof checklist status:
- `trace_verify.py` proof covered corrupted `system_state`, malformed JSON expectations, mixed known/unknown registry reporting, and cold Safe-Stop read branches
- `trace_export.py` proof covered summary integrity under filters, live/cold consistency, multiple REDLINE IDs, and container/global mixed export cases
- `seal.py` proof covered repeated review after rejection, whitespace-only rationale/proposed text, mixed-case verdict normalization, ratification history ordering, and idempotence
- `oath.py` proof covered persistence-failure density, consent namespace edge cases, blank bindings, and malformed container/action bindings

Phase F coverage status:
- `scribe.py` moved from 73.3% to 100.0%
- `audit/migrate.py` moved from 0.0% to 100.0%
- every package module met the Phase F 80% floor

## Phase G — Demo / Operator Experience

Landed:
- `examples/demo_suite.py` defaults to the live RSS-bound LLM path for human demos
- `--offline` forces deterministic fallback for repeatable proof/demo recordings
- imported `build_demo_report(live_llm=False)` stays deterministic for tests
- transcript demonstrates useful global retrieval, tenant-scoped retrieval, PERSONAL/REDLINE refusal, cross-container isolation, OATH denial/recovery, Safe-Stop persistence/recovery, and cold TRACE verification
- normal advisor workflow uses SYSTEM-only scope so ordinary conversation does not open WORK/PERSONAL data
- `src/main.py demo` uses demo routing so normal chat stays SYSTEM-only while obvious seeded-data questions open governed data paths
- RUNE/domain-pack direction clarified: one shared RUNE law with governed tenant/domain vocabulary packs and flow descriptors
- `reference_pack.py` now uses explicit entry metadata while preserving legacy compatibility through `iter_container_entries()`
- demo world includes construction, legal, medical, and finance packs with pack versions, flows, and vocab hints
- PERSONAL entries can be non-REDLINE or REDLINE explicitly
- global demo data includes finance variance and construction punch-list examples
- container data includes construction change order/safety hold and finance approval/cash-risk scenarios
- `ReferencePackError`, `validate_reference_pack()`, and `validate_demo_containers()` fail loud before malformed data can seed runtime state
- `seed_demo_world()` validates global rows and container packs before loading either
- validation covers labels, domains, pack versions, summaries, flows, vocab terms, questions, entry hubs, content, duplicate labels, and boolean REDLINE markers
- legacy tuple rows remain tolerated for backward/local compatibility
- `reference_pack.py` is now at 100.0% statement coverage
- `build_operator_summary()` and `write_demo_artifacts()` generate handoff artifacts from the same governed demo run
- `python examples/demo_suite.py --offline --artifacts demo_artifacts` writes `demo_report.json`, `demo_summary.md`, and `demo_trace.json`
- PAV now enforces `forbidden_sources` during advisory-view construction
- indirect prompt-injection proof pins poisoned retrieved content as scoped data, not authority, with REDLINE/PERSONAL exclusion and OATH state preserved
- `save_untrusted_content()` gives future external connectors a canonical data-only import boundary with provenance, persistence, and TRACE
- untrusted import receipts now hash-bind source and wrapped content with SHA-256 digests, byte lengths, provenance persistence, TRACE digest payloads, and mutation detection
- Phase G coverage floor is closed: every package module is at or above 85%
- `cycle.py` proof now covers strict-mode diagnostics and handle routing branches
- `trace_verify.py` proof now covers filtered broken-chain human reports, unknown-code listings, CLI stats, JSON schema errors, and absent Safe-Stop table handling
- demo handoff now gives reviewers a fast path, artifact inspection order, proof-signal checklist, and release-boundary language
- external vocabulary map added for engineers/reviewers who need plain-language equivalents for RSS terms without renaming the system vocabulary

Still open:
- optional signed/export-bundle structure once external trust anchoring begins
- governed pack selection/versioning once multiple demo worlds or tenant-specific packs exist
- connector-specific indirect-prompt-injection proof matrix for future browser, email, document, RAG, tool-return, and Unicode-heavy inputs

## Post-rc.1 Hardening And Proof Discipline

Landed:
- cold TRACE REDLINE export now routes REDLINE ID collection through the `Persistence.redline_entry_ids()` seam before falling back to SQLite internals, keeping export sanitization behind the storage boundary
- TRACE audit writes now serialize chain append plus persistence through the audit lock, preserving cold-verifiable hash-chain order under concurrent governed writes in the current single-process runtime
- `docs/PROJECT_STATUS.md` is generated by `docs/build_project_status.py` as a public current-state view; it reports proof snapshot, deterministic drift light, and reviewer entry points without becoming a new truth source
- public hygiene now checks generated Project Status freshness after baseline sync and reverse Pact-code-map gates have already passed, avoiding a duplicate acceptance/coverage run
- the Project Status generator now fails closed on dead internal reviewer links, so public status navigation cannot silently drift after doc renames

Still open:
- multi-process/distributed audit throughput remains future work; the current TRACE concurrency fix is a single-process/threaded integrity guarantee
- generated status views do not replace semantic review of prose claims; they report mechanical freshness and proof surfaces only

## Phase H — External Trust Anchoring And Deployment-Boundary Maturity

Future work:
- external signing
- timestamp anchoring
- stronger off-box audit posture
- deployment-layer non-repudiation story
- genuine ingress authentication rather than architectural single-process discipline

## Integrated Review Findings Archive

The full-module review surfaced several real issues that have since been closed or moved into future watch.

Priority A closures:
- TECTON destructive transitions now require reasons
- `clear_safe_stop()` is idempotent
- LLM availability check timeout is config-driven
- `archive_entry()` returns the archived `HubEntry`

Priority B closures:
- `_PIPELINE_STAGES` promoted to module-level constant
- stale coverage notes moved out of current public claims
- large monolithic test file split mechanically while keeping `tests/test_all.py` as the runner
- `load_constitution()` directly tested
- PAV unknown sanitize policy now raises
- CYCLE strict mode added for diagnostic callers

Priority C closures:
- module count wording resolved to the `src/rss/` package rule
- assertion-count drift resolved by runner output
- claim matrix regenerated after all tagged-test updates
- `conftest.py` module wording resolved
- demo suite now derives isolation pair from configured demo containers rather than hardcoded labels

Low-priority observations still visible:
- `audit_log.verify_chain()` returns bool only while the cold verifier returns a detail dict
- `persistence.save_hub_entry` uses `INSERT OR REPLACE`; UUID collision is theoretical, but `INSERT OR ABORT` would be more fail-loud in an audit-first posture

## Landed Work Since The Earlier Public Baseline

Test / proof growth:
- baseline moved from **111 / 850 / 0** to **139 / 1171 / 0**
- constitution loader edge coverage
- LLM adapter prompt/fallback/config-aware coverage
- SCRIBE UAP/status/handler edge coverage
- cold TRACE verifier CLI/error/Safe-Stop coverage
- extended OATH, SEAL, and TRACE export coverage
- OATH namespace and persistence-failure density
- chain-hash migration scaffold proof
- runner-truth hardening
- demo/reference-pack proof
- Phase G demo-suite proof
- Phase G normal-advisor boundary proof
- Phase G reference-pack v2 proof
- Phase G demo-pack validation proof
- Phase G demo artifact proof
- indirect prompt-injection proof
- untrusted-content import boundary proof
- Phase G coverage-floor proof
- untrusted import hash-binding proof

Hardening fixes:
- R1 repo restructure into `src/rss/`
- config-driven default term packs and definition prefixes
- Section 0 config binding to real path/hash
- cold TRACE export sanitizes REDLINE IDs from container rows as well as global rows
- exact-boundary container filtering parity
- `trace_verify.py` exit-code and registry-load handling hardened
- OATH blank-container normalization and delimiter guard
- SEAL amendment normalization and explicit `ALREADY_RATIFIED`
- TECTON destructive transition reasons
- `clear_safe_stop()` idempotence
- `archive_entry()` return parity
- PAV unknown policy raise
- PAV forbidden-source enforcement
- untrusted import source/wrapped digest receipts and mutation detection
- CYCLE strict mode
- LLM availability timeout config
- governed offline fallback
- reference-pack v2
- demo artifact export bundle
- modularized tests with stable acceptance runner

Honesty / release-surface clarifications:
- custom acceptance harness is canonical
- `pytest` parity is optional
- source-module layout rule tied to `src/rss/`
- ingress posture is architectural, not cryptographic
- README names collaboration targets without inflating current claims

## DOCS-02 Historical Carry-Forward

Recorded 2026-09-11 from ROADMAP at `0b4ca43`. The pre-existing ledger above is
unchanged. These literal snapshots preserve earlier wording and evidence; they
are not current instructions, renewed proof, or assertions about remote state.
Current Genesis planning, priority, and release obligations belong to
[ROADMAP](../../ROADMAP.md#current-build-thread). Old version/phase names below
retain their historical meaning and are not renumbered.

### Earlier Release Wording

Former ROADMAP lines 5-18. In particular, rc.1 measurements remain
historical, unbolded evidence, outside current-baseline generation and scanning.

```text
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
```

### rc.1 Scope and Proof Snapshot

Former ROADMAP lines 266-344. In particular, rc.1 measurements remain
historical, unbolded evidence, outside current-baseline generation and scanning.

```text
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
```

### Earlier Exit Criteria

Former ROADMAP lines 348-370. In particular, rc.1 measurements remain
historical, unbolded evidence, outside current-baseline generation and scanning.

```text
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
```

### Closed-Item Retirement Proposals — Records Retained

Retirement/deduplication is proposed, not performed. Human approval is still
required before discarding a distinct record. Exact duplicates already present
in this ledger retain that earlier survivor; the additional literal records
below were not all present here. Any unfinished condition embedded in a CLOSED
item remains open and has a current detail route; the label is not blanket closure.

Former ROADMAP line 167:

```text
- **Pre-tag RUNE/OATH hardening map:** closed. OATH requester fallback, RUNE constraint-prompt proof, and RUNE longest bounded-match precedence are now proven.
```

Former ROADMAP line 168:

```text
- **Action proposal / broker decision surface:** closed as a bounded code slice. RSS now has structured `ActionProposal` objects and a `SideEffectBroker` that reviews proposed side effects, emits TRACE receipts, issues short-lived in-process single-use authorization receipts, supports pre-execution claim/revocation, and imports claimed results as untrusted data-only evidence. It does not execute tools, persist leases, auto-wire into `Runtime.process_request`, or claim universal per-action enforcement.
```

Former ROADMAP line 169:

```text
- **RUNE embedded disallowed scan:** closed as a code helper and used by the action broker to audit longer payload strings for bounded disallowed terms while preserving `classify()` exact-match semantics.
```

Former ROADMAP line 170:

```text
- **TRACE v2 audit integrity:** closed as a persistence/audit hardening slice. New TRACE rows carry a versioned stored-field hash envelope (`payload_hash` + `hash_version`), the cold verifier recomputes v2 envelopes and detects downgrade attempts, boot verification uses the deep verifier, production mode forces SQLite `synchronous=FULL`, and ratified amendment persistence is atomic. This improves local stored-field integrity; it does not claim external signing, timestamp anchoring, or payload-inclusive third-party recomputation.
```

Former ROADMAP line 171:

```text
- **Safe-Stop clear atomicity:** closed as a bounded single-process persistence slice. The clear receipt and halt deletion now share one explicit SQLite transaction; failed receipt persistence leaves the prior halt active, post-commit adapter errors reconcile from exact durable state, and unconfirmable outcomes remain recovery-fenced until restart verification. General governed-state/receipt coupling remains separate work.
```

Former ROADMAP line 172:

```text
- **Restricted halted-bootstrap recovery:** closed as a bounded Section 0 surface. A boot that begins in Safe-Stop, or fails pre-emission TRACE verification and establishes a durable recovery fence, returns `SafeStopRecovery` rather than the broad `Runtime`; if that fence cannot persist, bootstrap closes and raises. The facade exposes status, atomic T-0 clear, and lifecycle close only. Successful clear closes the recovery session and requires a fresh bootstrap before execution or governed-state access. This is a public-surface restriction inside the trusted single process, not process isolation, cryptographic T-0 identity, constructor/migration purity, or revocation of references retained before an in-process halt.
```

Former ROADMAP line 173:

```text
- **Production Genesis before authority:** closed as a bounded bootstrap slice. After TRACE continuity is restored and any pre-existing halt is routed to recovery, bootstrap verifies the configured Section 0 artifact before normal term initialization, migration receipts/schema stamping, governed-state restore, or default EXECUTE consent. Missing required or mismatched Genesis establishes persistent Safe-Stop and returns `SafeStopRecovery`; valid production and documented missing-artifact dev mode continue normally. This does not move verification ahead of `Runtime` construction or constructor-time schema migration or extend integrity beyond Section 0; those remain separate invariants.
```

Former ROADMAP line 174:

```text
- **Critical persisted consent before authority:** the baseline gate and reviewed alias correction are checkpointed in Roots. Before normal terms, migration receipts/schema stamping, restore, or default authority, bootstrap examines every durable row claiming the canonical `GLOBAL:EXECUTE` key or OATH-normalized namespace. Noncanonical aliases, unknown status, key/tuple mismatch, blank requester, duplicate shadow row, or consent-load failure establishes persistent Safe-Stop and exposes only `SafeStopRecovery`; failed fencing closes and raises. Invalid rows remain durable evidence, and the registered proof covers both restore modes without calling OATH authorization. This does not validate every tenant/action consent, add tuple uniqueness to the SQLite schema, preserve consent scope/duration/grant-time fidelity, couple Safe-Stop entry atomically, or claim protection from external database writers between validation and use.
```

Former ROADMAP line 175:

```text
- **Governance boundary hardening:** closed as a code-backed pre-release slice. OATH now treats GLOBAL `DENIED` as a restrictive kernel prohibition, runtime HIGH_RISK/CONSTITUTIONAL requests require elevated consent classes, WARD blocks protected-field injection/removal, RUNE update paths run the anti-trojan scanner while force-sealed terms survive restore, SEAL refuses mismatched restored canon hashes, post-LLM REDLINE scan failure withholds output, and TECTON separates suspended-read access from suspended request processing.
```

Former ROADMAP line 183:

```text
- CLOSED: Sections 1-7 cleanup landed after Section 0; implementation-reference drift, CYCLE load wording, S5/S6 concurrency and persistence boundaries, and S7 amendment-persistence wording now match the current kernel truth.
```

Former ROADMAP line 184:

```text
- CLOSED FOR `v0.1.0-rc.1`: final acceptance, sync, claim-matrix, and offline demo gates passed before the tag. The ignored local demo bundle reports `PASS`, 22/22 successful task IDs bound to TRACE, 14/14 expected evidence markers found, and cold verification over 192 events. Rerun the gates before final `v0.1.0`.
```

Former ROADMAP line 228:

```text
- CLOSED: Seat interface decision for SCOPE/RUNE resolved by adding WARD-compatible adapters while preserving direct runtime request-path calls.
```

Former ROADMAP line 230:

```text
- CLOSED: CYCLE fail-closed proof now covers internal runtime-stage exceptions as `UNEXPECTED_ERROR` at Stage 6, in addition to strict-mode unknown-domain rejection.
```

Former ROADMAP line 231:

```text
- CLOSED: SEAL external attribution scanner now blocks generic external-advisor/model authorship and authority-attribution phrases, including common verb/preposition/actor evasions, while still allowing bare non-authority mentions.
```

Former ROADMAP line 239:

```text
- CLOSED: reverse Pact-code map now lives at `docs/pact_code_map.md`, generated by `docs/build_pact_code_map.py` and checked by public hygiene. Full-Pact hash/integrity enforcement remains future hardening.
```

Former ROADMAP line 240:

```text
- CLOSED: generated public Project Status now lives at `docs/PROJECT_STATUS.md`, generated by `docs/build_project_status.py`, checked by public hygiene, and guarded against dead reviewer links. It is a status view, not a new truth source.
```

Former ROADMAP line 426:

```text
- OATH routed `authorize` now fails closed when `requester` is missing or blank instead of defaulting to T-0; proof verifies no consent record is created and explicit requester flow still works
```

Former ROADMAP line 427:

```text
- RUNE contextual reinjection now has capture-adapter proof that sealed-term constraints remain kernel metadata and are excluded from advisor prompt text
```

Former ROADMAP line 428:

```text
- RUNE primary substring classification now prefers the longest bounded sealed-term match so registration order cannot make a shorter term outrank a more specific phrase
```

Former ROADMAP line 429:

```text
- stale top-level duplicate modules `src/pav.py` and `src/reference_pack.py` removed; canonical code now lives under `src/rss/`
```

Former ROADMAP line 430:

```text
- cold TRACE verifier now fails full-chain verification when the first surviving row still has a parent hash, detecting head truncation while preserving filtered container-view semantics
```

Former ROADMAP line 431:

```text
- `_validate_llm_response()` now documents that response scanning is downstream sanitation, while SCOPE/PAV/OATH remain the authoritative upstream boundary
```

Former ROADMAP line 432:

```text
- Section 3 execution validation now re-hashes `ExecutionIntent.raw_text` before execution and rejects far-future TTLs on externally constructed intents
```

Former ROADMAP line 433:

```text
- SEAL amendment proposals now reject external advisor attribution before review or ratification, so forbidden authorship claims cannot sit in actionable proposal state
```

Former ROADMAP line 434:

```text
- SEAL ceremony TRACE emission now fails closed when a trace callback is wired: proposal, review, and ratification do not mutate ceremony state if amendment audit emission fails
```

Former ROADMAP line 435:

```text
- WARD registration now fails fast when a seat lacks the standard `status()` / `handle(task)` interface, so malformed routable seats cannot enter the registry.
```

Former ROADMAP line 437:

```text
- action-plane decision surface added: `rss.action` provides typed proposals, broker gate review, TRACE receipts, in-process claim/revocation, and untrusted result import without executing tools or persisting leases
```

Former ROADMAP line 439:

```text
- demo artifact proof now records per-question proof rows, expected governed-evidence markers, and successful task IDs bound to TRACE artifacts so useful retrieval cannot pass on fluent but ungrounded answers
```

Former ROADMAP line 476:

```text
- CLOSED: OATH structured `check(detailed=True)` preserves the current string return while exposing consent source (`CONTAINER`, `GLOBAL`, `GLOBAL_FALLBACK`, `ABSENT`, `ERROR`) for audit/reviewer context.
```

Former ROADMAP line 478:

```text
- CLOSED: OATH explicit `DENIED` consent status and `deny()` operation now let a container-specific denial override GLOBAL authorization, and DENIED records survive restore/restart without being upgraded.
```

Former ROADMAP line 479:

```text
- CLOSED: OATH coercion wording cleanup renamed the current urgency-word check as `detect_coercion_keyword_limited()` / `keyword_flagged` while preserving a legacy wrapper; real governed coercion-warning semantics remain future work.
```

Former ROADMAP line 484:

```text
- CLOSED: TECTON rate-limit input validation now rejects non-positive or malformed `max_requests_per_minute` values at profile construction and mutation boundaries, while invalid legacy persisted values sanitize visibly to the default on restore.
```

Former ROADMAP line 485:

```text
- CLOSED at OATH API boundary: structured consent checks expose whether authorization came from container-specific consent, GLOBAL, GLOBAL fallback, absent consent, or validation error. Runtime response/TRACE surfacing remains future product work.
```

Former ROADMAP line 489:

```text
- CLOSED: Section 6 live export sanitizer hardening now aborts JSON/text exports if REDLINE ID collection from live hubs fails, rather than producing a silently trusted export
```

Former ROADMAP line 490:

```text
- CLOSED: Restore visibility hardening now counts skipped persisted records in `restore_skips`, stores structured `runtime.restore_warnings`, and prints restore warnings for malformed or duplicate terms, synonyms, consents, and hub entries instead of silently swallowing them.
```

Former ROADMAP line 491:

```text
- CLOSED: PAV/runtime skipped-source visibility now records skipped-source metadata for forbidden sources, standard LEDGER exclusion, and hub-read failures, and runtime responses expose only the skipped-source count without leaking skipped content or exception messages.
```

Former ROADMAP line 492:

```text
- CLOSED: Section 7 amendment persistence now persists proposals, review state, ratified amendment records, reconstructed canon state, and queryable history across restart
```

Former ROADMAP line 493:

```text
- CLOSED: canonical versioning model now lives in `docs/VERSIONING.md`: project/release versions use semver, `-rc.N` is release-candidate iteration only, and Pact section versions are internal amendment records that surface through a project MINOR bump when sealed.
```

Former ROADMAP line 497:

```text
- CLOSED: reverse Pact-code map generation now reports code references by Pact section, source references without matching Pact headings, Pact sections without source refs, and governance modules without Pact refs
```

Former ROADMAP line 498:

```text
- CLOSED: guarded Sections 1-7 canon-to-file export now lives in `rss.audit.pact_canon_export` with dry-run default, stale-base refusal, explicit T-0 write gate, atomic writes, first-canon `--expected-file-hash`, and Section 0 refusal
```

Former ROADMAP line 504:

```text
- CLOSED for planning: `docs/proposals/V0_1_1_AMENDMENT_PLAN.md` groups the accumulated `docs/PACT_ALIGNMENT.md` Pact text candidates by section and dependency before the v0.1.1 ceremony begins
```

Former ROADMAP line 176, also retained literally pending retirement approval:

```text
- **Pact cleanup checkpoint:** the section-by-section Pact cleanup (Sections 0-7) is landed and pushed. Future Pact text changes move through the v0.1.1 amendment ceremony unless a release-gate review proves v0.1.0 would otherwise be false.
```

### Routes for Earlier Still-Open Lists

These are historical-to-detail routes, not priority or new closure claims:

- Phase D caller authentication and wrapper identity: [ingress finding](../KERNEL_FINDINGS.md#caller-identity-and-ingress-boundary).
- Phase E thread/worker and wrapper context: [propagation finding](../KERNEL_FINDINGS.md#thread-and-worker-context-propagation).
- Phase G connector IPI: [import/PAV detail](../PACT_ALIGNMENT.md#retained-import-and-pav-detail); governed pack selection: [tenant detail](../PACT_ALIGNMENT.md#retained-tenant-and-seat-detail); signed bundles: [external proof](../PACT_ALIGNMENT.md#retained-external-proof-detail).
- Post-rc.1 throughput and generated-shape-versus-semantic-review limits: [deployment/proof detail](../PACT_ALIGNMENT.md#retained-deployment-and-proof-detail).
- Phase H anchoring and chain migration: [external proof](../PACT_ALIGNMENT.md#retained-external-proof-detail); ingress and recovery: [kernel findings](../KERNEL_FINDINGS.md).
- Integrated-review verifier-return consistency and Hub collision behavior: [persistence detail](../PACT_ALIGNMENT.md#retained-persistence-and-authority-detail).

### Earlier Snapshot and Command Context

Former ROADMAP lines 43-72, retained literally as historical context, not fresh
acceptance or an instruction to run these commands in this documentation pass.

````text
## Current Snapshot

Current code state:
- **180 test functions / 2908 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **92.7% statement coverage** via `python run_coverage.py`
- **180 claims / 180 tests / 124 Pact sections** in `docs/claim_matrix.md`
- **26 kernel modules** in the `src/rss/` package tree plus `src/main.py`
- active work: **Current Build Thread below**; Phase G is retained as phase history, not the current task selector

Current posture:
- public-alpha hardening is materially beyond the earlier 111/850 baseline
- the acceptance harness is the single local truth command
- public docs are synced to the current 180/2908 baseline
- historical Phase G work and release inventories do not override the current build queue

Canonical local truth-run:
```bash
python tests/test_all.py
```

Optional local checks:
```bash
python run_coverage.py
python docs/build_claim_matrix.py
python docs/build_project_status.py --check
python docs/sync_baseline.py --check --require-clean
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Note: on the current Windows environment, `pytest` is not installed / not on PATH. `pytest` parity is optional tooling, not the source of truth.
````
